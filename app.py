from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_config import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    driver_id = data.get('driver_id')
    driver_name = data.get('driver_name')
    driver_mobile = data.get('driver_mobile')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO driver_location (driver_id, driver_name, driver_mobile, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s)
        """, (driver_id, driver_name, driver_mobile, latitude, longitude))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Location data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM driver_location")
        locations = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(locations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
