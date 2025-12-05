from flask import *
from database import *

public=Blueprint("public",__name__)

@public.route('/')
def home():
    return render_template("home.html")

@public.route('/login',methods=['post','get'])
def login():
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']
        print(username,password)
        db="select * from login where username='%s' AND password='%s'"%(username,password)
        a=select(db)
        print(a)
        if a:
            session['log']=a[0]['login_id']
        if a:
            if a[0]['usertype']=='admin':
                return redirect(url_for('admin.adminpage'))
            if a[0]['usertype']=='scrap':
                qry = " select * from scrap where login_id='%s'"%(session['log'])
                res =select(qry)
                if res:
                    session['scrap']=res[0]['scrapper_id']
                return redirect(url_for('scrap.scrappage'))
            if a[0]['usertype']=='user':
                qry = " select * from user where login_id='%s'"%(session['log'])
                res =select(qry)
                if res:
                    session['user']=res[0]['user_id']
                return redirect(url_for('user.userpage'))
            if a[0]['usertype']=='rto':
                qry = "select * from rto where login_id='%s'"%(session['log'])
                res =select(qry)
                if res:
                    session['rto']=res[0]['Rto_id']
                return redirect(url_for('rto.rtopage'))
            if a[0]['usertype']=='police':
                qry = " select * from police where login_id='%s'"%(session['log'])
                res =select(qry)
                if res:
                    session['police']=res[0]['police_id']
                return redirect(url_for('police.policepage'))
    return render_template("login.html")

@public.route('/scrapReg',methods=['post','get'])
def scrapreg():
    # if 'log' in session:
    
        if 'submit' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['place']
            post=request.form['post']
            pincode=request.form['pin']
            phno=request.form['phonenumber']
            email=request.form['email']
            licences=request.form['licences']
            username=request.form['username']
            password=request.form['password']

            qrty="select * from login where username='%s' and password='%s'"%(username,password)
            res=select(qrty)
            if res:
                print(res,"//////////////////////")
                return """<script>alert("USERNAME OR PASSWORD Already exists");window.location="/scrapReg"</script>"""
            else:
                scrap="insert into login values(NULL,'%s','%s','pending')"%(username,password)
                ins=insert(scrap)
                print(ins)
                b="insert into scrap values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(ins,fname,lname,place,post,pincode,phno,email,licences)
                ins=insert(b)
                return """<script>alert("Registration sucessfully");window.location="/login"</script>"""

        return render_template("scrapReg.html")
      
@public.route('/userReg',methods=['post','get'])
def userreg():
    # if 'log' in session:
        if 'submit' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['place']
            post=request.form['post']
            pincode=request.form['pin']
            phno=request.form['phonenumber']
            email=request.form['email']
            username=request.form['username']
            password=request.form['password']

            qrty="select * from login where username='%s' and password='%s'"%(username,password)
            res=select(qrty)
            if res:

                print(res,"//////////////////////")
                return """<script>alert("USERNAME OR PASSWORD Already exists");window.location="/userReg"</script>"""
            else:
                user="insert into login values(NULL,'%s','%s','user')"%(username,password)
                ins=insert(user)
                print(ins)
                c="insert into user values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"%(ins,fname,lname,place,post,pincode,phno,email)
                ins=insert(c)
                print(ins)
                return """<script>alert("Registration sucessfully");window.location="/login"</script>"""

        return render_template("userReg.html")



 
@public.route('/logout')
def logout():
    session.clear()
    return redirect('/')
