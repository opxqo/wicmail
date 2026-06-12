import pymysql
import sys
import os

HOST = os.getenv("DB_HOST", "your-database-host")
PORT = int(os.getenv("DB_PORT", "3306"))
USER = os.getenv("DB_USER", "your-username")
PASSWORD = os.getenv("DB_PASSWORD", "your-password")

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
