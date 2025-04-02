
from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'sql7.freesqldatabase.com',
    'user': 'sql7770632',
    'password': 'rW4FZ1M34e',
    'database': 'sql7770632'
}

def get_connection():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/location', methods=['POST'])
def save_location():
    data = request.json
    driver_id = data['driver_id']
    driver_name = data['driver_name']
    driver_mobile = data['driver_mobile']
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_connection()
    cursor = conn.cursor()

    # Delete previous location of the driver before inserting the new one
    cursor.execute("""DELETE FROM driver_location WHERE driver_id = %s""", (driver_id,))
    
    # Insert the new location
    cursor.execute("""INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)""", (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp))
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Location saved successfully!'})

@app.route('/locations', methods=['GET'])
def get_locations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the latest location for each driver
    cursor.execute("""SELECT * FROM driver_location GROUP BY driver_id""")

    locations = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
