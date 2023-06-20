import psycopg2

# 连接到 Cloud SQL 实例
connection = psycopg2.connect(
            host='/cloudsql/cncf',
            user='postgres',
            password='pMJMn3`yOtCmV>he',
            dbname='demo'
)

# 创建游标对象
cursor = connection.cursor()

# 执行 INSERT 语句插入数据
insert_query = "INSERT INTO demo (id, name, number) VALUES (%s, %s, %s)"

# 示例数据
data = [
    (1, 'John', 123),
    (2, 'Emma', 456),
    (3, 'Mike', 789)
]

# 插入数据
cursor.executemany(insert_query, data)

# 提交更改
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()
