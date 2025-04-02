from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_config import get_connection


app = Flask(__name__)

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
def location():
    data = request.json
    driver_id = data['driver_id']
    driver_name = data['driver_name']
    driver_mobile = data['driver_mobile']
    latitude = data['latitude']
    longitude = data['longitude']

    connection = get_connection()
    cursor = connection.cursor()

    # Insert or update the driver's latest location
    cursor.execute("""
        INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        driver_name = VALUES(driver_name), 
        driver_mobile = VALUES(driver_mobile), 
        latitude = VALUES(latitude), 
        longitude = VALUES(longitude);
    """, (driver_id, driver_name, driver_mobile, latitude, longitude))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Location updated successfully"}), 200

@app.route('/locations', methods=['GET'])
def locations():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Retrieve the latest location for each driver
    cursor.execute("""
        SELECT * FROM driver_location;
    """)
    locations = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
