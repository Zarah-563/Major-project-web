from flask import *
from database import*

doctors=Blueprint('doctors',__name__)


@doctors.route('/doctor_home')
def doctor_home():
	data={}
	p="select*from doctor where doctor_id='%s'"%(session['doctor_id'])
	res=select(p)
	data['docinfo']=res
	return render_template('doctor_home.html')


@doctors.route('/doctor_view_enquiry',methods=['get','post'])
def doctor_view_enquiry():
	data={}
	p="SELECT * FROM `enquiry` INNER JOIN `users` on enquiry.user_id=users.login_id where doctor_id='%s'"%(session['doctor_id'])
	eres=select(p)
	print("kkkkkkkkkkkkkkkkkkkkkkkkkkkk",p)
	data['enquiry']=eres

	if 'action' in request.args:
		action=request.args['action']
		eid=request.args['id']
	else:
		action=None


	if action=="update":
		q="select * from enquiry where equiry_id='%s'"%(eid)
		res=select(q)
		data['up']=res

	if 'update' in request.form:
		reply=request.form['reply']
		q="update enquiry set enq_reply='%s' where equiry_id='%s'"%(reply,eid)
		update(q)
		return redirect(url_for('doctors.doctor_view_enquiry'))

	return render_template('doctor_view_enquiry.html',data=data)

@doctors.route('/doctor_view_appointment')
def doctor_view_appointment():
	data={}
	# p="SELECT * FROM `users` INNER JOIN `prediction` USING(`user_id`) INNER JOIN `appointment` USING (`user_id`) INNER JOIN `payment` USING(`appointment_id`)  WHERE `appointment`.`doctor_id`='%s' GROUP BY `appointment_id`"%(session['doctor_id'])

	p="SELECT * FROM `users` INNER JOIN `prediction` ON USERS.user_id=prediction.user_id INNER JOIN `appointment` ON appointment.user_id=users.user_id where  appointment.doctor_id='%s'"%(session['doctor_id'])
	print(p)
	ares=select(p)
	data['view']=ares

	return render_template('doctor_view_appointment.html',data=data)

@doctors.route('/doctor_add_remady',methods=['get','post'])
def doctor_add_remady():
	data={}
	appointment_id=request.args['appointment_id']
	user_id=request.args['user_id']
	if 'submit' in request.form:
		remady=request.form['remady']
		q="INSERT INTO `remady` VALUES(NULL,'%s','%s','%s')"%(appointment_id,remady,user_id)
		insert(q)
	if 'action' in request.args:
		action=request.args['action']
		remady_id=request.args['remady_id']
	else:
		action=None

	if action=='remove':
		q="DELETE FROM `remady` WHERE `remady_id`='%s'"%(remady_id)
		delete(q)

	q="SELECT * FROM `remady` WHERE `appointment_id`='%s'"%(appointment_id)
	data['view']=select(q)
	return render_template('doctor_add_remady.html',appointment_id=appointment_id,user_id=user_id,data=data)
# @doctors.route('/replyenquiry')
# def replyenquiry():
# 	data={}
# 	x="select * from enquiry"
# 	res=select(x)
# 	data['enquiry']=res


# 		

# 	return render_template('.html',data=data)