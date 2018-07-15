from flask import Flask, flash, render_template, request, redirect, session
from models import User_Obj

User = User_Obj()

def index():
    return render_template("index.html")

def register_user():
    if User.create(request.form):
        return redirect("/success")
    else:
        return redirect("/")

def new_user_page(): 
    return render_template("success.html")

def access_wall():
    return render_template("wall.html")

def login():
    if User.login(request.form):
        return redirect("/wall")
    else:
        return redirect('/') 

def logout():
    User.logout()
    return redirect("/")
