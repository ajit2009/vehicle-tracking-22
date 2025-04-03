from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration
def get_connection():
    return mysql.connector.connect(
        host='sql7.freesqldatabase.com',       # Server address
        user='sql7770632',                     # Your database username
        password='rW4FZ1M34e',                # Your database password
        database='sql7770632',                 # Your database name
        port=3306                             # Default MySQL port
    )

@app.route('/')
def index():
    return render_template('dashboard.html')  # Ensure 'dashboard.html' exists in the 'templates' folder

@app.route('/location', methods=['POST'])
def location():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415

    data = request.get_json()
    
    try:
        driver_id = data['driver_id']
        driver_name = data['driver_name']
        driver_mobile = data['driver_mobile']
        latitude = data['latitude']
        longitude = data['longitude']
    except KeyError:
        return jsonify({"error": "Invalid JSON format"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
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
        # Retrieve the latest location for each driver
        cursor.execute("SELECT * FROM driver_location;")
        locations = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
