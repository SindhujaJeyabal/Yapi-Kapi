import dbHandler


def querySatchel():
	try:
		listall=[]
		listall=dbHandler.queryAll()
		print type(listall)
	except Exception as e:
		return e
querySatchel()
mylist=[]
mylist=dbHandler.queryAll()
str1="wow"
for strin in mylist:
	print type(strin)
	str1=str1+strin['teachername']
print str1