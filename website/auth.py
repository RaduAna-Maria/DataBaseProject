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

@auth.route('/edit_database_university_insert', methods=['GET','POST'])
def edit_database_university_insert():
    if request.method == 'POST':            
        name = request.form.get('name_insert')
        street = request.form.get('street_insert')
        number = request.form.get('number_insert')
        city = request.form.get('city_insert')
        county = request.form.get('county_insert')

        query = "SELECT * FROM University WHERE Name = '{}'"
        query = query.format(name)
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            flash('University already exists', category='error')
        else:
            query = "INSERT INTO University (Name, Street, Number, City, County) VALUES ('{}', '{}', '{}', '{}', '{}')"
            query = query.format(name,street,number,city,county)
            cursor.execute(query)
            cnxn.commit()
            flash('University added', category='success')

        query = "SELECT Name, Street, Number, City, County FROM University"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
            p.append(row[4])
      
    return render_template("home_edit_university_insert.html", acc = p, n = len(p))

@auth.route('/edit_database_university_update', methods=['GET','POST'])
def edit_database_university_update():
    if request.method == 'POST':
        name1 = request.form.get('name_update')
        name2 = request.form.get('new_name_update')
        street = request.form.get('street_update')
        number = request.form.get('number_update')

        query = "SELECT * FROM University WHERE Name = '{}'"
        query = query.format(name1)
        cursor.execute(query)
        user = cursor.fetchone()
        print(query)

        if not user:
            flash('University does not exist', category='error')
        else:
            query = "UPDATE University SET Name = '{}', Street = '{}', Number = '{}' WHERE Name = '{}'"
            query = query.format(name2,street,number,name1)
            cursor.execute(query)
            print(query)
            cnxn.commit()
            flash('University updated', category='success')

        query = "SELECT Name, Street, Number, City, County FROM University"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
            p.append(row[4])

    return render_template("home_edit_university_update.html", acc = p, n = len(p))

@auth.route('/edit_database_university_delete', methods=['GET','POST'])
def edit_database_university_delete():
    if request.method == 'POST':
        name = request.form.get('name_delete')

        query = "SELECT * FROM University WHERE Name = '{}'"
        query = query.format(name)
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            flash('University does not exist', category='error')
        else:
            query = "DELETE FROM University WHERE Name = '{}'"
            query = query.format(name)
            cursor.execute(query)
            cnxn.commit()
            flash('University deleted', category='success')

        query = "SELECT Name, Street, Number, City, County FROM University"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
            p.append(row[4])

    return render_template("home_edit_university_delete.html", acc = p, n = len(p))

@auth.route('/edit_database_sport_insert', methods=['GET','POST'])
def edit_database_sport_insert():
    if request.method == 'POST':
        name = request.form.get('name_insert')
        type_s = request.form.get('type_insert')
        field = request.form.get('field_insert')

        query = "SELECT * FROM Sport WHERE Name = '{}'"
        query = query.format(name)
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            flash('Sport already exists', category='error')
        else:
            query = "INSERT INTO Sport (Name, Type, Field) VALUES ('{}', '{}', '{}')"
            query = query.format(name,type_s,field)
            cursor.execute(query)
            cnxn.commit()
            flash('Sport added', category='success')

        query = "SELECT Name, Type, Field FROM Sport"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])

    return render_template("home_edit_sport_insert.html", acc = p, n = len(p))

@auth.route('/edit_database_sport_update', methods=['GET','POST'])
def edit_database_sport_update():
    if request.method == 'POST':
        name1 = request.form.get('name_update')
        name2 = request.form.get('new_name_update')
        type_s = request.form.get('type_update')
        field = request.form.get('field_update')

        query = "SELECT * FROM Sport WHERE Name = '{}'"
        query = query.format(name1)
        cursor.execute(query)
        user = cursor.fetchone()
        print(query)

        if not user:
            flash('Sport does not exist', category='error')
        else:
            query = "UPDATE Sport SET Name = '{}', Type = '{}', Field = '{}' WHERE Name = '{}'"
            query = query.format(name2,type_s,field,name1)
            cursor.execute(query)
            print(query)
            cnxn.commit()
            flash('Sport updated', category='success')

        query = "SELECT Name, Type, Field FROM Sport"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])

    return render_template("home_edit_sport_update.html", acc = p, n = len(p))

@auth.route('/edit_database_sport_delete', methods=['GET','POST'])
def edit_database_sport_delete():
    if request.method == 'POST':
        name = request.form.get('name_delete')

        query = "SELECT * FROM Sport WHERE Name = '{}'"
        query = query.format(name)
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            flash('Sport does not exist', category='error')
        else:
            query = "DELETE FROM Sport WHERE Name = '{}'"
            query = query.format(name)
            cursor.execute(query)
            cnxn.commit()
            flash('Sport deleted', category='success')

        query = "SELECT Name, Type, Field FROM Sport"
        cursor.execute(query)
        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])

    return render_template("home_edit_sport_delete.html", acc = p, n = len(p))

@auth.route('/simple_queries1', methods=['GET','POST'])
def simple_queries1():
    if request.method == 'POST':
        number = request.form.get('var')

        query = """ SELECT S.Name, S.Surname, T.Name
                    FROM Student S JOIN Team T ON S.TeamID = T.TeamID
                    JOIN TournamentTeam TT
                    ON S.TeamID = TT.TeamID
                    GROUP BY S.Name, S.Surname, T.Name
                    HAVING COUNT(TT.TeamID) >= {}"""
        query = query.format(number)
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
        
        cnxn.commit()

    return render_template("simple_queries1.html", acc = p, n = len(p))

@auth.route('/simple_queries2', methods=['GET','POST'])
def simple_queries2():
    if request.method == 'POST':
        query = """ SELECT T.Name, Count(S.TeamID) AS Students
                    FROM  Team T LEFT JOIN Student S
                    ON T.TeamID = S.TeamID
                    GROUP BY T.Name"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
        
        cnxn.commit()
        
    return render_template("simple_queries2.html", acc = p, n = len(p))

@auth.route('/simple_queries3', methods=['GET','POST'])
def simple_queries3():
    if request.method == 'POST':
        query = """ SELECT DISTINCT T.Name
                    FROM Team T LEFT JOIN Tournament TOU
                    ON T.SportID = TOU.SportID
                    WHERE TOU.StartDate > '2023/04/30'
                    GROUP BY T.Name"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
        
        cnxn.commit()
    return render_template("simple_queries3.html", acc = p, n = len(p))

@auth.route('/simple_queries4', methods=['GET','POST'])
def simple_queries4():
    if request.method == 'POST':
        query = """ SELECT U.Name, COUNT(S.StudentID) AS NUmberOfStudents
                    FROM University U LEFT JOIN Student S ON U.UniversityID = S.UniversityID
                    WHERE S.Sex = 'F'
                    GROUP BY U.Name"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
        
        cnxn.commit()
        
    return render_template("simple_queries4.html", acc = p, n = len(p))

@auth.route('/simple_queries5', methods=['GET','POST'])
def simple_queries5():
    if request.method == 'POST':
        query = """ SELECT T.Name, TT.NumberOfPoints, S.Name, S.Surname
                    FROM STUDENT S 
                    JOIN Team T ON S.TeamID = T.TeamID
                    JOIN TournamentTeam TT ON T.TeamID = TT.TeamID
                    WHERE S.YearOfStudy > 1 AND S.Grade > 7 AND 10*T.NumberOfVictories < TT.NumberOfPoints
                    GROUP BY T.Name, TT.NumberOfPoints, S.Name, S.Surname
                    ORDER BY TT.NumberOfPoints DESC"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
        
        cnxn.commit()
        
    return render_template("simple_queries5.html", acc = p, n = len(p))

@auth.route('/simple_queries6', methods=['GET','POST'])
def simple_queries6():
    if request.method == 'POST':
        sport = request.form.get('var')

        query = """ SELECT TOP 3 T.Name, T.CoachName, T.CoachSurname, T.NumberOfVictories
                    FROM Team T JOIN Sport S
                    ON T.SportID = S.SportID
                    WHERE S.Name = '{}'
                    ORDER BY T.NumberOfVictories DESC"""
        query = query.format(sport)
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
        
        cnxn.commit()
    return render_template("simple_queries6.html", acc = p, n = len(p))

@auth.route('/complex_queries1', methods=['GET','POST'])
def compex_queries1():
    if request.method == 'POST':
        query = """ SELECT T.Name, T.NumberOfVictories, S.Name
                    FROM Team T JOIN Sport S ON T.SportID = S.SportID
                    WHERE T.NumberOfVictories IN (SELECT MAX(T2.NumberOfVictories)
                                                    FROM Team T2
                                                    WHERE T2.SportID = T.SportID)
                    ORDER BY T.NumberOfVictories"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
        
        cnxn.commit()
    return render_template("complex_queries1.html", acc = p, n = len(p))

@auth.route('/complex_queries2', methods=['GET','POST'])
def compex_queries2():
    if request.method == 'POST':
        query = """ SELECT T.Name, S.Name, T.StartDate, T.EndDate
                    FROM Tournament T JOIN Sport S ON T.SportID = S.SportID
                    WHERE S.Name != 'Inot'
                    AND (T.StartDate > ANY (SELECT T2.StartDate
                                            FROM Tournament T2 JOIN Sport S2 ON T2.SportID = S2.SportID
                                            WHERE S2.Name = 'Inot'))"""
        cursor.execute(query)

        p = []
        for row in cursor.fetchall():
            p.append(row[0])
            p.append(row[1])
            p.append(row[2])
            p.append(row[3])
        
        cnxn.commit()
    return render_template("complex_queries2.html", acc = p, n = len(p))

@auth.route('/complex_queries3', methods=['GET','POST'])
def compex_queries3():
    return render_template("complex_queries3.html")

@auth.route('/complex_queries4', methods=['GET','POST'])
def compex_queries4():
    return render_template("complex_queries4.html")