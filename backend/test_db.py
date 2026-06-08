import pymysql
import sys

HOST = "175.178.102.49"
PORT = 3306
USER = "wicmail"
PASSWORD = "DkDTbD2kxEkS7BwW"

def test_connection():
    try:
        print(f"正在连接 {USER}@{HOST}:{PORT} ...")
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, connect_timeout=10)
        print("✅ 连接成功！")

        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
            print(f"   MySQL 版本: {version}")

            cur.execute("SHOW DATABASES")
            dbs = [r[0] for r in cur.fetchall()]
            print(f"   数据库列表: {dbs}")

        conn.close()
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
