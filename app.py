from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'sql7.freesqldatabase.com',       # FreeSQLDatabase.com host
    'user': 'sql7770632',                     # Your database username
    'password': 'rW4FZ1M34e',                # Your database password
    'database': 'sql7770632',                 # Your database name
    'port': 3306
}

@app.route('/')
def index():
    return render_template('dashboard.html')   # Ensure you have 'dashboard.html' in your templates folder

@app.route('/location', methods=['POST'])
def save_location():
    data = request.get_json()
    driver_id = data.get('driver_id')
    driver_name = data.get('driver_name')
    driver_mobile = data.get('driver_mobile')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Delete previous location for this driver to keep database light
        cursor.execute("DELETE FROM driver_location WHERE driver_id = %s", (driver_id,))
        
        # Insert the new location
        cursor.execute(
            "INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude) "
            "VALUES (%s, %s, %s, %s, %s)",
            (driver_id, driver_name, driver_mobile, latitude, longitude)
        )
        connection.commit()

        return jsonify({"message": "Location saved successfully!"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Retrieve the latest location of each driver
        cursor.execute("SELECT * FROM driver_location GROUP BY driver_id")
        locations = cursor.fetchall()

        return jsonify(locations), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
