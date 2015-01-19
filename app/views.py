from flask import render_template,request,session,redirect
from flask import url_for
from app import app
from libs import api
import dbHandler
import satchelHandler

def auth():
	if (session['username']!=""):
		return
	else:
		return redirect(url_for('main'))


@app.route('/', methods=['GET', 'POST'])
def index():
	if 'username' in session:
		#return 'Logged in as %s' %session['username']		
		return redirect(url_for('main'))

	if request.method == 'POST':
		cl1= request.form['uname']
		pw1 = request.form['pword']
		tup1=('teacher',cl1,pw1)
		session['username']=cl1

		# TODO : Authentication!!!
		#l1=satchelHandler.authTeacher(tup1)
		l1 = True
		if(l1==False):
			return render_template('studentform.html',fail="Not Found ... !")
		else:
			session['teachername']=cl1
			#studlist=satchelHandler.queryStudentForTeachers(cl1)
			studlist=dbHandler.queryStudentForTeachers(cl1)
			coursewrok=dbHandler.queryCoursework(cl1)
			return redirect(url_for('classAdminRender'))
		return redirect(url_for('main'))	
	#return redirect(url_for('login'))
	return render_template('landingpage.html')


@app.route('/debug')
def debug():
	#return "Static URL"+url_for('static', filename='css/bootstrap.min.css')
	return app.config['DATABASE']+apis.printme()

@app.route('/artifacts.html/<tribename>')
def queryAllArtifactsForTribe(tribename):
	# show the user profile for that user
	if(tribename==""):
		return "No tribe selected"
	print "view: getting artifacts for tribe: ", tribename
	newTribe=tribename.replace("ZZZZZ", " ")
	artifact_tribes, category_tribes = api.get_artifacts_category_for_tribe(newTribe)
	print type(artifact_tribes), len(artifact_tribes), type(artifact_tribes[0])
	print type(category_tribes), len(category_tribes), type(category_tribes[0])
	
	categ_arts = dict()
	link_categ = list()
	for categ in category_tribes:
		categ_arts[categ] = [arty for arty in artifact_tribes if categ in arty['objfilecode_ss']]
		categ_copy = categ[:]
		categ_copy=categ_copy.replace(" ", "ZZZZZ")
		link_categ.append(categ_copy)
		
	#print categ_arts
	return render_template('artifacts.html',artifact_list=categ_arts, category_list=category_tribes, tribe_name = newTribe, link_tribename= tribename,link_categlist=link_categ, total_count=len(artifact_tribes))

@app.route('/artifact-category.html/<tribename>/<categoryname>')
def queryAllArtifactsForCategoryinTribe(tribename,categoryname) :
	# show the user profile for that user
	if(tribename==""):
		return "No tribe selected"
	newTribe=tribename.replace("ZZZZZ", " ")
	newCateg=categoryname.replace("ZZZZZ", " ")
	artifacts_category = api.get_artifacts_tribe_category(newTribe, newCateg)
	return render_template('artifact-category.html',artifact_list=artifacts_category, categ_name = newCateg, tribe_name = newTribe, count = len(artifacts_category))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('main'))
	return render_template('landingpage.html')

@app.route('/guestlogin', methods=['GET', 'POST'])
def loginGuest():
	session['username'] = "guest"
	return redirect(url_for('main'))

@app.route('/homepage.html')
def main():
	return render_template('homepage.html', name=session['username'])


@app.route('/satchel.html')
def satrender():
    satchelContents = satchelHandler.querySatchel()
    coursework = satchelHandler.queryCourseworkForStudent(session['username'])
    count = len(satchelContents)
    objectList = []
    for item in satchelContents:
        print "item in satchel",item
        print "CALLING ARTIFACT LIST"
        obj = api.getArtifactById(item['obj'])
        print type(obj[0])
        objectList.append(obj[0])
    return render_template('satchel.html', name=session['username'], count=count, artifactList=objectList, coursework=coursework)

@app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username

@app.route('/addtosatchel/<objid>')
def satchelAdd(objid):
	# This is going to add objid to the current requestor
	satchelHandler.addToSatchel(objid)
	return "Success !!!!"

@app.route('/queryAll')
def queryAll():
	# show the user profile for that user
	mylist=[]
	mylist=satchelHandler.querySatchel()
	str1="wow"
	for myelement in mylist:
		str1=str1+myelement['teachername']
	return str1

@app.route('/viewSatchel/<studname>')
def viewSatchelForStudent(studname):
	# show the user profile for that user
	mylist=[]
	satchelContents=satchelHandler.querySatchelForStudent(studname)
	count = len(satchelContents)
	objectList = []
	for item in satchelContents:
		print "item in satchel",item
		print "CALLING ARTIFACT LIST"
		obj = api.getArtifactById(item['obj'])
		print type(obj[0])
		objectList.append(obj[0])
	return render_template('studentssatchel.html', name=studname, count=count, artifactList=objectList)

@app.route('/artifact-category.html/<tribename>')
def queryAll1Artifacts(tribename):
	artifact_list=api.get_all_artifacts(tribename)
	count = len(artifact_list)
	# show the user profile for that user
	return render_template('artifact-category.html',artifact_list=artifact_list,count=count)

@app.route('/logout')
def terminate():
	# remove the username from the session if it's there
	session.pop('username', None)
	session.pop('teachername', None)

	return redirect(url_for('index'))

@app.route('/studentlogin', methods=['GET', 'POST'])
def studlogin():
	if request.method == 'POST':
		print "form control"
		cl1= request.form['classname']
		pw1 = request.form['password1']
		print "form req"
		tup1=(cl1,pw1)
		print "wow",tup1
		l1=satchelHandler.getStudentLogin(tup1)
		print "list of studs", l1
		if(l1 is None):
			return render_template('studentform.html',fail="Not Found ... !")
		else:
			session['teachername']=l1['teachername']
			return render_template('choosename.html',studlist=l1['liststuds'])
		return redirect(url_for('main'))
	return render_template('studentform.html')

@app.route('/studentrender/<studlogin>')
def studentRender(studlogin):
	if 'teachername' in session:
		session['username']= studlogin
		return redirect(url_for('main'))
	else:
		return redirect(url_for('fail'))
	return render_template('teacherform.html')

@app.route('/classadmin', methods=['GET', 'POST'])
def classAdminRender():
	if 'teachername' in session:
		cl1=session['teachername']

		if request.method == 'POST':
			coursework= request.form.get('coursework')
			added_student = request.form.get('student-added')
			if coursework != None:
				print 'coursework:'+coursework
				dbHandler.updateCoursework(cl1, coursework)
			elif added_student != None:
				dbHandler.addStudentToClass(cl1, added_student)

		student_list=dbHandler.queryStudentForTeachers(cl1)
		coursewrok=dbHandler.queryCoursework(cl1)

		return render_template('classadmin.html', student_list = student_list, coursewrok = coursewrok)
	else:
		return redirect(url_for('fail'))	

@app.route('/fail')
def fail():
	return render_template('fail.html')
