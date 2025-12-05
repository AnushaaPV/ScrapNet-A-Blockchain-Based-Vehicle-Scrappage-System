import datetime
import uuid
from flask import *
from database import *
from blk import *


rto=Blueprint("rto",__name__)

@rto.route('/rto')
def rtopage():
    if 'log' in session:
        response = make_response(render_template("RTOhome.html"))
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
    return render_template("RTOhome.html")

# @rto.route('/view_users',methods=['post','get'])
# def view_users():
#     if 'log' in session:
#         data={}
#         b="select * from user"
#         data['view']=select(b)
#         response = make_response(render_template("view_users.html",data=data))
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
#     return render_template("view_users.html",data=data)
 
@rto.route('/view_rto_profile',methods=['post','get'])
def view_rto_profile():
    if 'log' in session:
     data={}
     c="select * from rto where Rto_id='%s'"%(session['rto'])
     data['view']=select(c)
     response = make_response(render_template("RTOprofile.html",data=data))
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
    return render_template("RTOprofile.html",data=data)


@rto.route('/rto_forwarded_scrapvehicle',methods=['post','get'])
def rto_forwarded_scrapvehicle():
    if 'log' in session:
     data={}
     c="SELECT *,scarprrequest.status AS request_status FROM scarprrequest INNER JOIN my_vehicle USING(my_vehicle_id) INNER JOIN USER USING(user_id) INNER JOIN vehicle USING(vehicle_id) WHERE Rto_id='%s' AND scarprrequest.status IN ('forward','approve','scrapped')"%(session['rto'])
     data['view']=select(c) 
     if 'action' in request.args:
         act=request.args['action']
         id=request.args['id']
         if act == 'approve':
             a="update scarprrequest set status='approve' where request_id='%s'"%(id)
             update(a)
             return "<script>alert('Approved');window.location='/rto_forwarded_scrapvehicle'</script>"  
         if act == 'reject':
             a="update scarprrequest set status='rejected' where request_id='%s'"%(id)
             update(a)
             return "<script>alert('Rejected');window.location='/rto_forwarded_scrapvehicle'</script>"  
     response = make_response(render_template("rto_forwarded_scrapvehicle.html",data=data))
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
    return render_template("rto_forwarded_scrapvehicle.html",data=data)

@rto.route('/manage_vehicle',methods=['post','get'])
def manage_vehicle():
    if 'log' in session:
        data={}
        b="select * from vehicle"
        data['view']=select(b)
        if 'submit' in request.form:
            Model=request.form['model']
            Enginenum=request.form['enginenum']
            ChassisNumber=request.form['chasesno']
            SeatNumber=request.form['seater']
            RegisterNumber=request.form['regno']
            p="insert into vehicle values(NULL,'%s','%s','%s','%s','%s','%s',curdate())"%(session['rto'],Model,Enginenum,ChassisNumber,SeatNumber,RegisterNumber)
            ins=insert(p)
            print(ins)
            return "<script>alert('Sucessfully Submitted');window.location='/manage_vehicle'</script>"
        response = make_response(render_template("manage_vehicle.html",data=data))
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
    return render_template("manage_vehicle.html",data=data)

@rto.route('/view_rto_suspicious',methods=['post','get'])
def view_rto_suspicious():
    if 'log' in session:
     data={}
     c="SELECT * FROM suspiciousactivity INNER JOIN vehicle USING(vehicle_id) INNER JOIN my_vehicle USING(vehicle_id) INNER JOIN police USING(police_id)"
     data['view']=select(c)
     response = make_response(render_template("view_suspicious.html",data=data))
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
    return render_template("view_suspicious.html",data=data)

# @scrap.route('/view_scrapped_vehicle',methods=['post','get'])
# def view_scrapped_vehicle():
#      data={}
#      c="SELECT * FROM scarprrequest INNER JOIN my_vehicle USING(my_vehicle_id) INNER JOIN USER USING(user_id) INNER JOIN  vehicle USING (vehicle_id)WHERE scrapper_id='%s' AND scarprrequest.status='forward'"%(session['scrap'])
#      data['view']=select(c)
#      return render_template("view_scrapped_vehicle.html",data=data)




@rto.route('/rto_add_certicate',methods=['post','get'])
def add_certicate():
    data={}
    id=request.args['id']
    qrt="select * from vehicle where vehicle_id='%s'"%(id)
    res=select(qrt)
    data['view']=res
    date=datetime.date.today()
    return render_template('rto_add_certicate.html',data=data,date=date)


@rto.route('/upload_certificate',methods=['post','get'])
def upload_certificate():
    rid=request.args['rid']
    
    from datetime import datetime

    # Get the current date and time
    current_datetime = datetime.now()

    # Print the current date and time
    print("Current date and time:", current_datetime)

    if 'register' in request.form:
        certificate=request.files['certificate']
        path='static/'+str(uuid.uuid4())+certificate.filename
        certificate.save(path)

        qry1="insert into certificate values(null,'%s','%s','%s',curdate())"%(rid,session['rto'],path)
        insert(qry1)

        qrt="update scarprrequest set status='Certificate Added' where request_id='%s'"%(rid)
        dd=update(qrt)
        print(dd,"_____________________")

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address,abi=contract_abi)
        id=web3.eth.get_block_number()
        message = contract.functions.addCertificate(int(id),int(rid),int(session['rto']),str(path),str(current_datetime)).transact()
        print(message)
        return '''<script>alert("Certificate Add successfully");window.location="/rto"</script>'''
        
        
    return render_template('rto_upload_certificate.html')

@rto.route('/view_certified_scrapreq',methods=['post','get'])
def view_certified_scrapreq():
    data={}
    c="SELECT * FROM `vehicle` INNER JOIN `my_vehicle` USING(vehicle_id) INNER JOIN `scarprrequest` USING(my_vehicle_id) WHERE scarprrequest.status='Certificate Added'"
    data['view']=select(c)
    return render_template('view_certified_scrapreq.html',data=data)

