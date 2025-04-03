from flask import Flask, request, jsonify
from db_config import get_connection
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Vehicle Tracking API is running."

@app.route('/location', methods=['POST'])
def location():
    try:
        if request.is_json:
            # Handle JSON data
            data = request.json
        else:
            # Handle Form Data
            data = request.form.to_dict()

        # Extracting data from the request
        driver_id = data.get('driver_id')
        name = data.get('name')
        mobile = data.get('mobile')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if all required fields are present
        if not all([driver_id, name, mobile, latitude, longitude]):
            return jsonify({"error": "Missing data fields"}), 400

        # Connect to the database
        connection = get_connection()
        cursor = connection.cursor()

        # Remove the previous entry for the same driver (to keep only the last location)
        cursor.execute("DELETE FROM driver_location WHERE driver_id = %s", (driver_id,))

        # Insert new location
        cursor.execute("""
            INSERT INTO driver_location (driver_id, name, mobile, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (driver_id, name, mobile, latitude, longitude, timestamp))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Location saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/locations', methods=['GET'])
def locations():
    try:
        # Connect to the database
        connection = get_connection()
        cursor = connection.cursor()

        # Retrieve only the last recorded location of each driver
        cursor.execute("""
            SELECT DISTINCT ON (driver_id) driver_id, name, mobile, latitude, longitude, timestamp
            FROM driver_location
            ORDER BY driver_id, timestamp DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        # Convert the results to a list of dictionaries
        result = [{"driver_id": row[0], "name": row[1], "mobile": row[2], "latitude": row[3], "longitude": row[4], "timestamp": row[5]} for row in rows]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
