from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Replace with your own connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=db_test;"
    "UID=sa;"
    "PWD=Choky999;"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Name VALUES (?);", name)
        return redirect(url_for('home'))
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)