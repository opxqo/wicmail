"""
邮件服务模块 - 阿里云企业邮箱 SMTP
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Union, Dict
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class SMTPConfig:
    host: str = os.getenv("SMTP_HOST", "smtp.qiye.aliyun.com")
    port: int = int(os.getenv("SMTP_PORT", "465"))
    user: str = os.getenv("SMTP_USER", "")
    password: str = os.getenv("SMTP_PASSWORD", "")
    from_name: str = os.getenv("SMTP_FROM_NAME", "WIC Mail")
    use_ssl: bool = os.getenv("SMTP_USE_SSL", "true").lower() == "true"


class EmailService:
    def __init__(self, config: Optional[SMTPConfig] = None):
        self.config = config or SMTPConfig()

    def _create_connection(self) -> Union[smtplib.SMTP_SSL, smtplib.SMTP]:
        """创建 SMTP 连接"""
        if self.config.use_ssl:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(
                self.config.host,
                self.config.port,
                context=context,
                timeout=30,
            )
        else:
            server = smtplib.SMTP(
                self.config.host,
                self.config.port,
                timeout=30,
            )
            server.starttls()

        server.login(self.config.user, self.config.password)
        return server

    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        body: str,
        html: bool = False,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict:
        """
        发送邮件

        Args:
            to: 收件人邮箱地址（字符串或列表）
            subject: 邮件主题
            body: 邮件正文
            html: 是否为 HTML 格式
            cc: 抄送地址
            bcc: 密送地址
            attachments: 附件文件路径列表

        Returns:
            dict: {"success": bool, "message": str}
        """
        msg = MIMEMultipart()
        msg["From"] = f"{self.config.from_name} <{self.config.user}>"
        msg["Subject"] = subject

        # 处理收件人
        if isinstance(to, str):
            to = [to]
        msg["To"] = ", ".join(to)

        all_recipients = list(to)

        # 处理抄送
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            msg["Cc"] = ", ".join(cc)
            all_recipients.extend(cc)

        # 处理密送
        if bcc:
            if isinstance(bcc, str):
                bcc = [bcc]
            all_recipients.extend(bcc)

        # 添加正文
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(body, content_type, "utf-8"))

        # 添加附件
        if attachments:
            for file_path in attachments:
                path = Path(file_path)
                if path.exists():
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(path.read_bytes())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={path.name}",
                    )
                    msg.attach(part)

        try:
            server = self._create_connection()
            server.sendmail(self.config.user, all_recipients, msg.as_string())
            server.quit()
            return {"success": True, "message": f"邮件已成功发送至 {', '.join(to)}"}
        except smtplib.SMTPAuthenticationError as e:
            return {"success": False, "message": f"SMTP 认证失败: {e}"}
        except smtplib.SMTPException as e:
            return {"success": False, "message": f"SMTP 错误: {e}"}
        except Exception as e:
            return {"success": False, "message": f"发送失败: {e}"}

    def test_connection(self) -> dict:
        """测试 SMTP 连接"""
        try:
            server = self._create_connection()
            server.noop()
            server.quit()
            return {
                "success": True,
                "message": f"SMTP 连接成功！已登录: {self.config.user}",
            }
        except smtplib.SMTPAuthenticationError as e:
            return {"success": False, "message": f"SMTP 认证失败，请检查用户名和密码: {e}"}
        except smtplib.SMTPException as e:
            return {"success": False, "message": f"SMTP 连接错误: {e}"}
        except Exception as e:
            return {"success": False, "message": f"连接失败: {e}"}


if __name__ == "__main__":
    service = EmailService()
    result = service.test_connection()
    print(result)
