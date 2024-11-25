import pymysql
import pandas as pd
import random
# con = pymysql.connect(host='localhost', user='mysql_user_id', password='_password_',
#                        db='access_db', charset='utf8') # 한글처리 (charset = 'utf8')

con = pymysql.connect(host='localhost', user='root', password='root',
                       db='testt', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()
 
# STEP 4: SQL문 실행 및 Fetch

i = 124
q = str(i)
cur = con.cursor()
sql = "INSERT INTO testtable (V) VALUES (%s)"
cur.execute(sql, q)
con.commit()

# 데이타 Fetch
rows = cur.fetchall()
print(rows)     # 전체 rows

# STEP 5: DB 연결 종료
con.close()


# con = pymysql.connect(host='localhost', user='testuser', password='YES',
#                       db='ttest', charset='utf8', # 한글처리 (charset = 'utf8')
#                       autocommit=True, # 결과 DB 반영 (Insert or update)
#                       cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
#                      )
# cur = con.cursor()

# sql = "SELECT * FROM customers" # customers 테이블 전체를 불러옴
# cur.execute(sql)
# rows = cur.fetchall()
# con.close() # DB 연결 종료
# print(rows)