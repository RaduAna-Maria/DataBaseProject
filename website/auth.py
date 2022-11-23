from flask import Blueprint, render_template, request,  flash , redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import cnxn, cursor

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT * FROM [User] WHERE Email = '{}'"
        query = query.format(email)
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            if check_password_hash(user.Password, password):
                flash('Logged in', category = 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorect password. Please try again', category = 'error')
        else:
            flash('Account not find. Please sing up', category = 'error')
            return redirect(url_for('views.sing_up'))

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        query = "SELECT * FROM [User] WHERE Email = '{}'"
        query = query.format(email)
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            flash('Account already exists', category='error')
            return redirect(url_for('views.login'))
        if len(email) < 4:
            flash('Email must have at least 4 characters', category='error')
        elif len(username) < 2:
            flash('User must have at least 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must have at least 7 characters', category='error')
        else:
            password = generate_password_hash(password1, method='sha256')
            query = "INSERT INTO [User] (Email, Username, Password) VALUES ('{}', '{}', '{}')"
            query = query.format(email, username, password)
            cursor.execute(query)
            cnxn.commit()
            flash('Acount created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sing_up.html")

@auth.route('/change_password', methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        query = "SELECT * FROM [User] WHERE Email = '{}'"
        query = query.format(email)
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            flash('Account does not exist', category='error')
        elif not check_password_hash(user.Password, password1):
            flash('Incorrect password', category='error')
        elif password1 == password2:
            flash('New password similar to old password', category='error')
        else:
            password = generate_password_hash(password2, method='sha256')
            query = "UPDATE [User] SET Password = '{}' WHERE Email = '{}'"
            query = query.format(password,email)
            cursor.execute(query)
            cnxn.commit()
            flash('Password changed', category='success')
            return redirect(url_for('views.home'))

    return render_template("change_password.html")

@auth.route('/delete_account', methods=['GET','POST'])
def delete_account():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT * FROM [User] WHERE Email = '{}'"
        query = query.format(email)
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            flash('Account does not exist', category='error')
        elif not check_password_hash(user.Password, password):
            flash('Incorrect password', category='error')
        else:
            query = "DELETE FROM [User] WHERE Email = '{}'"
            query = query.format(email)
            cursor.execute(query)
            flash('Account deleted', category='success')
            return redirect(url_for('views.login'))

    return render_template("delete_account.html")