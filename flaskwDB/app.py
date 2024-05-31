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
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                    SpotID INTEGER NOT NULL,
                    ParkingLotID INTEGER NOT NULL,
                    VehicleID INTEGER NOT NULL,
                    StartTime DATETIME NOT NULL,
                    EndTime DATETIME NOT NULL,
                    FOREIGN KEY (SpotID) REFERENCES ParkingSpot(SpotID),
                    FOREIGN KEY (ParkingLotID) REFERENCES ParkingLot(ParkingLotID),
                    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID));
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ParkingLot (
    ParkingLotID INTEGER PRIMARY KEY AUTOINCREMENT,
    OwnerID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Location TEXT NOT NULL,
    Capacity INTEGER NOT NULL,
    FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID)
);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ParkingSpot (
    SpotID INTEGER PRIMARY KEY AUTOINCREMENT,
    ParkingLotID INTEGER NOT NULL,
    SpotNumber INTEGER NOT NULL,
    IsAvailable BOOLEAN NOT NULL,
    FOREIGN KEY (ParkingLotID) REFERENCES ParkingLot(ParkingLotID)
);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Vehicle (
    VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    LicensePlate TEXT NOT NULL UNIQUE,
    State TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES RegisteredUser(UserID)
);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS RegisteredUser (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Owner (
    OwnerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    PhoneNumber TEXT NOT NULL
);''')

    # cursor.execute('''DROP TABLE IF EXISTS reservations''')
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
    tables = []
    table_names = ['Reservations', 'ParkingLot', 'ParkingSpot', 'Vehicle', 'RegisteredUser', 'Owner']

    connect = sqlite3.connect('parking.db')
    cursor = connect.cursor()

    for table_name in table_names:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        # Fetching column names from the cursor's description attribute
        column_names = [description[0] for description in cursor.description]
        tables.append((table_name, column_names, data))

    connect.close()
    return render_template("database.html", tables=tables)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
