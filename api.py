from flask import *
from database import *
import uuid
from cnn_predict import predict
import os

api=Blueprint('api',__name__)

@api.route('/login')
def login():
    data={}
    uname=request.args['username']
    pwd=request.args['password']
    query="select * from login where username='%s' and password='%s'"%(uname,pwd)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    data['methods']="login"
    print(data,"<<<<<<<<<")
    return str(data)


@api.route('/view_remedy')
def view_remedy():
    data={}
    login_id=request.args['login_id']
    query="select * from remady where user_id=(select user_id from users where login_id='%s')"%(login_id)
    print(query)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    # data['method']="ViewProfile"
    return str(data)


@api.route('/view_doctor')
def view_doctor():
    data={}
    # doctor_id=request.args['doctor_id']
    query="select * from doctor"
    print(query)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    # data['method']="ViewProfile"
    return str(data)



@api.route('/upload_photo',methods=['post'])
def upload_photo():
    data={}
    lid=request.form['lid']
    image=request.files['image']
    path="static/uploads/"+str(uuid.uuid4())+image.filename
    
    image.save(path)
    result, cancer_result=predict(path)
    
    
    if cancer_result:
        out="Result :  "+result+"  \nCancer Result :  "+cancer_result
    else:
        out="Result :  "+result+"  \n No Cancer "
    
  
    
    w="insert into prediction values(null,(select user_id from users where login_id='%s'),'%s','%s',curdate())"%(lid,path,out)
    resq=insert(w)
    if resq:
        return jsonify(method="viewoutput",status="true",data=out)
    else:
        return jsonify(method="viewoutput",status="false")
@api.route('/viewoutput',methods=['get'])
def viewoutput():
    data={}
    lid=request.args['lid']
    q="select * from prediction where user_id=(select user_id from users where login_id='%s')"%(lid)
    res=select(q)
    if res:
        return jsonify(method="viewoutput",status="true",data=res)
    else:
        return jsonify(method="viewoutput",status="false")




@api.route('/send_enquiry_view_reply',methods=['post','get'])
def send_enquiry_view_reply():
    data={}
    user_id=request.args['user_id']
    docid=request.args['doctor']

 
    print(user_id,'///////////////')
    enquiry=request.args['enquiry']
 
    query1="insert into enquiry values (null,'%s','%s',curdate(),'pending','%s')"%(user_id,enquiry,docid)
    print(query1)
    log=insert(query1)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    data['methods']='send_enquiry_view_reply'
    return str(data)


@api.route('/view_reply')
def view_reply():
    data={}
    # doctor_id=request.args['doctor_id']
    query="select * from enquiry"
    print(query)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    data['methods']="view_reply"
    return str(data)

@api.route('/sub_view_doctor')
def sub_view_doctor():
    data={}
    # doctor_id=request.args['doctor_id']
    query="select * from doctor"
    print(query)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    data['methods']="sub_view_doctor"
    return str(data)
@api.route('/rating')
def rating():
    data={}


    lid=request.args['lid']
    reviews=request.args['reviews']
    rate=request.args['rate']
    # date=request.args['date']


    query1="insert into rating values (null,(select user_id from users where login_id='%s'),'%s','%s',curdate())"%(lid,reviews,rate)
    # query1="insert into program values (null,'%s','%s')"%(title,date)

    print(query1)
    log=insert(query1)
    print(log)

    if log:
        data['status']='success'
    else:
        data['status']='failed'
    # data['method']="ViewProfile"
    return str(data)



@api.route('/view_fee_amount')
def view_fee_amount():
    data={}
    # user_id=request.args['user_id']
    # query="select * from appointment where user_id='%s'"%(user_id)
    query="select * from appointment"
    print(query)
    log=select(query)
    print(log)

    if log:
        data['status']='success'
        data['data']=log
    else:
        data['status']='failed'
    # data['methods']="view_reply"
    return str(data)

@api.route('/payment')
def payment():
    data={}

    logid=request.args['appointment_id']
    doctor_id=request.args['doctor_id']
    # logid=request.args['logid']
    # query1="update appointment set appoin_status='Appointment Fixed' where appointment_id='%s'"%(appointment_id)
    

    q2="insert into appointment values(null,(select user_id from users where login_id='%s'),'%s',curdate(),'pending','500')"%(logid,doctor_id)
    print(q2)  
    id=insert(q2)

    query1="insert into payment values (null,'%s',500,curdate())"%(id)
    print(query1)
    insert(query1)
    
    data['status']='success'
    
    # data['method']="ViewProfile"
    return str(data)


@api.route('/signup',methods=['GET','POST'])
def signup():
    data={}
    
    fname=request.args['firstname']
    place=request.args['place']
    phno=request.args['phonenumber']
    email=request.args['email']
    username=request.args['username']
    password=request.args['password']
    
    u="insert into login values(null,'%s','%s','user')"%(username,password)
    log=insert(u)
    i="insert into users values (null,'%s','%s','null','null','null','','%s','%s','%s','%s')"%(log,fname,'',place,phno,email)
    res=insert(i)
    if res:
        data['status']="success"
        data['data']=res
        print('success')
    else:
        data['status']="failed"
        print('fail')
    return str(data)



@api.route('/view_nearby_doctors')
def view_nearby_doctors():
    data={}

    lid=request.args['lid']
    query1="select * from doctors where place like ='%s'"%(lid)

    print(query1)
    update(query1)
    
    data['status']='success'
    
    # data['method']="ViewProfile"
    return str(data)



@api.route('/view_doctors')
def view_doctors():
    data={}

    # lid=request.args['lid']
    place=request.args['place']
    query1="select * from doctor where place like '%s'"%(place)
    print(query1)
    res=select(query1)
    
    data['status']='success'
    
    data['data']=res
    return str(data)



@api.route('/sort_by_top_rate')
def sort_by_top_rate():
    data={}

    # lid=request.args['lid']
    place=request.args['place']
    query1="select * from doctor order by rate '%s'"%(place)
    print(query1)
    res=select(query1)
    
    data['status']='success'
    
    data['data']=res
    return str(data)