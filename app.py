from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

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
if __name__ == '__main__':
    app.run(debug=True)