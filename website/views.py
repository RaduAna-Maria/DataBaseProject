from flask import Blueprint, redirect, render_template

views = Blueprint('views', __name__)

@views.route('/')
def login():
    return redirect('login')

@views.route('/sing_up')
def sing_up():
    return render_template('sing_up.html')

@views.route('/home')
def home():
    return render_template('home.html')

@views.route('/change_password')
def change_password():
    return render_template('change_password.html')

@views.route('/delete_account')
def delete_account():
    return render_template('delete_account.html')

@views.route('/home/edit_database')
def home_edit_database():
    return render_template('home.html')

@views.route('/home/statistics')
def home_statistics():
    return render_template('home.html')