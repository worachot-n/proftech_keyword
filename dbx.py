import mysql.connector
import configure as conf

def query(sqlx):
    mydb = mysql.connector.connect(host=conf.hostdb,
    user=conf.userdb,
    password=conf.passworddb,
    database=conf.dbname)
    mycursor = mydb.cursor()
    mycursor.execute(sqlx)
    rows = mycursor.fetchall()
    mydb.disconnect()
    return rows

def update(sqlx):
    countReturn=0
    mydb = mysql.connector.connect(host=conf.hostdb,
    user=conf.userdb,
    password=conf.passworddb,
    database=conf.dbname)
    mycursor = mydb.cursor()
    mycursor.execute(sqlx)
    mydb.commit()
    countReturn=mycursor.rowcount
    mydb.disconnect()
    return countReturn

def updatepara(sqlx,para):
    countReturn=0
    mydb = mysql.connector.connect(host=conf.hostdb,
    user=conf.userdb,
    password=conf.passworddb,
    database=conf.dbname)
    mycursor = mydb.cursor()
    mycursor.execute(sqlx,para)
    mydb.commit()
    countReturn=mycursor.rowcount
    mydb.disconnect()
    return countReturn

def updatepara_multi(sqlx,paras):
    countReturn=0
    mydb = mysql.connector.connect(host=conf.hostdb,
    user=conf.userdb,
    password=conf.passworddb,
    database=conf.dbname)
    mycursor = mydb.cursor()
    mycursor.executemany(sqlx,paras)
    mydb.commit()
    countReturn=mycursor.rowcount
    mydb.disconnect()
    return countReturn

# data = [
#   ('Jane', date(2005, 2, 12)),
#   ('Joe', date(2006, 5, 23)),
#   ('John', date(2010, 10, 3)),
# ]
# stmt = "INSERT INTO employees (first_name, hire_date) VALUES (%s, %s)"
# cursor.executemany(stmt, data)