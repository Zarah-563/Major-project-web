from flask import *
from database import *
import uuid
admin=Blueprint('admin',__name__)

@admin.route('/admin_home',methods=['get','post'])
def admin_home():
	if not session.get("lid") is None:
		data={}
		return render_template("admin_home.html",data=data)
	else:
		return redirect(url_for('public.login'))




@admin.route('/admin_View_predicted_output',methods=['get','post'])
def admin_View_predicted_output():
	data={}
	q="SELECT *,users.firstname AS `user` FROM `prediction` INNER JOIN `users` USING (`user_id`) ORDER BY `prediction_id` DESC"
	data['pre']=select(q)
	return render_template("admin_View_predicted_output.html",data=data)




@admin.route('/admin_View_rating',methods=['get','post'])
def admin_View_rating():
	data={}
	q="SELECT *,users.firstname AS `user` FROM `rating` INNER JOIN `users` USING (`user_id`) ORDER BY `rating_id` DESC"
	data['rate']=select(q)
	return render_template("admin_View_rating.html",data=data)


@admin.route('/admin_view_appointment',methods=['get','post'])
def admin_view_appointment():

	data={}
	q="SELECT * FROM `appointment` INNER JOIN `users` USING(`user_id`) ORDER by appoin_date asc"
	print(q)
	data['view']=select(q)

	if 'action' in request.args:
		action=request.args['action']
		appointment_id=request.args['appointment_id']
	else:
		action=None

	if action=='accept':
		q="UPDATE `appointment` SET `appoin_status`='accept your appoinment' WHERE `appointment_id`='%s' "%(appointment_id)
		print(q)
		update(q)
		return redirect(url_for('admin.admin_view_appointment'))
	
	return render_template('admin_view_appointment.html',data=data)




@admin.route('/admin_view_bookingdetails')
def admin_view_bookingdetails():
	data={}
	p="SELECT * FROM `users` INNER JOIN `prediction` USING(`user_id`) INNER JOIN `appointment` USING (`user_id`) INNER JOIN `doctor` USING (`doctor_id`)  INNER JOIN `payment` USING(`appointment_id`)  GROUP BY `appointment_id`"
	ares=select(p)
	data['view']=ares

	return render_template('admin_view_bookingdetails.html',data=data)

@admin.route('admin_view_doctors',methods=['get','post'])
def admin_view_doctors():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None

	if action=='delete':
		q="DELETE FROM `login` WHERE `login_id`='%s'"%(login_id)
		delete(q)
		q="DELETE FROM `doctor` WHERE `login_id`='%s'"%(login_id)
		delete(q)

	q="SELECT * FROM  `doctor`"
	data['view']=select(q)
	return render_template('admin_view_doctors.html',data=data)

@admin.route('admin_view_users',methods=['get','post'])
def admin_view_users():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None

	if action=='delete':
		q="DELETE FROM `login` WHERE `login_id`='%s'"%(login_id)
		delete(q)
		q="DELETE FROM `users` WHERE `login_id`='%s'"%(login_id)
		delete(q)


	q="SELECT * FROM  `users`"
	data['view']=select(q)
	return render_template('admin_view_users.html',data=data)






























