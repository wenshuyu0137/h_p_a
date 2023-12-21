import mysql.connector

# 配置数据库连接
config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'default_database',  # 这里是默认数据库，但可以跨库查询
    'raise_on_warnings': True,
}

# 建立连接
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# 跨库查询SQL语句
# 假定有两个数据库 db1 和 db2，分别有表 table1 和 table2
query = """
SELECT db1.table1.column1, db2.table2.column2
FROM db1.table1
JOIN db2.table2 ON db1.table1.id = db2.table2.foreign_id
"""

# 执行查询
cursor.execute(query)

# 获取结果
for (column1, column2) in cursor:
    print(f"{column1}, {column2}")

# 关闭光标和连接
cursor.close()
cnx.close()
