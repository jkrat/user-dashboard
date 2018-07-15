from flask import Flask, flash, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
# from models import Validator
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'dortmund'
bcrypt = Bcrypt(app)

mysql = connectToMySQL('regform_1')

@app.route("/")
def user_form():  
    return render_template("index.html")

@app.route("/success")
def user_registered():
    return render_template("success.html")

@app.route("/wall")
def enter_sites():
    return render_template("success.html")

@app.route("/register", methods=['POST'])
def register_page():
    session.clear()
    session['firstName']= request.form['firstName']
    session['lastName']= request.form['lastName']
    session['email']= request.form['email']
    #name validations
    if request.form['firstName'].isalpha() == False or len(request.form['firstName']) < 2:
        session['firstName_validation_error'] = 'is-invalid'
        errors.append(['Invalid first name', 'firstName'])

    if request.form['lastName'].isalpha() == False or len(request.form['lastName']) < 2:
        flash('Invalid last name', 'lastName')
        session['lastName_validation_error'] = 'is-invalid'
    #email validations    
    if not EMAIL_REGEX.match(request.form['email']) or len(request.form['email']) < 1:
        flash("Invalid email address", "email")
        session['email_validation_error'] = 'is-invalid'
    #duplicate email check
    else:
        email_duplicate_query = "SELECT email FROM users WHERE email = %(email)s;"
        email_duplicate_query_result = mysql.query_db(email_duplicate_query, request.form)
        if email_duplicate_query_result:
            flash("Email address already registered", "email")
            session['email_validation_error'] = 'is-invalid'
    #password validations
    if len(request.form['password']) < 8:
        flash('Password should be more than 8 characters', 'password')
        session['password_validation_error'] = 'is-invalid'

    if request.form['password'] != request.form['confirmPassword']:
        flash('Passwords should match', 'confirmPassword')
        session['confirmPassword_validation_error'] = 'is-invalid'

    # registration fail
    if '_flashes' in session.keys():
        print("\n\n---------------------------------")
        print(session)
        return redirect('/')
    #registration success
    else:
        user_sub = {
            'firstName' : request.form['firstName'], 
            'lastName' : request.form['lastName'], 
            'email' : request.form['email'], 
            'password' : bcrypt.generate_password_hash(request.form['password'])
    }
        insert_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
        mysql.query_db(insert_query, user_sub)
        session["logged_in"] = True
        return redirect("/success")     

@app.route("/login", methods=["POST"])
def login_user():
    if request.form['password']:
        login_sub = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        password_match_query = "SELECT id, first_name, password FROM users WHERE email = %(email)s;"
        password_match_query_result = mysql.query_db(password_match_query, login_sub)
        print('SESSION:', password_match_query_result)
        if password_match_query_result:
            check = bcrypt.check_password_hash(password_match_query_result[0]['password'], login_sub['password'])
        
            #user validation success    
            if check:
                session.clear()
                session["id"] = password_match_query_result[0]['id']
                session["firstName"] = password_match_query_result[0]['first_name']
                session["logged_in"] = True
                return redirect("/wall")

                
    #user validation fail
    if request.form['email']:
        session['login-email'] = request.form['email']
    flash("You could not be logged in", "login_error")
    return redirect('/') 


@app.route("/logout")
def logout_user():
    flash('You have been logged out', 'logout')
    session.clear()  #OR session['count'] = 0 OR session.clear() OR session.pop('')
    return redirect("/")

def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)
    print("\n\n-------------------------------------------")

if __name__=="__main__":
    app.run(debug=True)  



