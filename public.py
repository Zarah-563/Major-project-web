from flask import *
from database import *
import uuid
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template("index_new.html")


@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
		res=select(q)
		print(res)
		if not res:
			flash('INCORRECT USERNAME OR PASSWORD')
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				flash('WELCOME ADMIN')
				return redirect(url_for("admin.admin_home"))
			
			if res[0]['usertype']=='user':
				q="SELECT * FROM `users` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				if res2:
					session['id']=res2[0]['user_id']
					flash('WELCOME TO USERS HOME')
					return redirect(url_for("user.user_home"))
				
			if res[0]['usertype']=='doctor':
				print("klkkkkkkkkkkkkkkkkkkklklllllllllllll")
				q="SELECT * FROM `doctor` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				print(res2)
				if res2:
					session['doctor_id']=res2[0]['doctor_id']
					flash('WELCOME TO DOCTOR HOME')
					return redirect(url_for("doctors.doctor_home"))

	return render_template('login.html')



@public.route('/user_Register',methods=['get','post'])
def user_Register():
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phno=request.form['phno']
		email=request.form['email']
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
		res=select(q)
		if res:
			flash('USER NAME ALREADY EXIST')
			return redirect(url_for('public.user_Register'))
		else:
			q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES ('%s','%s','user')"%(uname,pwd)
			id=insert(q)
			q="INSERT INTO `users`(`login_id`,`firstname`,`lastname`,`place`,`phone`,`email`) VALUES ('%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phno,email)
			insert(q)
			# flash('REGISTERED')
		return """<script>alert('Registered Succesfully');window.location='/login'</script>"""
	return render_template('user_Register.html')


@public.route('/doctorreg' ,methods=['post','get'])
def doctorreg():
	if 'submit' in request.form:
		firstname=request.form['fname']
		lastname=request.form['lname']
		place=request.form['place']
		email=request.form['email']
		phno=request.form['phone']
		username=request.form['username']
		password=request.form['password']

		q="insert into login values(null,'%s','%s','doctor')"%(username,password)
		lid=insert(q)
		q="insert into doctor values(null,'%s','%s','%s','%s','%s','%s')"%(lid,firstname,lastname,place,phno,email)
		insert(q)
		return """<script>alert('Registered Succesfully');window.location='/login'</script>"""

	return render_template('doctorreg.html')
