from flask import Flask, flash, request, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'dortmund'
bcrypt = Bcrypt(app)

def db_connection(db_name):
    global mysql
    mysql = connectToMySQL(db_name)

def check_for_duplicate_email(data):
    query = "SELECT email FROM users WHERE email = %(email)s;"
    return mysql.query_db(query, data)

def insert_user(data):
    query = "INSERT INTO users (first_name, last_name, email, password, user_level, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, 1, NOW(), NOW());"
    return mysql.query_db(query, data)

def check_password_match(data):
    query = "SELECT id, first_name, password FROM users WHERE email = %(email)s;"
    return mysql.query_db(query, data)

def validate_registration(data):   
    #name validations
    if data['firstName'].isalpha() == False or len(data['firstName']) < 2:
        flash('Invalid first name', 'firstName')
        session['firstName_validation_error'] = 'is-invalid'
        # errors.append(['Invalid first name', 'firstName'])
    if data['lastName'].isalpha() == False or len(data['lastName']) < 2:
        flash('Invalid last name', 'lastName')
        session['lastName_validation_error'] = 'is-invalid'
    #email validations    
    if not EMAIL_REGEX.match(data['email']) or len(data['email']) < 1:
        flash("Invalid email address", "email")
        session['email_validation_error'] = 'is-invalid'
    #duplicate email check
    else:
        email_check_data = data
        duplicate_email = check_for_duplicate_email(email_check_data)
        if duplicate_email:
            flash("Email address already registered", "email")
            session['email_validation_error'] = 'is-invalid'
    #password validations
    if len(data['password']) < 8:
        flash('Password should be more than 8 characters', 'password')
        session['password_validation_error'] = 'is-invalid'
    if data['password'] != data['confirmPassword']:
        flash('Passwords should match', 'confirmPassword')
        session['confirmPassword_validation_error'] = 'is-invalid'
    # registration fail
    if '_flashes' in session.keys():
        return False
    #registration success
    else:
        user_insert_data= {
            'firstName' : data['firstName'], 
            'lastName' : data['lastName'], 
            'email' : data['email'], 
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        insert_user(user_insert_data)
        return True

def validate_login(data):
    if data['password']:
        login_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        password_match_result = check_password_match(login_data)
        if password_match_result:
            #user validation success 
            if bcrypt.check_password_hash(password_match_result[0]['password'], login_data['password']):
                session.clear()
                session["id"] = password_match_result[0]['id']
                session["firstName"] = password_match_result[0]['first_name']
                return True           
    #user validation fail
    if request.form['email']:
        session['login-email'] = request.form['email']
    flash("You could not be logged in", "login_error")
    return False

class User_Obj(object):
    def create(self, data):
        session.clear()
        session['firstName']= data['firstName']
        session['lastName']= data['lastName']
        session['email']= data['email']
        user_input = data
        if validate_registration(user_input):
            session["logged_in"] = True
            return True
        else:
            return False
    def login(self, data):
        if validate_login(data):
            session["logged_in"] = True
            print(session)
            return True
        else: 
            return False
    def logout(self):
        flash('You have been logged out', 'logout')
        session.clear()  #OR session['count'] = 0 OR session.clear() OR session.pop('')


        






       





