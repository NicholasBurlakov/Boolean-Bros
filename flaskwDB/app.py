from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                        id INTEGER PRIMARY KEY,
                        spot_id INTEGER,
                        reserved INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/index.html')
def index():
    return render_template('index.html')

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


@app.route('/participants.html') 
def participants(): 
    connect = sqlite3.connect('parking.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM reservations') 

    data = cursor.fetchall() 
    return render_template("participants.html", data=data) 

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
