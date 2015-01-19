import sqlite3
from flask import g

def queryTeachers(myname):
	conn = sqlite3.connect("dbase/hearstdata.db")
	c = conn.cursor()
	query='select distinct teacher from hearstmain'
	c.execute(query)
	results = [dict(teachername=row1[0]) for row1 in c.fetchall()]

	#results = [dict(myname=row[0], fname=row[1], srcname=row[2]) for row in c.fetchall()]
	conn.close()
	return results

def authTeachers(tup2):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	query='select count(distinct teacher) from loginclass where role = ? and login = ? and password = ?'
	c.execute('select count(distinct teacher) from loginclass where role = ? and login = ? and password = ?',tup2)
	results = [dict(countTeachers=row1[0]) for row1 in c.fetchall()]
	conn.close()
	if len(results)>0:
		return True
	else:
		return False

def addStudentToClass(teacher, student):
	coursewrok=queryCoursework(teacher)

	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	tup=(student, 'Student', coursewrok['classdesc'], teacher)
	c.execute('insert into usermap values (?,?,?,?)', tup)
	conn.commit()
	conn.close()
	return


def queryStudentForTeachers(myname):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	tup=('Student',myname)
	query='select distinct uname from usermap where role =? and mappedteacher = ?'
	c.execute('select distinct uname from usermap where role =? and mappedteacher = ?', tup)
	results = [dict(studname=row1[0]) for row1 in c.fetchall()]

	#results = [dict(myname=row[0], fname=row[1], srcname=row[2]) for row in c.fetchall()]
	conn.close()
	return results

def queryAll():
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	query='select * from hearstmain'
	c.execute(query)
	results = [dict(username=row[0], obj=row[1]) for row in c.fetchall()]
	conn.close()
	return results

def queryClassLogin(tuple1):
	#table loginclass (classname text not null,login text not null, passw text, mappedteacher text)
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	tup=('Student',myname)
	query='select distinct mappedteacher from loginclass where login =? and passw = ?'
	c.execute('select distinct uname from usermap where role =? and mappedteacher = ?', tuple1)
	results = [dict(tname=tuple1[0]) for row1 in c.fetchall()]
	tname1=results[0]['tname']
	result={'teachername': tname1, 'liststuds': []}
	result['liststuds']=queryStudentForTeachers(tname1)
	#results = [dict(myname=row[0], fname=row[1], srcname=row[2]) for row in c.fetchall()]
	conn.close()
	return result

def queryStudentLogin(tuple1):
	#table loginclass (classname text not null,login text not null, passw text, mappedteacher text)
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	login1,pass1=tuple1
	query=('select mappedteacher from loginclass where login =? and passw = ?',tuple1)
	print "queryyyyy",query
	c.execute('select mappedteacher from loginclass where login =? and passw = ?',tuple1)
	#print "--------",c.fetchall()
		#results = [dict(tname=tuple1[0]) for row1 in c.fetchall()]
	results = [dict(tname=row1[0]) for row1 in c.fetchall()]

	tname1=results[0]['tname']
	print "teachers name ======", results
	result={'teachername': tname1, 'liststuds': []}
	result['liststuds']=queryStudentForTeachers(tname1)
	conn.close()
	return result

def queryAllByUser(username):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	query='select * from hearstmain where username=' +"'"+ username +"'"
	c.execute(query)
	results = [dict(username=row[0], obj=row[1]) for row in c.fetchall()]
	conn.close()
	return results

def queryCoursework(teacher):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	tup=('student',teacher)
	c.execute('select distinct classname from loginclass where role =? and mappedteacher = ?', tup)
	results = []
	reulst_list = c.fetchall()
	if len(reulst_list) >=1 :
		results = {'classdesc' : reulst_list[0][0]} 
	conn.close()
	return results

def queryCourseworkByStudent(student):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()

	# query mappedteacher first
	tup1=('Student',student)
	c.execute('select mappedteacher from usermap where role =? and uname = ?', tup1)
	mappedteacher = c.fetchone()[0]

	# query coursework from the teacher
	tup2=('student', mappedteacher)
	c.execute('select distinct classname from loginclass where role =? and mappedteacher = ?', tup2)
	results = {'classdesc' : c.fetchone()[0]} 

	conn.close()
	return results

def updateCoursework(teacher, coursework):
	conn = sqlite3.connect("app/dbase/hearstdata.db")
	c = conn.cursor()
	tup=(coursework,teacher)
	c.execute('update loginclass set classname = ? where mappedteacher = ?', tup)
	conn.commit()
	conn.close()
	return

def addToSatchel(tup):
	try:
		conn = sqlite3.connect("app/dbase/hearstdata.db")
		c = conn.cursor()
		#teachername,studname,obid=objid
		#entries=('MRs Robin', 'Jinny', objid,'1','2')
		entries=( tup[0], tup[1])
		print "db:", entries
		query='insert into hearstmain values (?,?)'
		c.execute('insert into hearstmain values (?,?)',entries)
		conn.commit()
		conn.close()

	except Exception as e:
		print "ERROR", e
	
if __name__ == '__main__':
	queryAll()