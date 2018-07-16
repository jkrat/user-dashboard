from flask import Flask, flash, render_template, request, redirect, session
from models import User_Obj, Message_Obj, fill_user_dropdown

User = User_Obj()
Message = Message_Obj()

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
    message_info = Message.display()
    messages = message_info['message_list']
    message_count = message_info['message_count']
    print(message_count)
    print(type(message_count))
    users = fill_user_dropdown()
    return render_template("wall.html", messages=messages, count=message_count, users=users)

def login():
    if User.login(request.form):
        return redirect("/wall")
    else:
        return redirect('/') 

def logout():
    User.logout()
    return redirect("/")

def create_message():
    Message.create(request.form)
    return redirect('/wall')

def delete_message(num):
    data = {'id' : int(num)}
    Message.delete(data)
    return redirect('/wall')
