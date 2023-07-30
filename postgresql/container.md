### 建立一個可連線的 PostgreSQL container

本篇會使用 psql 工具以 "postgres" 使用者身份連接到 PostgreSQL 伺服器。您可以在 CLI 中使用 SQL 命令和 PostgreSQL 操作。<br>
若您需要在容器內執行其他 PostgreSQL 相關操作，可以使用 docker exec 命令來執行您所需的命令<br>
當您建立一個可連線的 PostgreSQL container 時，以下是更詳細的步驟及一些補充資訊：<br>

#### Step 1: 下載 PostgreSQL 映像檔
首先，使用 docker pull 命令下載 PostgreSQL 映像檔。如果您已經下載過該映像檔，則可以跳過這個步驟。
```sh
# 先 pull image
$ docker pull postgres
```


#### Step 2: 建立 PostgreSQL Container
接下來，使用 docker create 或 docker run 命令建立一個 PostgreSQL Container。兩者的效果是相同的，您可以選擇其中一個方式來執行。<br>
使用 docker create 命令：<br>
```sh
# 建立 container，設定 port 號，設定 postgres 最高權限的登入密碼
$ docker create --name my-postgres -p 8080:5432 -e POSTGRES_PASSWORD=admin postgres
# --name my-postgres: 指定容器的名稱為 "my-postgres"，您可以自行更改名稱。
# -p 8080:5432: 將容器的 5432 Port 映射到主機的 8080 Port，這樣您可以透過主機的 8080 Port 來連接 PostgreSQL。
# -e POSTGRES_PASSWORD=admin: 設定 PostgreSQL 的最高權限使用者 "postgres" 的登入密碼為 "admin"，您可以自行更改密碼。
# 執行 container
$ docker start my-postgres
```

或者使用 docker run 命令：<br>
如果不想要分這麼步驟執行，也可以直接使用 docker run：<br>
```sh
$ docker run -d --name my-postgres -p 8080:5432 -e POSTGRES_PASSWORD=admin postgres
# -d: 以背景模式運行容器。
# 其他參數與 docker create 相同。
```


示範如何用 docker 建立一個可以連線的 PostgreSQL container。<br>
- 建立 container，使用 pull + create + start


#### Step 3: 啟動 PostgreSQL Container
執行以下命令來啟動 PostgreSQL Container：

```sh
$ docker start my-postgres
```

可以使用 docker ps 命令來檢查容器是否正在運行，以及它所使用的 Port 映射情況：
```sh
$ docker ps
```

若要進入正在運行的 PostgreSQL Container 的 bash 終端機，可以使用以下命令：
```sh
$ docker exec -it my-postgres bash
```

這將使您進入容器內部的 bash 終端機，讓您可以在容器中執行各種操作。但請注意，這只是一個 shell 終端，並不會自動連接到 PostgreSQL CLI。
若要在容器內部使用 PostgreSQL CLI，可以使用以下命令：
```sh
$ docker exec -it my-postgres psql -U postgres

# 這會使用 psql 工具以 "postgres" 使用者身份連接到 PostgreSQL 伺服器。您可以在 CLI 中使用 SQL 命令和 PostgreSQL 操作。
# 若要退出 PostgreSQL CLI，請輸入 \q 並按下 Enter 鍵。
# 若您需要在容器內執行其他 PostgreSQL 相關操作，可以使用 docker exec 命令來執行您所需的命令，就像前面的例子一樣。
```


- 其他維運指令

```sh
# 啟動一個可以操作的 bash 終端機非常簡單，只需要在尾端加上 bash 即可
$ docker exec -it CONTAINER bash
# 查看版本
$ docker exec my-postgres psql -V
```

---
接來來將手把手建立使用者、新增資料庫，甚至在這些資料庫中創建資料表。
隨著 PostgreSQL 容器日益成熟，您需要多個使用者以及特定權限，來管理不同的資料庫。首先，讓我們一起看看如何建立新的使用者並給予他們登入權限，並設置安全的密碼。

#### Step 5: 建立使用者 與 新增資料庫
```sh
# 僅需一個簡單的指令，我們建立使用者「mlaas」並設定了安全的登入密碼。
postgres=# create role mlaas with login password 'xxxx@1313';
CREATE ROLE
# 新增一個資料庫並將其指派給新建立的使用者
postgres=# create database mlaas owner mlaas;
CREATE DATABASE
```

這樣一來，「mlaas」資料庫已經建立並由使用者「mlaas」擁有。您現在擁有一個專屬的空間來儲存和管理您的資料。
當我們準備好我們的資料庫後，就該在其中建立資料表。資料表是關聯式資料庫的基本組成部分，它以列和欄的方式組織資料。以下是如何在「mlaas」資料庫中建立資料表的步驟：
```sh
postgres=# \c
You are now connected to database "postgres" as user "postgres".
postgres=# \c mlaas
You are now connected to database "mlaas" as user "postgres".
```


#### Step 6: 使用 CREATE TABLE 命令建新的資料表：
讓我們建立一個名為「customers」的資料表，包含「id」、「name」和「email」欄位：

```sh
CREATE TABLE table_name (
    column1 data_type1 constraints,
    column2 data_type2 constraints,
    ...
);
# 創建一个名為 "customers" 的表，包含 "id"、"name" 和 "email" 列：
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE
);
```

若要查看「mlaas」資料庫中所有的資料表，您可以使用「\dt」命令
```sh
# \dt 命令來查看資料庫中所有表的列表
mlaas=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner   
--------+-----------+-------+----------
 public | customers | table | postgres
(1 row)

# 或者，如果您只想查看特定表的詳細信息
\d table_name


mlaas-# \d customers
                                    Table "public.customers"
 Column |          Type          | Collation | Nullable |                Default                
--------+------------------------+-----------+----------+---------------------------------------
 id     | integer                |           | not null | nextval('customers_id_seq'::regclass)
 name   | character varying(100) |           | not null | 
 email  | character varying(255) |           |          | 
Indexes:
    "customers_pkey" PRIMARY KEY, btree (id)
    "customers_email_key" UNIQUE CONSTRAINT, btree (email)

```
#### Step 7: 調整權限 
最後，將資料表的所有權指派給相應的使用者非常重要。舉例來說，讓我們將「customers」資料表指派給「mlaas」使用者

```sh
mlaas=# ALTER TABLE customers OWNER TO mlaas;
ALTER TABLE
mlaas=# \dt
         List of relations
 Schema |   Name    | Type  | Owner 
--------+-----------+-------+-------
 public | customers | table | mlaas
(1 row)

```

太好了！「customers」資料表現在屬於「mlaas」使用者，確保正確的管理和存取控制

接下來用，可以開始放入一些 sample data
https://github.com/KellenJohn/ContainerLab/blob/main/postgresql/insert_to_db.py
#### Step 8: Insert Data
```python
import psycopg2

# 填入您的 PostgreSQL 容器連接訊息
db_host = "172.18.0.2"  # 或者您的容器的 IP 地址
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-postgres

"""
使用正确的主机和端口：默认情况下，PostgreSQL 容器将监听在本地主机（localhost）和默认端口 5432。
但是，由于在 Docker 容器中运行，可能需要使用容器的 IP 地址和相应的映射端口来连接。
"""
db_port = "5432"       # PostgreSQL 默認端口是 5432
db_name = "mlaas"      # 數據庫名稱
db_user = "mlaas"      # 連接數據庫的用户名
db_password = "xxxx@1313"  # 連接數據庫的密碼

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
```






