import os

from flask import Flask, render_template, request, jsonify
import sqlite3
from sqlalchemy import create_engine

app = Flask(__name__)

#import images
IMAGES_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER



# Initialize SQLite database
def init_db():
    engine = create_engine('sqlite:///parking.db')
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                        spot_id INTEGER PRIMARY KEY,
                        reserved INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'empty_parking.jpg')
    return render_template("index.html", empty_parking=full_filename)
@app.route('/index.html')
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'empty_parking.jpg')
    return render_template("index.html", empty_parking=full_filename)

@app.route('/availability.html')
def avl():
    return render_template('availability.html')

@app.route('/login.html')
def log():
    return render_template('login.html')

@app.route('/register.html')
def reg():
    return render_template('register.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    spot_id = request.json.get('spot_id')
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservations (spot_id, reserved) VALUES (?, ?)', (spot_id, 1))
    conn.commit()
    conn.close()
    return jsonify({"message": "Reservation successful"}), 200


@app.route('/database.html')
def database():
    connect = sqlite3.connect('parking.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM reservations')

    data = cursor.fetchall()
    # Fetching column names from the cursor's description attribute
    column_names = [description[0] for description in cursor.description]

    connect.close()
    return render_template("database.html", data=data, columns=column_names)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
