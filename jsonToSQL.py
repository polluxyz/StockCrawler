import psycopg2

try:
    # 連線到 PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        dbname="stockdb",
        user="postgres",
        password="450041",
        port="5432",
    )
    cur = conn.cursor()

    # 創建表格
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stock (
            symbol VARCHAR(10) PRIMARY KEY,  -- 股票代號
            name VARCHAR(100) NOT NULL       -- 股票名稱
        );
    """
    )

    conn.commit()
    print("✅ 表格 'stock' 建立成功！")

except psycopg2.Error as e:
    print("❌ 發生錯誤：", e)

finally:
    if "cur" in locals():
        cur.close()
    if "conn" in locals():
        conn.close()
