from flask import *
from database import *

admin=Blueprint("admin",__name__)

@admin.route('/admin')
def adminpage():
    if 'log' in session:
        response = make_response(render_template("admin.html"))
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
    return render_template("admin.html")

@admin.route('/RTO',methods=['post','get'])
def Rtoreg():
    if 'log' in session:
        data={}
        a="select * from rto"
        data['view']=select(a)
        if 'submit' in request.form:
            Rname=request.form['Rname']
            place=request.form['place']
            phno=request.form['phonenumber']
            pincode=request.form['pin']
            email=request.form['email']
            RegNo=request.form['regno']
            username=request.form['username']
            password=request.form['password']
            rto="insert into login values(NULL,'%s','%s','rto')"%(username,password)
            ins=insert(rto)
            print(ins)

            r="insert into rto values(NULL,'%s','%s','%s','%s','%s','%s','%s')"%(ins,Rname,place,phno,pincode,email,RegNo)
            ins=insert(r)
            print(ins)
            # return "<script>alert('Registered successfully);window.location='/complaint/RTO'</script>"
        response = make_response(render_template("RTO.html",data=data))
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
    return render_template("RTO.html",data=data)

@admin.route('/Police',methods=['post','get'])
def policereg():
    if 'log' in session:
        data={}
        b="select * from police"
        data['view']=select(b)
        if 'submit' in request.form:
            Sname=request.form['Sname']
            place=request.form['place']
            pincode=request.form['pin']
            email=request.form['email']
            phno=request.form['phonenumber']
            username=request.form['username']
            password=request.form['password']
            police="insert into login values(NULL,'%s','%s','police')"%(username,password)
            ins=insert(police)
            print(ins)

            p="insert into police values(NULL,'%s','%s','%s','%s','%s','%s')"%(ins,Sname,place,pincode,email,phno)
            ins=insert(p)
            print(ins)
            return "<script>alert('Registered successfully);window.location='/complaint'</script>"
        response = make_response(render_template("Police.html",data=data))
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
    return render_template("Police.html",data=data)

@admin.route('/complaint',methods=['post','get'])
def viewcomp():
    if 'log' in session:
        data={}
        c="select * from complaint"
        data['view']=select(c)
        if'action'in request.args:
            action=request.args['action']
            id=request.args['id']

            if action=='reply':
                q="select * from complaint where complaint_id='%s'"%(id)
                r=select(q)
                if r:
                    data['reply']=r
                    if'submit'in request.form:
                        reply=request.form['reply']
                        a=" update complaint set reply='%s'where complaint_id='%s'"%(reply,id)
                        update(a)
                        # popmsg
                        return "<script>alert('replied');window.location='/complaint'</script>"
        response = make_response(render_template("viewcomplaint.html",data=data))
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
    return render_template("viewcomplaint.html",data=data)

@admin.route('/scrapcomp',methods=['post','get'])
def viewcompany():
    if 'log' in session:
        data={}
        c="select * from scrap INNER JOIN login USING(login_id)"
        data['view']=select(c) 
        if 'action' in request.args:
            act=request.args['action']
            id=request.args['id']
            if act == 'approve':
                a="update login set usertype='scrap' where login_id='%s'"%(id)
                update(a)
                return "<script>alert('Approved');window.location='/scrapcomp'</script>"  
            if act == 'reject':
                a="update login set usertype='rejected' where login_id='%s'"%(id)
                update(a)
                return "<script>alert('Rejected');window.location='/scrapcomp'</script>"  
        response = make_response(render_template("scrapcomp.html",data=data))
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
    return render_template("scrapcomp.html",data=data)
        

@admin.route('/comprating',methods=['post','get'])
def companyrating():
    if 'log' in session:
        data={}
        c="SELECT * FROM rating INNER JOIN scrap USING(scrapper_id)"
        data['view']=select(c)
        if 'submit' in request.form:
            rate=request.form['rate']
            rate="insert into rating values(NULL,'%s','%s','%s',curdate())"%(session['log'],rate)
            ins=insert(rate)
            print(ins)
        response = make_response(render_template("comprating.html",data=data))
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
    return render_template("comprating.html",data=data)



