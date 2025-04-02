from flask import Flask, request, jsonify
import mysql.connector
from db_config import get_connection
from datetime import datetime
import logging

app = Flask(__name__)

# Setup logging to print errors to Render logs
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def index():
    return "Vehicle Tracking Backend is running!"

@app.route('/location', methods=['POST'])
def location():
    try:
        data = request.json

        # Retrieve data from the request
        driver_id = data['driver_id']
        driver_name = data['driver_name']
        driver_mobile = data['driver_mobile']
        latitude = data['latitude']
        longitude = data['longitude']
        timestamp = datetime.now()

        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Insert data into the table
        query = """
            INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (driver_id, driver_name, driver_mobile, latitude, longitude, timestamp))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Location saved successfully"}), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Failed to save location"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
