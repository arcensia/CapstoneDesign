import pymysql


con = pymysql.connect(host='localhost', user='root', password='',
                       db='TESTDB', charset='utf8')

# STEP 3: 
cur = con.cursor()
 
# STEP 4
sql = "SELECT * FROM Bsensertable"
cur.execute(sql)
 

rows = cur.fetchall()
print(rows)


con.close()
