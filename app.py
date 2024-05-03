import os
from flask import Flask, json, jsonify, render_template, request, redirect, url_for ,flash,session
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
                cursor.execute("SELECT userID FROM [User] WHERE username = ?;", username)
                userID = cursor.fetchone()
                cursor.execute("SELECT * FROM [Admin] WHERE userID = ?;", userID)
                admin = cursor.fetchone()

                if user and Bcrypt().check_password_hash(user[6], password):
                    session['userID'] = user[0]
                    session['username'] = username
                    session['name'] = user[2] 
                    session['ssn'] = user[1]
                    session['birth'] = user[3]
                    session['gender'] = user[4]

                    if admin:
                        session['role'] = 'admin'
                        print("admin")
                        flash('Admin Login successful', 'question')
                    else:
                        session['role'] = 'user'
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
                    cursor.execute("INSERT INTO Member (userID,SSN) VALUES (?,?);", userID, ssn)
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
        return redirect(url_for('login'))
    
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
        #location
        ssn = session.get('ssn')
        province = request.form.get('province')
        street = request.form.get('street')
        zipcode = request.form.get('zipcode')
        sub_district = request.form.get('sub_district')
        district = request.form.get('district')
        
        # Call the upload function
        upload(petID)

        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Pet (PetID,name, breed, size, gender, age, behaviour, sterilization, hair_color,foundDate,userID,ImageID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", petID, name, breed, size, gender, age, behaviour, sterilisation, colors, foundDate, userID, petID)
                cursor.execute("INSERT INTO FoundPlace (userID , SSN , PetID , Province , Street , Zipcode , Sub_district , district) VALUES (?,?,?,?,?,?,?,?);", userID, ssn, petID, province, street, zipcode, sub_district, district)
                if type == 'Dog':
                    cursor.execute("INSERT INTO Dog (PetID) VALUES (?);", petID)
                elif type == 'Cat':
                    cursor.execute("INSERT INTO Cat (PetID) VALUES (?);", petID)
        
        flash('Animal added successfully', 'success')
        return redirect(url_for('addition'))
    
    return render_template('addition.html')

def upload(petID):
    if 'photo' not in request.files:
        return 'No file part'
    
    photo = request.files['photo']

    if photo.filename == '':
        return 'No selected file'

    if photo:
        filename = str(petID)  # Convert petID to string
        photo.save(os.path.join('static/photo', f'{filename}.jpg'))
        return 'File uploaded successfully'

@app.route('/myAddition', methods=['GET', 'POST'])
def myAddition():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        return redirect(url_for('login'))
    
    userID = session.get('userID')
    
    if request.method == 'GET':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Pet WHERE userID = ?;", userID)
                pets = cursor.fetchall() 
    return render_template('myAddition.html', pets=pets)

@app.route('/delete/<petID>', methods=['GET', 'POST'])
def delete(petID):

    message = None
    with pyodbc.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DECLARE @PetID INT = ?;
                DECLARE @Message NVARCHAR(255);
                IF EXISTS (SELECT 1 FROM UserRequest WHERE PetID = @PetID)
                    BEGIN
                        -- Set message if PetID exists in UserRequest table
                        SET @Message = 'Pet is currently in Request Pending.'
                        SELECT @Message AS Message
                    END
                ELSE
                BEGIN
                        SET @Message = 'Pet deleted successfully.'
                        SELECT @Message AS Message
                        DELETE FROM FoundPlace WHERE PetID = @PetID;
                        IF EXISTS (SELECT 1 FROM Cat WHERE PetID = @PetID)
                        BEGIN
                            DELETE FROM Cat WHERE PetID = @PetID
                        END

                        IF EXISTS (SELECT 1 FROM Dog WHERE PetID = @PetID)
                        BEGIN
                            DELETE FROM Dog WHERE PetID = @PetID
                        END
                        DELETE FROM Pet WHERE PetID = @PetID
                END
                
                """, petID)
            
            row = cursor.fetchone()
            print(row)
            message = row.Message
            print(message)
            
            if message == 'Pet is currently in Request Pending.':
                print(message)
                flash(message, 'error')
            elif message == 'Pet deleted successfully.':
                print(message)
                flash(message, 'success')

    return redirect(url_for('myAddition'))

@app.route('/UpdatePet/<petID>', methods=['GET', 'POST'])
def UpdatePet(petID):
    if 'userID' not in session:
        flash('Please log in first', 'info')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
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
        # Location
        ssn = session.get('ssn')
        province = request.form.get('province')
        street = request.form.get('street')
        zipcode = request.form.get('zipcode')
        sub_district = request.form.get('sub_district')
        district = request.form.get('district')

        if not petID:  # If petID is not provided, insert a new record
            petID = str(random.randint(10000, 99999))  # Generate a new petID
            upload(petID)  # Upload the photo

        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    IF EXISTS (SELECT 1 FROM Pet WHERE PetID = ?)
                    BEGIN
                        UPDATE Pet
                        SET name = ?, breed = ?, size = ?, gender = ?, age = ?, behaviour = ?, sterilization = ?, hair_color = ?, foundDate = ?
                        WHERE PetID = ?;
                    END
                    ELSE
                    BEGIN
                        INSERT INTO Pet (PetID, name, breed, size, gender, age, behaviour, sterilization, hair_color, foundDate, userID, ImageID)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    END;
                """, petID, name, breed, size, gender, age, behaviour, sterilisation, colors, foundDate, petID, petID, name, breed, size, gender, age, behaviour, sterilisation, colors, foundDate, userID, petID)

                cursor.execute("""
                                    IF EXISTS (SELECT 1 FROM FoundPlace WHERE PetID = ?)
                                    BEGIN
                                        UPDATE FoundPlace
                                        SET userID = ?, SSN = ?, Province = ?, Street = ?, Zipcode = ?, Sub_district = ?, district = ?
                                        WHERE PetID = ?;
                                    END
                                    ELSE
                                    BEGIN
                                        INSERT INTO FoundPlace (userID, SSN, PetID, Province, Street, Zipcode, Sub_district, district)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                                    END;
                                """, petID, userID, ssn, province, street, zipcode, sub_district, district, petID, userID, ssn, province, street, zipcode, sub_district, district, petID)
                if type == 'Dog':
                    cursor.execute("INSERT INTO Dog (PetID) VALUES (?);", petID)
                elif type == 'Cat':
                    cursor.execute("INSERT INTO Cat (PetID) VALUES (?);", petID)
        
        flash('Animal Profile edit successfully', 'success')
        return redirect(url_for('myAddition'))
    
    with pyodbc.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Pet WHERE PetID = ?;", petID)
            pet = cursor.fetchone()
            
            cursor.execute("SELECT * FROM FoundPlace WHERE PetID = ?;", petID)
            found_place = cursor.fetchone()

    return render_template('UpdatePet.html', pet=pet, found_place=found_place)


@app.route('/filter')
def filter_pets():
    category = request.args.get('category')
    color = request.args.get('color')
    gender = request.args.get('gender')
    sterilization = request.args.get('sterilization')

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Construct SQL query based on filter inputs
        query = "SELECT * FROM Pet WHERE 1=1"
        params = []

        if category == 'cat':
            query += " AND EXISTS (SELECT 1 FROM Cat C WHERE C.petID = Pet.PetID)"
        elif category == 'dog':
            query += " AND EXISTS (SELECT 1 FROM Dog D WHERE D.PetID = Pet.PetID)"

        if color != 'all':
            colors = color.split(',')
            query += f" AND hair_color IN ({','.join(['?'] * len(colors))})"
            params.extend(colors)
        if gender != 'all':
            query += " AND gender = ?"
            params.append(gender)
        if sterilization != 'all':
            query += " AND sterilization = ?"
            params.append(sterilization)

        cursor.execute(query, params)
        pets = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    except pyodbc.Error as e:
        # Handle errors
        return jsonify([])  # Return an empty list if an error occurs
    finally:
        cursor.close()
        conn.close()

    return jsonify(pets)

@app.route('/petprofile')
def ViewPetProfile():
    pet_id = request.args.get('PetID')
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = """
            SELECT Pet.*, [User].name AS Uname
            FROM Pet 
            INNER JOIN [User] ON Pet.userID = [User].userID 
            WHERE Pet.PetID = ?
            """
            
        cursor.execute(query, (pet_id,))
        pet = cursor.fetchone()
        pet_dict = dict(zip([column[0] for column in cursor.description], pet))
    except pyodbc.Error as e:
        # Handle errors
        return "Error fetching pet data"

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('PetProfile', pet_data=json.dumps(pet_dict)))

@app.route('/PetProfile.html')
def PetProfile():
    pet_data = json.loads(request.args.get('pet_data'))
    return render_template('PetProfile.html', pet_data=pet_data)

@app.route('/adopt', methods=['POST'])
def adopt_pet():

    if 'userID' not in session:
        flash('Please log in first', 'info')
        print("Login")
        return redirect(url_for('login'))
    
    data = request.json
    petID = data['petID']
    userID = session.get('userID')
    requestID = str(random.randint(10000, 99999))
    date = datetime.now().strftime('%Y-%m-%d')
    approve = 0
    
    print('userID : ',userID)
    print('petid : ', petID)
    
    if request.method == 'POST':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                 # Check if petID and userID already exist in UserRequest table
                cursor.execute("SELECT COUNT(*) FROM UserRequest WHERE PetID = ? AND userID = ?", petID, userID)
                if cursor.fetchone()[0] > 0:
                    flash('Adoption request for this pet already exists.', 'error')
                    print("Exists")
                    return redirect(url_for('homepage'))
                else:
                    cursor.execute("""  
                    DECLARE @SSN VARCHAR(17);
                    SET @SSN = (SELECT [User].SSN FROM [User] WHERE userID = ?)           
                        
                    INSERT INTO UserRequest (requestID,userID,SSN,PetID,[date],approve_request)
                    VALUES (?,?,@SSN,?,?,?);           
                                
                    """,userID,requestID,userID,petID,date,approve)
                    print("Success")
                    flash('Your adoption request has been submitted.', 'success')    
    print("Finish")
    return redirect(url_for('homepage'))                
    


@app.route('/statusUser', methods=['GET', 'POST'])
def statusUser():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        return redirect(url_for('login'))
    
    userID = session.get('userID')
    print("userID:", userID)
    
    if request.method == 'GET':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT Pet.name, UserRequest.date, UserRequest.approve_request,UserRequest.requestID
                    FROM UserRequest
                    JOIN Pet ON UserRequest.PetID = Pet.PetID
                    WHERE UserRequest.userID = ?;
                """, userID)
                pets = cursor.fetchall() 
    return render_template('StatusUser.html', pets=pets)

@app.route('/StatusAdmin')
def StatusAdmin():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT Pet.name, UserRequest.date, UserRequest.approve_request,UserRequest.userID,UserRequest.requestID
                    FROM UserRequest
                    JOIN Pet ON UserRequest.PetID = Pet.PetID
                """)
                requests = cursor.fetchall()
    return render_template('StatusAdmin.html',requests=requests)

@app.route('/PermissionFormAdmin')
def PermissionFormAdmin():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        print("Login")
        return redirect(url_for('login'))
    
    requestID = request.args.get('requestID')
    
    if request.method == 'GET':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT  
                        UR.approve_request,
                        UR.userID,
                        UR.requestID,
                        P.*,
                        FP.*,
                        U.name,
                        E.score
                    FROM UserRequest UR
                    JOIN Pet P ON UR.PetID = P.PetID
                    LEFT JOIN FoundPlace FP ON UR.PetID = FP.PetID
                    JOIN [User] U ON UR.userID = U.userID
                    LEFT JOIN Exam E ON UR.userID = E.userID
                    WHERE requestID = ?
                """,requestID)
                request_data = cursor.fetchall()
    print(request_data)           
    return render_template('PermissionFormAdmin.html',request=request_data)

@app.route('/PermissionFormUser')
def PermissionFormUser():
    if 'userID' not in session:
        flash('Please log in first', 'info')
        print("Login")
        return redirect(url_for('login'))
    
    requestID = request.args.get('requestID')
    
    if request.method == 'GET':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT  
                        UR.approve_request,
                        UR.userID,
                        UR.requestID,
                        P.*,P.name AS petName,
                        FP.*,
                        U.name,
                        E.score
                    FROM UserRequest UR
                    JOIN Pet P ON UR.PetID = P.PetID
                    LEFT JOIN FoundPlace FP ON UR.PetID = FP.PetID
                    JOIN [User] U ON UR.userID = U.userID
                    LEFT JOIN Exam E ON UR.userID = E.userID
                    WHERE requestID = ?
                """,requestID)
                request_data = cursor.fetchall()
    print(request_data)      
    return render_template('PermissionFormUser.html',request=request_data)

@app.route('/api/permission', methods=['POST'])
def handle_permission():
    
    if 'userID' not in session:
        flash('Please log in first', 'info')
        print("Login")
        return redirect(url_for('login'))
    
    requestID = request.form.get('requestID')
    permission = request.form['permission']
    if request.method == 'POST':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                
                if(permission == 'APPROVE'):
                    cursor.execute("""
                        UPDATE UserRequest
                        SET approve_request = ?
                        WHERE requestID = ?;
                    """, 1, requestID)
                else:
                    cursor.execute("""
                        DELETE FROM UserRequest
                        WHERE requestID = ? ;
                    """, requestID)
    return redirect(url_for('StatusAdmin'))

@app.route('/delete_request/<requestID>', methods=['DELETE'])
def delete_request(requestID):
    if 'userID' not in session:
        flash('Please log in first', 'info')
        print("Login")
        return redirect(url_for('login'))

    if request.method == 'DELETE':
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM UserRequest
                        WHERE requestID = ? ;
                    """, requestID)
    
    flash('Request deleted successfully', 'success')
    return jsonify({'redirect': url_for('statusUser')}), 200

if __name__ == '__main__':
    app.run(debug=True)
