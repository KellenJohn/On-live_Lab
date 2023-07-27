### 建立一個可連線的 PostgreSQL container
示範如何用 docker 建立一個可以連線的 PostgreSQL container。
- 建立 container，使用 pull + create + start

```sh
# 先 pull image
$ docker pull postgres
# 建立 container，設定 port 號，設定 postgres 最高權限的登入密碼
$ docker create --name my-postgres -p 8080:5432 -e POSTGRES_PASSWORD=admin postgres
# 執行 container
$ docker start my-postgres
```

- 建立 container，使用 run
如果不想要分這麼步驟執行，也可以直接使用 docker run：
```sh
$ docker run -d --name my-postgres -p 8080:5432 -e POSTGRES_PASSWORD=admin postgres
```
- 維運指令
```sh
# 查看版本
$ docker exec my-postgres psql -V
# 查看當前存在的 Database Name
# 這裡會需要使用 psql 的 -U 參數來指定建立連線的使用者
$ docker exec my-postgres psql -U postgres -l

# 進入 PostgreSQL 的 CLI 命令列介面
# 這裡會使用 exec 的 -i 與 -t 參數，讓終端機保持開啟。當進入 PostgreSQL 後若想離開，則可輸入 「\q」即可。
$ docker exec -it my-postgres psql -U postgres
```


- 建立使用者 與 新增資料庫
```sh
postgres=# create role mlaas with login password 'xxxx@1313';
CREATE ROLE
postgres=# create database mlaas owner mlaas;
CREATE DATABASE

postgres=# \c
You are now connected to database "postgres" as user "postgres".
postgres=# \c mlaas
You are now connected to database "mlaas" as user "postgres".

mlaas=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner   
--------+-----------+-------+----------
 public | customers | table | postgres
(1 row)

mlaas=# ALTER TABLE customers OWNER TO mlaas;
ALTER TABLE
mlaas=# \dt
         List of relations
 Schema |   Name    | Type  | Owner 
--------+-----------+-------+-------
 public | customers | table | mlaas
(1 row)

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





