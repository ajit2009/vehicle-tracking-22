from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # For handling CORS issues
import logging
import mysql.connector
from db_config import get_connection

app = Flask(__name__, template_folder='templates')
CORS(app)  # Allow Cross-Origin requests

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Test Route to Check Database Connectivity
@app.route('/test', methods=['GET'])
def test():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({"tables": tables}), 200
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return jsonify({"error": str(e)}), 500

# Route to handle incoming location data (POST Request)
@app.route('/location', methods=['POST'])
def location():
    try:
        data = request.json  # Ensure JSON data is parsed correctly
        logging.debug(f"Received data: {data}")
        
        driver_id = data.get('driver_id')
        driver_name = data.get('driver_name')
        driver_mobile = data.get('driver_mobile')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not all([driver_id, driver_name, driver_mobile, latitude, longitude]):
            logging.error("Missing fields in the request data")
            return jsonify({"error": "Missing fields"}), 400

        connection = get_connection()
        cursor = connection.cursor()

        # Insert or Update the latest location for the driver
        cursor.execute("""
            INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE 
            driver_name = VALUES(driver_name), 
            driver_mobile = VALUES(driver_mobile), 
            latitude = VALUES(latitude), 
            longitude = VALUES(longitude), 
            timestamp = NOW();
        """, (driver_id, driver_name, driver_mobile, latitude, longitude))

        connection.commit()
        cursor.close()
        connection.close()

        logging.info("Location updated successfully")
        return jsonify({"message": "Location updated successfully"}), 200

    except Exception as e:
        logging.error(f"Error in /location endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Route to retrieve all latest locations (GET Request)
@app.route('/locations', methods=['GET'])
def locations():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Retrieve only the latest location for each driver
        cursor.execute("""
            SELECT driver_id, driver_name, driver_mobile, latitude, longitude, timestamp
            FROM driver_location;
        """)
        
        locations = cursor.fetchall()
        
        cursor.close()
        connection.close()

        logging.info("Locations retrieved successfully")
        return jsonify(locations), 200

    except Exception as e:
        logging.error(f"Error in /locations endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Serve the dashboard HTML file at the root URL
@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
