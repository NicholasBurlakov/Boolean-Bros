import datetime
import os

from flask import Flask, render_template, request, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "Boolean_Bros_Rule"

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
                    ParkingLotID INTEGER,
                    VehicleID INTEGER,
                    StartTime DATETIME,
                    EndTime DATETIME,
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
    Username TEXT NOT NULL UNIQUE,
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


    conn.commit()
    conn.close()

@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'empty_parking.jpg')
    if 'username' in session:
        return render_template("userHome", empty_parking=full_filename, username=session['username'])
    else:
        return render_template("index.html", empty_parking=full_filename)
@app.route('/index.html')
def index():
    return home()

@app.route('/availability.html')
def avl():
    if 'username' in session:
        return render_template('userAvailability.html', username=session['username'])
    else:
        return render_template('availability.html')

@app.route('/login.html')
def log():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/userHome')
def userHome():
    return home()


@app.route('/userProfile.html')
def userProfile():
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Email FROM RegisteredUser WHERE Username = ?", (session['username'],))
    session['email'] = cursor.fetchone()[0]

    return render_template("userProfile.html", username=session['username'], email=session['email'])


@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    spot_id = data.get('spot_id')
    parking_lot_id = data.get('parking_lot_id', 1)  # Assuming a default parking lot ID
    vehicle_id = data.get('vehicle_id', 1)  # Assuming a default vehicle ID
    start_time = data.get('start_time', '2024-01-01 00:00:00')  # Default start time
    end_time = data.get('end_time', '2024-12-31 00:00:00')  # Default end time

    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reservations (SpotID, ParkingLotID, VehicleID, StartTime, EndTime) 
                      VALUES (?, ?, ?, ?, ?)''',
            (spot_id, parking_lot_id, vehicle_id, start_time, end_time))
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

@app.route('/login.html', methods=["POST"])
def loginUser():
    #Ensures this can only be accessed through POST request
    if request.method == "POST":

        print(session)
        #If user is already logged in
        if 'username' in session:
            return render_template("login.html", error_message="User already logged in")

        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()

        # From HTML
        username = request.form['username']
        password = request.form['password']

        #SQL
        cursor.execute("SELECT Username, Password FROM RegisteredUser WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchall()
        conn.close()

        #If username and password are correct...
        if len(result) > 0:
            #Redirect to loggedin home page
            session['username'] = username
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'empty_parking.jpg')
            return render_template("userHome", empty_parking=full_filename, username=username)
        #If username or password are incorrect...
        else:
            return render_template("login.html", error_message="Invalid username or password")

    #If not POST request
    return render_template("login.html")

@app.route('/register.html', methods=["POST"])
def registerUser():
    #Ensures this can only be accessed through POST request
    if request.method == "POST":
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()

        # From HTML
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username, email, password)

        #SQL
        #Checks if username or email already exists
        cursor.execute("SELECT Username, Email FROM RegisteredUser WHERE Username = ? and Email = ?", (username, email))
        result = cursor.fetchall()

        #If username or email already exist...
        if len(result) > 0:
            session['username'] = username
            conn.close()
            return render_template("register.html", error_message="Username or email already exists")
        #If username or email are unique insert into database
        else:
            cursor.execute("INSERT INTO RegisteredUser (Username, Email, Password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()

            #Redirect to loggedin home page
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'empty_parking.jpg')
            return render_template("userHome", empty_parking=full_filename, username=username)

        conn.close()


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    return home()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
