from flask import Flask, render_template, request, redirect, url_for ,flash,session
import pyodbc
from flask_bcrypt import Bcrypt
import uuid
import random
from datetime import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'choky'


# Replace with your own connection string

#For Local
# conn_str = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=localhost;"
#     "Database=db_test;"
#     "UID=sa;"
#     "PWD=Choky999;"
# )

#For Azure
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:cs264group2.database.windows.net,1433;"
    "Database=cs251;"
    "UID=cs264group2;"
    "PWD=adminGroup2;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO UserData VALUES (?,?,?);", id,name,age)
        return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/view', methods=['GET'])
def view_data():
    with pyodbc.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM UserData;")
            data = cursor.fetchall()
    return render_template('view.html', data=data)

@app.route('/homepage', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM [User] WHERE username = ?;", username)
                user = cursor.fetchone()
                if user and Bcrypt().check_password_hash(user[6], password):
                    session['userID'] = user[0]
                    session['username'] = username
                    session['name'] = user[2] 
                    session['ssn'] = user[1]
                    session['birth'] = user[3]
                    session['gender'] = user[4]
                    flash('Login successful', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Generate a random userID
            userID = str(random.randint(10000, 99999))
            name = request.form.get('name')
            username = request.form.get('username')
            password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            #phone = request.form.get('phone')
            ssn = request.form.get('ssn')
            birth = request.form.get('birth')
            gender = request.form.get('gender')
            with pyodbc.connect(conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO [User] (userID,name, username, pwd, ssn,birthDate,gender) VALUES (?,?,?,?,?,?,?);", userID,name, username, password, ssn,birth,gender)
            flash('Registration successful', 'success')
        except Exception as e:
            flash('An error occurred: ' + str(e), 'error')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/myprofile')
def myprofile():
    birthdate = session.get('birth')
    if birthdate:
        birthdate = datetime.strptime(birthdate, '%a, %d %b %Y %H:%M:%S %Z')
    return render_template('myprofile.html', birthdate=birthdate)

@app.route('/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    birthdate = session.get('birth')
    if birthdate:
        birthdate = datetime.strptime(birthdate, '%a, %d %b %Y %H:%M:%S %Z')
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            username = request.form.get('username')
            #phone = request.form.get('phone')
            ssn = request.form.get('ssn')
            birth = request.form.get('birth')
            with pyodbc.connect(conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE [User] SET name = ?, username = ?, ssn = ?, birthDate = ? WHERE userID = ?;", name, username, ssn, birth, session.get('userID'))
                    cursor.execute("SELECT * FROM [User] WHERE userID = ?;", session.get('userID'))
                    user = cursor.fetchone()
                    if user:
                        session['username'] = username
                        session['name'] = user[2]
                        session['ssn'] = user[1]
                        session['birth'] = user[3]
            flash('Registration successful', 'success')
        except Exception as e:
            flash('An error occurred: ' + str(e), 'error')
    return render_template('updateprofile.html', birthdate=birthdate)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('homepage'))

@app.route('/addition',methods=['GET','POST'])
def addition():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        #return redirect(url_for('login'))
    if request.method == 'POST':
        petID = str(random.randint(10000, 99999))
        userID = session.get('userID')
        foundDate = datetime.now()
        name = request.form.get('name')
        breed = request.form.get('breed')
        size = request.form.get('size')
        type = request.form.get('type')
        gender = request.form.get('gender')
        age = request.form.get('age')
        behaviour = request.form.get('behaviour')
        sterilisation = request.form.get('sterilisation')
        colors = request.form.get('colors')
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Pet (PetID,name, breed, size, gender, age, behaviour, sterilisation, hair_color,foundDate,userID) VALUES (?,?,?,?,?,?,?,?,?,?,?);",petID, name, breed, size, gender, age, behaviour, sterilisation, colors, foundDate,userID)
                if type == 'Dog':
                    cursor.execute("INSERT INTO Dog (PetID) VALUES (?);", petID)
                elif type == 'Cat':
                    cursor.execute("INSERT INTO Cat (PetID) VALUES (?);", petID)
        flash('Animal added successfully', 'success')
        return redirect(url_for('addition'))
    return render_template('addition.html')

if __name__ == '__main__':
    app.run(debug=True)
