import mysql.connector

password=''
database='skin_disease'

def select(q):
	cnx=mysql.connector.connect(user='root',host='localhost',password=password,database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	result=cur.fetchall()
	cnx.close()
	cur.close()
	return result

def delete(q):
	cnx=mysql.connector.connect(user='root',host='localhost',password=password,database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.rowcount
	cnx.close()
	cur.close()
	return result

def update(q):
	cnx=mysql.connector.connect(user='root',host='localhost',password=password,database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.rowcount
	cnx.close()
	cur.close()
	return result

def insert(q):
	cnx=mysql.connector.connect(user='root',host='localhost',password=password,database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.lastrowid
	cur.close()
	cnx.close()
	return result
