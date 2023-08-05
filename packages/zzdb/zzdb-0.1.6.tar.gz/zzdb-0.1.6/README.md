[![Python application](https://github.com/AndreiPuchko/zzdb/actions/workflows/main.yml/badge.svg)](https://github.com/AndreiPuchko/zzdb/actions/workflows/main.yml)
# The light Python DB API wrapper with some ORM functions (MySQL, PostgreSQL, SQLite)
## Quick start (run demo files)
## - in docker:
```bash
git clone https://github.com/AndreiPuchko/zzdb && cd zzdb/database.docker
./up.sh
./down.sh
```  
## - on your system:
```bash
pip install zzdb
git clone https://github.com/AndreiPuchko/zzdb && cd zzdb
# sqlite:
python3 ./demo/demo.py
# mysql and postgresql:
pip install mysql-connector-python psycopg2-binary
pushd database.docker && docker-compose up -d && popd
python3 ./demo/demo_mysql.py
python3 ./demo/demo_postgresql.py
pushd database.docker && docker-compose down -v && popd
```
# Features:
 ---
## Connect
```python
from zzdb.db import ZzDb

database_sqlite = ZzDb("sqlite3", database_name=":memory:")
# or just
database_sqlite = ZzDb()


database_mysql = ZzDb(
    "mysql",
    user="root",
    password="zztest"
    host="0.0.0.0",
    port="3308",
    database_name="zztest",
)
# or just
database_mysql = ZzDb(url="mysql://root:zztest@0.0.0.0:3308/zztest")

database_postgresql = ZzDb(
    "postgresql",
    user="zzuser",
    password="zztest"
    host="0.0.0.0",
    port=5432,
    database_name="zztest1",
)
```
---
## Define & migrate database schema (ADD COLUMN only).
```python
zzdb.schema import ZzDbSchema

schema = ZzDbSchema()

schema.add(table="topic_table", column="uid", datatype="int", datalen=9, pk=True)
schema.add(table="topic_table", column="name", datatype="varchar", datalen=100)

schema.add(table="message_table", column="uid", datatype="int", datalen=9, pk=True)
schema.add(table="message_table", column="message", datatype="varchar", datalen=100)
schema.add(
    table="message_table",
    column="parent_uid",
    to_table="topic_table",
    to_column="uid",
    related="name"
)

database.set_schema(schema)
```
---
## INSERT, UPDATE, DELETE
```python
database.insert("topic_table", {"name": "topic 0"})
database.insert("topic_table", {"name": "topic 1"})
database.insert("topic_table", {"name": "topic 2"})
database.insert("topic_table", {"name": "topic 3"})

database.insert("message_table", {"message": "Message 0 in 0", "parent_uid": 0})
database.insert("message_table", {"message": "Message 1 in 0", "parent_uid": 0})
database.insert("message_table", {"message": "Message 0 in 1", "parent_uid": 1})
database.insert("message_table", {"message": "Message 1 in 1", "parent_uid": 1})

# this returns False because there is no value 2 in topic_table.id - schema works!
database.insert("message_table", {"message": "Message 1 in 1", "parent_uid": 2})


database.delete("message_table", {"uid": 2})

database.update("message_table", {"uid": 0, "message": "updated message"})
```
---
## Cursor
```python
cursor = database.cursor(table_name="topic_table")
cursor = database.cursor(
    table_name="topic_table",
    where=" name like '%2%'",
    order="name desc"
)
cursor.insert({"name": "insert record via cursor"})
cursor.delete({"uid": 2})
cursor.update({"uid": 0, "message": "updated message"})

cursor = database.cursor(sql="select name from topic_table")

for x in cursor.records():
    print(x)
    print(cursor.r.name)

cursor.record(0)['name']
cursor.row_count()
cursor.first()
cursor.last()
cursor.next()
cursor.prev()
cursor.bof()
cursor.eof()
```