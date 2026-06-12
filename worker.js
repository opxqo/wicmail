/**
 * WicMail / Private Mailbox - Cloudflare Email Worker
 *
 * 功能：
 * 1. 接收 Cloudflare Email Routing 转来的邮件
 * 2. 读取 envelope、headers、raw 原始邮件
 * 3. 将邮件推送到 FastAPI
 * 4. 推送失败时转发到备用邮箱，避免邮件直接丢失
 *
 * 必填环境变量：
 * - FASTAPI_URL      FastAPI 接收接口，例如：https://api.example.com/api/inbound/cloudflare
 * - SECRET_KEY       Worker 和 FastAPI 共享密钥
 *
 * 可选环境变量：
 * - FALLBACK_EMAIL      备用邮箱，FastAPI 故障时兜底转发
 * - MAX_RAW_SIZE_MB     单封邮件 raw 传输上限，默认 10
 * - REQUEST_TIMEOUT_MS  请求 FastAPI 超时时间，默认 20000
 * - FORWARD_TOO_LARGE   raw 超限时是否转发到备用邮箱，默认 true
 * - REJECT_ON_FAILURE   推送失败且没有备用邮箱时是否拒收，默认 false
 */

import PostalMime from "postal-mime";

const WORKER_VERSION = "1.0.0";

export default {
    async email(message, env, ctx) {
        const logger = new Logger("WicMailWorker");
        const requestId = crypto.randomUUID();

        const config = getConfig(env);

        logger.info(
            `收到邮件 request_id=${requestId} from=${message.from} to=${message.to} rawSize=${message.rawSize}`
        );

        // 1. 基础配置校验
        if (!config.fastapiUrl || !config.secretKey) {
            logger.error("缺少 FASTAPI_URL 或 SECRET_KEY，无法推送到后端");

            if (config.fallbackEmail) {
                await safeForward(message, config.fallbackEmail, requestId, "worker_misconfigured", logger);
            } else {
                message.setReject("Email worker is not configured");
            }

            return;
        }

        // 2. 收集邮件头信息
        const headersObject = headersToObject(message.headers);

        const basePayload = {
            source: "cloudflare-email-worker",
            worker_version: WORKER_VERSION,
            request_id: requestId,

            envelope_from: message.from,
            envelope_to: message.to,

            header_from: message.headers.get("from") || "",
            header_to: message.headers.get("to") || "",
            header_cc: message.headers.get("cc") || "",
            header_reply_to: message.headers.get("reply-to") || "",

            subject: message.headers.get("subject") || "",
            message_id: message.headers.get("message-id") || "",
            date: message.headers.get("date") || "",

            headers: headersObject,

            raw_size: typeof message.rawSize === "number" ? message.rawSize : null,
            raw: null,
            raw_encoding: null,
            raw_sha256: null,
            raw_too_large: false,
            attachments: [],

            received_at: new Date().toISOString(),
        };

        // 3. 判断 raw 是否超过你自己设置的传输上限
        const rawSize = typeof message.rawSize === "number" ? message.rawSize : 0;
        const rawTooLarge = rawSize > config.maxRawBytes;

        if (rawTooLarge) {
            basePayload.raw_too_large = true;

            logger.warn(
                `邮件 raw 超出自定义上限 request_id=${requestId} rawSize=${rawSize} maxRawBytes=${config.maxRawBytes}`
            );
        } else {
            try {
                const rawBuffer = await new Response(message.raw).arrayBuffer();

                basePayload.raw = arrayBufferToBase64(rawBuffer);
                basePayload.raw_encoding = "base64";
                basePayload.raw_sha256 = await sha256Hex(rawBuffer);
                basePayload.attachments = await parseAndUploadAttachments(
                    rawBuffer,
                    requestId,
                    env,
                    logger
                );

                logger.info(
                    `raw 读取完成 request_id=${requestId} sha256=${basePayload.raw_sha256}`
                );
            } catch (error) {
                logger.error(`读取 raw 失败 request_id=${requestId} error=${formatError(error)}`);
            }
        }

        // 4. 推送到 FastAPI
        let pushSuccess = false;

        try {
            const result = await postToFastAPI(
                config.fastapiUrl,
                basePayload,
                config.secretKey,
                config.requestTimeoutMs
            );

            pushSuccess = result.ok;

            if (result.ok) {
                logger.info(
                    `推送 FastAPI 成功 request_id=${requestId} status=${result.status}`
                );
            } else {
                logger.error(
                    `推送 FastAPI 失败 request_id=${requestId} status=${result.status} body=${result.body}`
                );
            }
        } catch (error) {
            logger.error(`请求 FastAPI 异常 request_id=${requestId} error=${formatError(error)}`);
        }

        // 5. raw 超限时，后端只能收到元数据；建议额外转发一份到备用邮箱
        if (pushSuccess && rawTooLarge) {
            if (config.forwardTooLarge && config.fallbackEmail) {
                logger.warn(
                    `raw 超限，已推送元数据，开始转发完整邮件到备用邮箱 request_id=${requestId}`
                );

                await safeForward(message, config.fallbackEmail, requestId, "raw_too_large", logger);
            } else {
                logger.warn(
                    `raw 超限，但未配置转发 request_id=${requestId}，后端将只有邮件元数据`
                );
            }

            return;
        }

        // 6. 推送失败时兜底转发
        if (!pushSuccess) {
            if (config.fallbackEmail) {
                logger.warn(
                    `推送失败，开始兜底转发 request_id=${requestId} fallback=${config.fallbackEmail}`
                );

                await safeForward(message, config.fallbackEmail, requestId, "backend_failed", logger);
                return;
            }

            if (config.rejectOnFailure) {
                logger.warn(`推送失败且没有备用邮箱，拒收邮件 request_id=${requestId}`);
                message.setReject("Temporary internal mail delivery failure");
                return;
            }

            logger.error(
                `推送失败且没有备用邮箱，邮件可能丢失 request_id=${requestId}`
            );
        }
    },
};

/**
 * 读取 Worker 环境变量
 */
function getConfig(env) {
    const maxRawSizeMb = numberOrDefault(env.MAX_RAW_SIZE_MB, 10);
    const requestTimeoutMs = numberOrDefault(env.REQUEST_TIMEOUT_MS, 20_000);

    return {
        fastapiUrl: stringOrEmpty(env.FASTAPI_URL),
        secretKey: stringOrEmpty(env.SECRET_KEY),
        fallbackEmail: stringOrEmpty(env.FALLBACK_EMAIL),

        maxRawSizeMb,
        maxRawBytes: Math.floor(maxRawSizeMb * 1024 * 1024),

        requestTimeoutMs,

        forwardTooLarge: boolOrDefault(env.FORWARD_TOO_LARGE, true),
        rejectOnFailure: boolOrDefault(env.REJECT_ON_FAILURE, false),
    };
}

/**
 * 解析 MIME 附件并上传到 R2
 */
async function parseAndUploadAttachments(rawBuffer, requestId, env, logger) {
    if (!env.ATTACHMENTS) {
        logger.warn(`R2 绑定 ATTACHMENTS 未配置，跳过附件上传 request_id=${requestId}`);
        return [];
    }

    let parsed;
    try {
        const parser = new PostalMime();
        parsed = await parser.parse(new Uint8Array(rawBuffer));
    } catch (error) {
        logger.error(`附件 MIME 解析失败 request_id=${requestId} error=${formatError(error)}`);
        return [];
    }

    const attachments = parsed.attachments || [];
    if (attachments.length === 0) {
        return [];
    }

    const results = [];

    for (const att of attachments) {
        const content = att.content;
        if (!content) {
            logger.warn(`附件内容为空，跳过上传 request_id=${requestId} file=${att.filename || "unnamed"}`);
            continue;
        }

        const contentSha256 = await sha256Hex(content);
        const filename = att.filename || "unnamed";
        const safeFilename = sanitizeFilename(filename);
        const r2Key = `attachments/${requestId}/${contentSha256}_${safeFilename}`;
        const contentType = att.mimeType || "application/octet-stream";
        const size = getByteLength(content);

        try {
            await env.ATTACHMENTS.put(r2Key, content, {
                httpMetadata: {
                    contentType,
                },
                customMetadata: {
                    requestId,
                    originalFilename: filename,
                    contentSha256,
                },
            });

            results.push({
                filename,
                content_type: contentType,
                size,
                r2_key: r2Key,
                content_sha256: contentSha256,
                is_inline: Boolean(att.contentId),
                content_id: att.contentId || null,
            });

            logger.info(
                `附件上传成功 request_id=${requestId} file=${safeFilename} size=${size} key=${r2Key}`
            );
        } catch (error) {
            logger.error(
                `附件上传失败 request_id=${requestId} file=${safeFilename} error=${formatError(error)}`
            );
        }
    }

    return results;
}

/**
 * 文件名安全处理，避免路径分隔符和特殊字符进入对象 key
 */
function sanitizeFilename(name) {
    const cleaned = String(name)
        .replace(/[/\\:*?"<>|]/g, "_")
        .replace(/\s+/g, "_")
        .replace(/^\.+$/, "unnamed")
        .slice(0, 200);

    return cleaned || "unnamed";
}

/**
 * 获取 ArrayBuffer 或 TypedArray 的字节长度
 */
function getByteLength(value) {
    if (typeof value.byteLength === "number") {
        return value.byteLength;
    }

    return 0;
}

/**
 * 推送 JSON 到 FastAPI
 *
 * Header 说明：
 * - X-Secret-Key：简单共享密钥校验
 * - X-Worker-Timestamp：签名时间
 * - X-Worker-Signature：HMAC-SHA256 签名，后端可选验证
 */
async function postToFastAPI(url, payload, secretKey, timeoutMs) {
    const body = JSON.stringify(payload);
    const timestamp = new Date().toISOString();
    const signature = await hmacSha256Hex(secretKey, `${timestamp}.${body}`);

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",

            "X-Secret-Key": secretKey,
            "X-Worker-Timestamp": timestamp,
            "X-Worker-Signature": signature,
            "X-Worker-Version": WORKER_VERSION,

            "User-Agent": `WicMail-Cloudflare-Email-Worker/${WORKER_VERSION}`,
        },
        body,
        signal: timeoutSignal(timeoutMs),
    });

    const responseBody = response.ok
        ? ""
        : await response.text().catch(() => "");

    return {
        ok: response.ok,
        status: response.status,
        body: responseBody,
    };
}

/**
 * 兜底转发
 *
 * 注意：
 * Cloudflare 的 message.forward() 只能转发到账号里已验证的目标邮箱。
 * 可附加的转发 Header 只能是 X-* 类型。
 */
async function safeForward(message, targetEmail, requestId, reason, logger) {
    if (!targetEmail) {
        logger.warn(`没有配置 FALLBACK_EMAIL，无法兜底转发 request_id=${requestId}`);
        return false;
    }

    try {
        const extraHeaders = new Headers();

        extraHeaders.set("X-WicMail-Request-ID", requestId);
        extraHeaders.set("X-WicMail-Forward-Reason", reason);
        extraHeaders.set("X-WicMail-Worker-Version", WORKER_VERSION);

        await message.forward(targetEmail, extraHeaders);

        logger.info(
            `兜底转发成功 request_id=${requestId} target=${targetEmail} reason=${reason}`
        );

        return true;
    } catch (error) {
        logger.error(
            `兜底转发失败 request_id=${requestId} target=${targetEmail} error=${formatError(error)}`
        );

        return false;
    }
}

/**
 * Headers 转普通对象
 */
function headersToObject(headers) {
    const result = {};

    for (const [key, value] of headers.entries()) {
        if (result[key] === undefined) {
            result[key] = value;
        } else if (Array.isArray(result[key])) {
            result[key].push(value);
        } else {
            result[key] = [result[key], value];
        }
    }

    return result;
}

/**
 * ArrayBuffer 转 base64
 */
function arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    const chunkSize = 0x8000;
    let binary = "";

    for (let i = 0; i < bytes.length; i += chunkSize) {
        const chunk = bytes.subarray(i, i + chunkSize);
        binary += String.fromCharCode(...chunk);
    }

    return btoa(binary);
}

/**
 * SHA-256 Hex
 */
async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest("SHA-256", buffer);
    return arrayBufferToHex(digest);
}

/**
 * HMAC-SHA256 Hex
 */
async function hmacSha256Hex(secret, message) {
    const encoder = new TextEncoder();

    const key = await crypto.subtle.importKey(
        "raw",
        encoder.encode(secret),
        {
            name: "HMAC",
            hash: "SHA-256",
        },
        false,
        ["sign"]
    );

    const signature = await crypto.subtle.sign(
        "HMAC",
        key,
        encoder.encode(message)
    );

    return arrayBufferToHex(signature);
}

/**
 * ArrayBuffer 转 Hex
 */
function arrayBufferToHex(buffer) {
    const bytes = new Uint8Array(buffer);

    return [...bytes]
        .map((byte) => byte.toString(16).padStart(2, "0"))
        .join("");
}

/**
 * 超时 Signal
 */
function timeoutSignal(ms) {
    if (
        typeof AbortSignal !== "undefined" &&
        typeof AbortSignal.timeout === "function"
    ) {
        return AbortSignal.timeout(ms);
    }

    const controller = new AbortController();

    setTimeout(() => {
        controller.abort();
    }, ms);

    return controller.signal;
}

/**
 * 字符串环境变量
 */
function stringOrEmpty(value) {
    if (value === undefined || value === null) {
        return "";
    }

    return String(value).trim();
}

/**
 * 数字环境变量
 */
function numberOrDefault(value, defaultValue) {
    const parsed = Number(value);

    if (!Number.isFinite(parsed) || parsed <= 0) {
        return defaultValue;
    }

    return parsed;
}

/**
 * 布尔环境变量
 */
function boolOrDefault(value, defaultValue) {
    if (value === undefined || value === null || value === "") {
        return defaultValue;
    }

    const normalized = String(value).trim().toLowerCase();

    if (["true", "1", "yes", "y", "on"].includes(normalized)) {
        return true;
    }

    if (["false", "0", "no", "n", "off"].includes(normalized)) {
        return false;
    }

    return defaultValue;
}

/**
 * 格式化错误
 */
function formatError(error) {
    if (!error) {
        return "Unknown error";
    }

    if (error instanceof Error) {
        return `${error.name}: ${error.message}`;
    }

    return String(error);
}

/**
 * 简单日志类
 */
class Logger {
    constructor(name) {
        this.name = name;
    }

    info(message) {
        console.log(`[${this.name}][INFO][${new Date().toISOString()}] ${message}`);
    }

    warn(message) {
        console.warn(`[${this.name}][WARN][${new Date().toISOString()}] ${message}`);
    }

    error(message) {
        console.error(`[${this.name}][ERROR][${new Date().toISOString()}] ${message}`);
    }
}
