import mysql.connector
from flask import Flask, render_template, request, redirect, url_for,session
from datetime import datetime


app = Flask(__name__)
app.secret_key='hetvik'
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hetvikpatel'
}


def connect_db():
    return mysql.connector.connect(**db_config)


def create_hetvik1_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hetvik1(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()


def create_reserve1_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reserve1(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    people INT NOT NULL,
    phone VARCHAR(255) NOT NULL,
    dates DATE NOT NULL,
    times VARCHAR(255) NOT NULL,
    msg VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()


def create_connect_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS connect(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    message VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()


create_hetvik1_table()
create_reserve1_table()
create_connect_table()


@app.route('/', methods=['GET'])
def index1():
    return render_template('signup.html')

@app.route('/new1', methods=['POST'])
def signup():
    mesage=''
    if request.method == 'POST'and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        con = connect_db()
        cur = con.cursor()
        cur.execute("select * from hetvik1 where email=%s", (email,))
        acc = cur.fetchone()
        if acc:
            mesage = 'Already Exist! '
        elif password != confirm_password:
            mesage = 'Password Does Not Match!'
        else:
            try:

                cur.execute("INSERT INTO hetvik1(email, password) VALUES (%s, %s)", (email, password))
                con.commit()
                cur.close()
                con.close()
                return redirect(url_for('restaurant'))
            except Exception as e:
                print("Error inserting values:", e)
                return 'Error inserting values'
        return render_template('signup.html', mesage=mesage)


@app.route('/new',methods=['GET','POST'])
def login1():
    mesage=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password =request.form['password']
        con = connect_db()
        cur = con.cursor()
        cur.execute('select * from hetvik1 where email=%s and password=%s', (email, password))
        user=cur.fetchone()
        if user:
            session['logged_in'] = True
            session['email'] = user[0]
            session['password'] =user[1]
            mesage='logged in successfully'
            return redirect(url_for('index'))
        else:
            mesage='Invalid email or password'
            return render_template('restaurant.html', mesage=mesage)
    return render_template('restaurant.html')
@app.route('/login')
def restaurant():
    return render_template('restaurant.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/submit_reserve', methods=['POST'])
def submit_reserve():
    try:
        # Retrieve form data
        fname = request.form['fname']
        lname = request.form['lname']
        Email = request.form['Email']
        people = request.form['people']
        phone = request.form['phone']
        R_date_str = request.form['dates']
        R_date_obj = datetime.strptime(R_date_str, '%m/%d/%Y')
        R_date = R_date_obj.strftime('%Y-%m-%d')

        # Time
        R_time_str = request.form['times']
        R_time_obj = datetime.strptime(R_time_str, '%I:%M%p').strftime('%H:%M:%S')
        msg = request.form['msg']

        # Insert data into database
        con = connect_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO reserve1 (fname, lname, Email, people, phone, dates, times, msg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (fname, lname, Email, people, phone,R_date, R_time_obj, msg)
        )
        con.commit()
        cur.close()
        con.close()
        return 'Your table is reserved'
    except Exception as e:
        print("Problem with insertion:", e)
        return 'Error inserting values'

@app.route('/submit_connect', methods=['POST'])
def submit_connect():
    name = request.form['name']
    EMAIL = request.form['EMAIL']
    message = request.form['message']
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("INSERT INTO connect(name, EMAIL, message) VALUES (%s, %s, %s)",
                    (name,EMAIL,message))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for('index'))
    except Exception as e:
        print("Problem with insertion:", e)
        return 'Error inserting values'


if __name__ == '__main__':
    app.run()
