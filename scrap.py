from flask import *
from database import *

scrap=Blueprint("scrap",__name__)

@scrap.route('/scrap')
def scrappage():
    if 'log' in session:
        response = make_response(render_template("scraphome.html"))
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
    
    return render_template("scraphome.html") 

@scrap.route('/scrap_viewrating',methods=['post','get'])
def scrap_viewrating():
     if 'log' in session:
          data={}
          c="SELECT * FROM rating INNER JOIN USER USING(user_id) WHERE rating.scrapper_id='%s'"%(session['scrap'])
          data['view']=select(c)
          response = make_response(render_template("scrap_viewrating.html",data=data))
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
     
     return render_template("scrap_viewrating.html",data=data)

@scrap.route('/view_scrap_profile',methods=['post','get'])
def view_scrap_profile():
     if 'log' in session:
          data={}
          c="select * from scrap where scrapper_id='%s'"%(session['scrap'])
          data['view']=select(c) 
          if 'action' in request.args:
               action=request.args['action']
               if action =='update':
                    qry="select * from scrap where scrapper_id='%s'"%(session['scrap'])
                    data['up']=select(qry) 

                    if 'submit' in request.form:
                         fname=request.form['fname']
                         lname=request.form['lname']
                         place=request.form['place']
                         post=request.form['post']
                         pincode=request.form['pin']
                         phno=request.form['phonenumber']
                         email=request.form['email']
                         licences=request.form['licences']
                         up_qry="update scrap set f_name='%s',l_name='%s',place='%s',post='%s',pin='%s',phone='%s',email='%s',licences='%s' where scrapper_id='%s'"%(fname,lname,place,post,pincode,phno,email,licences,session['scrap'])
                         update(up_qry)
          response = make_response(render_template("scrapprofile.html",data=data))
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
     return render_template("scrapprofile.html",data=data)

@scrap.route('/pending_scrap_req',methods=['post','get'])
def pending_scrap_req():
     if 'log' in session:
          data={}
          c="SELECT scarprrequest.status AS request_status,scarprrequest.*,my_vehicle.*,user.* FROM scarprrequest INNER JOIN my_vehicle USING(my_vehicle_id) INNER JOIN USER USING(user_id) WHERE scrapper_id='%s' AND scarprrequest.status='pending'"%(session['scrap'])
          data['view']=select(c)
          if 'action' in request.args:
               action=request.args['action']
               id=request.args['id']
               if action =='forward':
                    qry="UPDATE scarprrequest SET status='forward' WHERE request_id='%s'"%(id)
                    update(qry)
                    return '''<script>alert("Successfully Forwarded");window.location="/pending_scrap_req"</script>'''
          response = make_response(render_template("pendscrapReq.html",data=data))
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
     
     return render_template("pendscrapReq.html",data=data)

@scrap.route('/view_forwarded_request',methods=['post','get'])
def view_forwarded_request():
     if 'log' in session:
          data={}
          c="SELECT sr.*, mv.*, v.*, mv.status AS my_vehicle_status, sr.status AS scraprequest_status FROM scarprrequest sr INNER JOIN my_vehicle mv USING(my_vehicle_id) INNER JOIN vehicle v USING(vehicle_id) WHERE sr.status != 'pending' AND sr.scrapper_id = '%s'"%(session['scrap'])
          data['view']=select(c)
          response = make_response(render_template("view_forwarded_request.html",data=data))
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
     
     return render_template("view_forwarded_request.html",data=data)

@scrap.route('/view_scrapped_vehicle',methods=['post','get'])
def view_scrapped_vehicle():
    if 'log' in session:  
          data={}
          c="SELECT * FROM `vehicle` INNER JOIN `my_vehicle` USING(vehicle_id) INNER JOIN `scarprrequest` USING(my_vehicle_id) WHERE scarprrequest.status='Certificate Added' AND scarprrequest.scrapper_id='%s'"%(session['scrap'])
          data['view']=select(c)
          response = make_response(render_template("view_scrapped_vehicle.html",data=data))
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
    
    return render_template("view_scrapped_vehicle.html",data=data)

@scrap.route('/view_suspicious_activity',methods=['post','get'])
def view_suspicious_activity():
     if 'log' in session:
          data={}
          c="SELECT * FROM suspiciousactivity INNER JOIN vehicle USING(vehicle_id) INNER JOIN my_vehicle USING(vehicle_id) INNER JOIN police USING(police_id)"
          data['view']=select(c)
          response = make_response(render_template("view_suspicious_activity.html",data=data))
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
    
     return render_template("view_suspicious_activity.html",data=data)


@scrap.route('/update_status',methods=['post','get'])
def update_status():
    id=request.args['id']
    print(id,"//////////////")
    if 'add' in request.form:

        status=request.form['Status']

        print(status,"+++++++++++++++++++++")
    
        ress="UPDATE  scarprrequest SET status='%s' WHERE request_id='%s' "%(status,id)
        upt=update(ress)
        print(upt,"///////////////////")
        return "<script>alert('Sucessfully Submitted');window.location='/view_forwarded_request'</script>"  
    
    return render_template("update_status.html")