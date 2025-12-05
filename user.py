from flask import *
from database import *
from predict import *
from newcnn import *
import uuid

users=Blueprint("user",__name__)

@users.route('/user')
def userpage():
    if 'log' in session:
        response = make_response(render_template("userhome.html"))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("userhome.html") 

@users.route('/sendcomplaint',methods=['post','get'])
def send_complaint():
    if 'log' in session:
        data={} 
        c="select * from complaint"
        data['view']=select(c)  
        if 'submit' in request.form:
            comp=request.form['Complaint']
            a="insert into complaint values(null,'%s','%s','pending',curdate())"%(session['log'],comp)
            ins =insert(a)
            print(ins)
            return "<script>alert('Send Complaint');window.location='/sendcomplaint'</script>"   
        response = make_response(render_template("sendcomplaint.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("sendcomplaint.html",data=data)




# @users.route('/viewcertificate',methods=['post','get'])
# def view_certificate():
#     if 'log' in session:
#         data={} 
#         c="select * from certificate"
#         data['view']=select(c) 
#         if 'submit' in request.form:
#             certificate=request.form['file']
#         response = make_response(render_template("view_certificate.html",data=data))
#     else:
#         response = make_response("""
#             <script>
#                 alert('Session Expired');
#                 window.location.href = '/';
#             </script>
#         """)
    
#     # Set headers to prevent caching
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response
#     return render_template("view_certificate.html",data=data)



@users.route('/user_view_scrap',methods=['post','get'])
def user_view_scrap():
    if 'log' in session:
        data={}
        c="select * from scrap"
        data['view']=select(c) 
        response = make_response(render_template("user_view_scrap.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("user_view_scrap.html",data=data)

@users.route('/sendrating',methods=['post','get'])
def send_rating():
    if 'log' in session:
        id=request.args['id']
        data={} 
        c="select * from rating where user_id='%s'"%(session['log'])
        data['view']=select(c) 
        if 'submit' in request.form:
            rating=request.form['rating']
            a="insert into rating values(NULL,'%s','%s','%s',curdate())"%(session['log'],id,rating)
            ins =insert(a)
            print(ins)
            return "<script>alert('Sucessfully Submitted');window.location='/user'</script>"  
        response = make_response(render_template("sendrating.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("sendrating.html",data=data)


@users.route('/view_user_profile',methods=['post','get'])
def view_user_profile():
    if 'log' in session:
        data={}
        c="select * from user where user_id='%s'"%(session['user'])
        data['view']=select(c) 

        if 'action' in request.args:
            action=request.args['action']
            if action =='update':
                qry="select * from user where user_id='%s'"%(session['user'])
                data['up']=select(qry) 

                if 'submit' in request.form:
                        fname=request.form['fname']
                        lname=request.form['lname']
                        place=request.form['place']
                        post=request.form['post']
                        pincode=request.form['pin']
                        phno=request.form['phonenumber']
                        email=request.form['email']
                        up_qry="update user set f_name='%s',l_name='%s',place='%s',post='%s',pin='%s',phone='%s',email='%s'where user_id='%s'"%(fname,lname,place,post,pincode,phno,email,session['user'])
                        update(up_qry)
        response = make_response(render_template("userprofile.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    
    return render_template("userprofile.html",data=data)


@users.route('/sendrequest',methods=['post','get'])
def send_request():
    if 'log' in session:
        sid=request.args['id']
        data={} 
        c="select * from my_vehicle inner join vehicle using(vehicle_id) where user_id='%s'"%(session['user'])
        data['view']=select(c) 
        if 'action' in request.args:
            action=request.args['action']
            m_id=request.args['mid']
            if action =='send':
                a="insert into scarprrequest values(NULL,'%s','pending','%s')"%(m_id,sid)
                ins =insert(a)
                print(ins)
            return"<script>alert('Sucessfully Submitted');window.location='/user_view_scrap'</script>"  
        response = make_response(render_template("sendrequest.html",data=data,sid=sid))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("sendrequest.html",data=data,sid=sid)


@users.route('/view_scrapreq_status',methods=['post','get'])
def view_scrapreq_status():
    if 'log' in session:
        data={}
        c="""SELECT 
            scarprrequest.status AS requeststatus,request_id,
            my_vehicle.*, 
            vehicle.* 
        FROM `scarprrequest`
        INNER JOIN `my_vehicle` USING(my_vehicle_id) 
        INNER JOIN `vehicle` USING(vehicle_id) 
        WHERE user_id ='%s'"""%(session['user'])
        data['view']=select(c)
        response = make_response(render_template("view_scrapreq_status.html",data=data))

    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("view_scrapreq_status.html",data=data)

@users.route('/view_own_vehicle',methods=['post','get'])
def view_own_vehicles():
    if 'log' in session:
        data={}
        c="select * from vehicle"
        data['view']=select(c)
        if 'action' in request.args:
            action=request.args['action']
            id=request.args['id']
            if action=='Add':
                q="INSERT into my_vehicle VALUES(NULL,'%s','%s','pending',curdate())"%(session['user'],id)
                r=select(q)
                return"<script>alert('Added');window.location='/view_own_vehicle'</script>"  
        response = make_response(render_template("view_own_vehicle.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("view_own_vehicle.html",data=data)


@users.route('/view_my_vehicle',methods=['post','get'])
def add_myvehicle():
    if 'log' in session:
        data={}
        c="select * from my_vehicle INNER JOIN vehicle using (vehicle_id)where user_id='%s'"%(session['user'])
        data['view']=select(c)
        if'action'in request.args:
            action=request.args['action']
            id=request.args['id']

            if action=='request':
                q="select * from my_vehicle INNER JOIN vehicle using (vehicle_id)where vehicle_id='%s'"%(id)
                r=select(q)
                data['veh']=r
                print(data,"(((((((((((((((((())))))))))))))))))")
        response = make_response(render_template("view_my_vehicle.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    return render_template("view_my_vehicle.html",data=data)




from vehicle_pred import predictvehicle

@users.route('/user_add_price',methods=['get','post'])
def user_add_price():

    data={}
    c="select * From price_info where user_id='%s'"%(session['user'])
    data['view']=select(c)
    
    if 'register' in request.form:
        
        carname = request.form['carname']
        regyear = request.form['regyear']
        seater = int(request.form['seater'])
        insurance = float(request.form['insurance'])
        fuel = request.form['fuel']
        km = float(request.form['km'])
        owner = request.form['owner']
        transmission = request.form['transmission']
        manufacture = request.form['manufacture']
        milege = float(request.form['millege'])
        engine = request.form['engine']
        maxpower = request.form['maxpower']
        torque= request.form['torque']
      
        
        result1 = predict(carname, regyear, seater, insurance, fuel, km, owner, transmission, manufacture, milege, engine, maxpower, torque)

        print("result1:", result1)

        image = request.files['image']

        if image.filename:
            path = "static/" + str(uuid.uuid4()) + image.filename
            print(path)

            image.save(path)
            result=predictvehicle(path)
            print(result,"pppppppppppppppppppppppppppppppppppppppppp")
            if result=='The image contains a vehicle!':
                out = predictcnn(path)
                print(out, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


            
                if out == 0:
                    data['res1'] = "75-90 %"
                    damage_percentage = 0.825  # Average of 75-90%
                    data['amt'] = 50000

                if out == 1:
                    data['res1'] = "60-75 %"
                    damage_percentage = 0.675  # Average of 60-75%
                    data['amt'] = 25000

                if out == 2:
                    data['res1'] = "50-60 %"
                    damage_percentage = 0.55  # Average of 50-60%
                    data['amt'] = 15000

                print("data:", data['res1'])

                # Calculate scrap value
                initial_value = float(result1)
                remaining_value_percentage = 1 - damage_percentage
                scrap_value = initial_value * remaining_value_percentage
                
                data['scrap_value'] = scrap_value

                print("Scrap Value:", scrap_value)
                # id=request.args['id']
                
                qry="insert into price_info values(null,'%s','%s','%s')"%(scrap_value,path,session['user'])
                insert(qry)
                # qrt="update scrapprequest set status='price Added' where request_id='%s'"%(id)
                # dd=update(qrt)
                # print(dd,"_____________________")
                
                return '''<script>alert("Add successfully");window.location="/user_add_price"</script>'''
            
            else:
                return '''<script>alert("Doesnt Recongize  Any Vehicle");window.location="/user"</script>'''


    return render_template('user_add_price.html',data=data)

@users.route('/view_usercertifcate',methods=['post','get'])
def view_usercertificate():
    data={}
    id=request.args['id']
    c="select * From certificate where request_id='%s'"%(id)
    data['view']=select(c)

    return render_template("view_usercertificate.html",data=data)


@users.route('/view_price_info',methods=['post','get'])
def view_price_info():
    data={}
    c="select * From price_info where user_id='%s'"%(session['user'])
    data['view']=select(c)

    return render_template("view_price_info.html",data=data)
