from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123" 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1712",
        database="digital_Complaint"
    )

# HOME
@app.route('/')
def home():
    logged_in = 'user' in session
    return render_template('index.html', logged_in=logged_in)

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        rollNo = request.form.get('rollNo')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ADMIN LOGIN
        if rollNo == "20SS1A0011" and email == "adminSS20@gmail.com" and password == "admin@123":
            session['user'] = rollNo
            session['admin'] = True
            return redirect("/admin")

        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = rollNo

            login_time = datetime.now()

            cursor.execute(
                "INSERT INTO login_history(rollNo,email,login_time) VALUES(%s,%s,%s)",
                (rollNo, email, login_time)
            )

            conn.commit()
            conn.close()

            return redirect('/')
        else:
            conn.close()
            return "Invalid Email or Password ❌"

    return render_template("login.html")


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        rollNo = request.form.get('rollNo')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Email Already Registered"

        cursor.execute(
            "INSERT INTO users(rollNo,email,password) VALUES(%s,%s,%s)",
            (rollNo, email, password)
        )

        register_time = datetime.now()

        cursor.execute(
            "INSERT INTO register_history(rollNo,email,register_time) VALUES(%s,%s,%s)",
            (rollNo, email, register_time)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")
#descriptive complaint

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():

    if 'user' not in session:
        return redirect('/login')

    rollNo = session['user']
    description = request.form.get('description')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO complaints(rollNo, description, created_at) VALUES(%s,%s,%s)",
        (rollNo, description, datetime.now())
    )
    conn.commit()
    conn.close()

    flash("Complaint submitted successfully ✅")
    return redirect('/')

# ADMIN 
@app.route('/admin')
def admin():

    if 'admin' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM login_history")
    login_records = cursor.fetchall()

    cursor.execute("SELECT * FROM register_history")
    register_records = cursor.fetchall()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        login_records=login_records,
        register_records=register_records,
        complaints=complaints
    )

if __name__ == '__main__':
    app.run(debug=True)