from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Importing CORS for cross-origin requests handling
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow all domains to access this Flask app

# Database configuration
def get_connection():
    return mysql.connector.connect(
        host='sql7.freesqldatabase.com',
        user='sql7770632',
        password='rW4FZ1M34e',
        database='sql7770632',
        port=3306
    )

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/location', methods=['POST'])
def location():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON format or missing data"}), 400

    try:
        driver_id = data['driver_id']
        driver_name = data['driver_name']
        driver_mobile = data['driver_mobile']
        latitude = data['latitude']
        longitude = data['longitude']
        timestamp = data['timestamp']  # Now accepting timestamp from the request
    except KeyError:
        return jsonify({"error": "Invalid JSON keys. Make sure all keys are present."}), 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Insert or update the driver's latest location
        cursor.execute("""
            INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            driver_name = VALUES(driver_name), 
            driver_mobile = VALUES(driver_mobile), 
            latitude = VALUES(latitude), 
            longitude = VALUES(longitude),
            timestamp = VALUES(timestamp)
        """, (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp))

        connection.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Location updated successfully"}), 200

@app.route('/locations', methods=['GET'])
def locations():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT driver_id, driver_name, driver_mobile, latitude, longitude, timestamp
            FROM driver_location
            GROUP BY driver_id;
        """)
        locations = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
