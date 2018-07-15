from flask import Flask
from models import db_connection
from urls import routes

DB_NAME = 'thewall'
app = Flask(__name__)
app.secret_key = 'dortmund'

db_connection(DB_NAME)
routes(app)

if __name__=="__main__":
    app.run(debug=True)  



