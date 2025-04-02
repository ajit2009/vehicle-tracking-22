from flask import Flask, request, jsonify
import mysql.connector
from db_config import get_connection

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def location():
    try:
        data = request.json
        driver_id = data['driver_id']
        driver_name = data['driver_name']
        driver_mobile = data['driver_mobile']
        latitude = data['latitude']
        longitude = data['longitude']
        
        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (driver_id, driver_name, driver_mobile, latitude, longitude))
        conn.commit()

        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location saved successfully"}), 200

    except Exception as e:
        print(e)  # This will show the error in your Render logs
        return jsonify({"error": "Failed to save location"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
