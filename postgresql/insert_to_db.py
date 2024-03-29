import psycopg2

# 填入您的 PostgreSQL 容器連接訊息
db_host = "IP???"  # 或者您的容器的 IP 地址
# 如果是用 GCP/AWS Cloud Shell 用容器啟用的
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-postgres

"""
使用正确的主机和端口：默认情况下，PostgreSQL 容器将监听在本地主机（localhost）和默认端口 5432。
但是，由于在 Docker 容器中运行，可能需要使用容器的 IP 地址和相应的映射端口来连接。
"""
db_port = "5432"       # PostgreSQL 默認端口是 5432
db_name = "mlaas"      # 數據庫名稱
db_user = "mlaas"      # 連接數據庫的用户名
db_password = "xxxx@8787"  # 連接數據庫的密碼

# 數據庫連接配置
conn_config = {
    "host": db_host,
    "port": db_port,
    "dbname": db_name,
    "user": db_user,
    "password": db_password
}

# 插入的數據列表
data_to_insert = [
    (1, "John", "john@example.com"),
    (2, "Alice", "alice@example.com"),
    (3, "Bob", "bob@example.com"),
    # 添加更多行...
]

try:
    # 連接到數據庫
    conn = psycopg2.connect(**conn_config)

    # 創建一個 cursor
    cursor = conn.cursor()

    # 執行插入數據的 SQL 語句
    for data in data_to_insert:
        cursor.execute("INSERT INTO customers (id, name, email) VALUES (%s, %s, %s);", data)

    # 提交事務
    conn.commit()

    print("成功插入數據到 customers 表！")

except (Exception, psycopg2.Error) as error:
    print("連接或插入數據時出錯:", error)

finally:
    # close cursor 和連接
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
