import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)
db_config= {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hetvikpatel'
}


def connect_db():
    return mysql.connector.connect(**db_config)


def create_hetvik_table():
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


create_hetvik_table()


@app.route('/', methods=['GET'])
def index1():  # put application's code here
    return render_template('restaurant.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("insert into hetvik1(email,password) values(%s,%s)", (email, password))
        con.commit()
        cur.close()
        con.close()
        return 'inserted'
    except Exception as e:
        print("problem with insertion", e)
        return 'error inserting values'


if __name__ == '_main_':
    app.run()