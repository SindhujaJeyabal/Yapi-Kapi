import sqlite3
from flask import g

def queryAllByUser(username):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	query='select * from hearstmain where username=' + 'Amy'
	c.execute(query)
	results = [dict(username=row[0], obj=row[1]) for row in c.fetchall()]
	conn.close()
	return results
	
def addTable(myname):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	
	querytoExec="create table hearstmain (username not null, obj not null);"
	c.execute(querytoExecs )
	conn.commit()
	conn.close()

def addMappingTable(myname):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	
	querytoExec="create table usermap (uname text not null,role text not null, classname text, mappedteacher text);"
	c.execute(querytoExec)
	conn.commit()
	conn.close()

def createClassLoginTable(myname):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	
	querytoExec="create table loginclass (classname text not null,role not null, login text not null, passw text, mappedteacher text);"
	c.execute(querytoExec)
	conn.commit()
	conn.close()

def addSatchelData(username,artifact_id):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	objtoadd =[(username,artifact_id)]

	query='insert into usermap values (?,?)'
	c.execute('insert into usermap values (?,?)',objtoadd)
	conn.commit()
	conn.close()

def addUserData():
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	objtoadd= [('John','Teacher','class','null'),('Amy','Student','class','John'),('Alice','Student','class','John'),('Mark','Student','class','John'), ('Ben','Student','class','John'),
				('Warren','Student','class','John'), ('Tim','Student','class','John'), ('Penny','Student','class','John'), ('Emily','Student','class','John'), ('Judith','Student','class','John'),
				('Diana','Student','class','John')]

	query='insert into usermap values (?,?,?,?)'
	c.executemany('insert into usermap values (?,?,?,?)',objtoadd)
	conn.commit()
	conn.close()

def addClassLogin():
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	objtoadd = [('class', 'teacher', 'teacher', 'yapikapi', 'John')]
	objtoadd = [('class', 'student', 'student','hearst','John')]
	c.executemany('insert into loginclass values (?,?,?,?,?)',objtoadd)
	conn.commit()
	conn.close()

def addToSatchel(tup):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	teachername,studname,obid=objid
	entries=( tup[0], tup[1])

	query='insert into hearstmain values (?,?)'
	c.execute('insert into hearstmain values (?,?)',entries)
	conn.commit()
	conn.close()

def qSatchel():
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	query2='select mappedteacher from loginclass where login =? and passw = ?'
	c.execute(query2,('student','hearst'))
	results = [dict(login=row[0]) for row in c.fetchall()]
	print results
	conn.close()

if __name__ == '__main__':
	# addTable("")
	# addMappingTable("")
	# createClassLoginTable("")
	# addUserData()conn.cursor()
	# qSatchel()
	#conn.close()
	#return results
	#addMappingTable("not")