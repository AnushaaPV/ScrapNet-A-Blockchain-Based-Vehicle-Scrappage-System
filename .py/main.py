from flask import *
from admin import*
from public import *
from scrap import *
from user import *
from RTO import *
from Police import *

app=Flask(__name__)


app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(scrap)
app.register_blueprint(users)
app.register_blueprint(rto)
app.register_blueprint(police)

app.secret_key="dfghjk"

app.run(debug=True,port=5009)