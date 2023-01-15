from flask import Blueprint, redirect, render_template
from . import cnxn, cursor

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

@views.route('/edit_database_university_insert')
def edit_database_university_insert():
    query = "SELECT Name, Street, Number, City, County FROM University"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])
        p.append(row[3])
        p.append(row[4])

    return render_template('home_edit_university_insert.html', acc = p, n = len(p))

@views.route('/edit_database_university_update')
def edit_database_university_update():
    query = "SELECT Name, Street, Number, City, County FROM University"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])
        p.append(row[3])
        p.append(row[4])

    return render_template('home_edit_university_update.html', acc = p, n = len(p))

@views.route('/edit_database_university_delete')
def edit_database_university_delete():
    query = "SELECT Name, Street, Number, City, County FROM University"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])
        p.append(row[3])
        p.append(row[4])
    return render_template('home_edit_university_delete.html', acc = p, n = len(p))

@views.route('/edit_database_sport_insert')
def edit_database_sport_insert():
    query = "SELECT Name, Type, Field FROM Sport"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])

    return render_template('home_edit_sport_insert.html', acc = p, n = len(p))

@views.route('/edit_database_sport_update')
def edit_database_sport_update():
    query = "SELECT Name, Type, Field FROM Sport"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])

    return render_template('home_edit_sport_update.html', acc = p, n = len(p))

@views.route('/edit_database_sport_delete')
def edit_database_sport_delete():
    query = "SELECT Name, Type, Field FROM Sport"
    cursor.execute(query)
    p = []
    for row in cursor.fetchall():
        p.append(row[0])
        p.append(row[1])
        p.append(row[2])

    return render_template('home_edit_sport_delete.html', acc = p, n = len(p))

@views.route('/simple_queries1')
def simple_queries1():
    return render_template('simple_queries1.html', acc = 0)

@views.route('/simple_queries2')
def simple_queries2():
    return render_template('simple_queries2.html', acc = 0)

@views.route('/simple_queries3')
def simple_queries3():
    return render_template('simple_queries3.html', acc = 0)

@views.route('/simple_queries4')
def simple_queries4():
    return render_template('simple_queries4.html', acc = 0)

@views.route('/simple_queries5')
def simple_queries5():
    return render_template('simple_queries5.html', acc = 0)

@views.route('/simple_queries6')
def simple_queries6():
    return render_template('simple_queries6.html', acc = 0)

@views.route('/complex_queries1')
def complex_queries1():
    return render_template('complex_queries1.html', acc = 0)

@views.route('/complex_queries2')
def complex_queries2():
    return render_template('complex_queries2.html', acc = 0)

@views.route('/complex_queries3')
def complex_queries3():
    return render_template('complex_queries3.html', acc = 0)

@views.route('/complex_queries4')
def complex_queries4():
    return render_template('complex_queries4.html', acc = 0)