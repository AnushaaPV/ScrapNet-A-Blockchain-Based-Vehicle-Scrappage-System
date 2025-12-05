from flask import *
from database import *

police=Blueprint("police",__name__)

@police.route('/police')
def policepage():
    if 'log' in session:
        response = make_response(render_template("Policehome.html"))
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
    return render_template("Policehome.html")

@police.route('/view_police_profile',methods=['post','get'])
def view_profile_profile():
     if 'log' in session:
          data={}
          c="select * from police where police_id='%s'"%(session['police'])
          data['view']=select(c)
          response = make_response(render_template("PoliceProfile.html",data=data))
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
     return render_template("PoliceProfile.html",data=data)

@police.route('/view_vehicles',methods=['post','get'])
def view_vehicles():
     if 'log' in session:
          data={}
          c="select * from vehicle"
          data['view']=select(c)
          if'action'in request.args:
               action=request.args['action']
               id=request.args['id']
               if action=='Suspicous':
                    q="select * from vehicle where vehicle_id='%s'"%(id)
                    r=select(q)
          response = make_response(render_template("view_vehicles.html",data=data))
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
     return render_template("view_vehicles.html",data=data)

@police.route('/manage_suspicious_activity',methods=['post','get'])
def manage_suspicious_activity():
     if 'log' in session:
          data={}
          a="select * from suspiciousactivity"
          data['view']=select(a)
          if 'submit' in request.form:
               Title=request.form['title']
               Description=request.form['description']
               id=request.args['id']
               qry="insert into suspiciousactivity values(NULL,'%s','%s','%s','%s',curdate())"%(id,session['police'],Title,Description)
               ins=insert(qry)
               print(qry)
               return '''<script>alert(" submitted Successfully ");window.location="/manage_suspicious_activity"</script>'''
          response = make_response(render_template("manage_suspicious_activity.html",data=data))
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
     return render_template("manage_suspicious_activity.html",data=data)
