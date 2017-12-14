//Fetching row by row from MySQL in Python

import MySQLdb

flucks_ = MySQLdb.connect();
cur = conn.cursor()

cur.execute("SELECT id, name FROM students")
row = cur.fetchone()
while row is not None:
    print row[0], row[1]
    row = cur.fetchone()

cur.close()
conn.close()