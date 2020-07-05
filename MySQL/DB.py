import pymysql

DB_Server = "DB Server"
# DB_Name = "zabbix"
User = "admin"
Password = "xxxxxxxxx"

print("Connecting to database...")

db = pymysql.connect(host=DB_Server, user=User, passwd=Password)

print("Succesfully Connected to database")

cur = db.cursor()

cur.execute('SHOW DATABASES')
print(cur.fetchall())

db.select_db("zabbix")

cur.execute('SHOW TABLES')
print(cur.fetchall())

db.close