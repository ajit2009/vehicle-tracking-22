from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'sql.freehost.com',       # Replace with your free hosting SQL server
    'user': 'your_user',               # Replace with your database username
    'password': 'your_password',       # Replace with your database password
    'database': 'vehicle_tracking_db'  # Replace with your database name
}

def get_connection():
    return mysql.connector.connect(**db_config)

# Home route to render HTML dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')

# Endpoint to receive location data from the Android app
@app.route('/location', methods=['POST'])
def update_location():
    data = request.json
    driver_id = data['driver_id']
    name = data['name']
    mobile = data['mobile']
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO driver_location (driver_id, name, mobile, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (driver_id, name, mobile, latitude, longitude, timestamp))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Location updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve all locations
@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM driver_location")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        locations = []
        for row in rows:
            locations.append({
                'driver_id': row[0],
                'name': row[1],
                'mobile': row[2],
                'latitude': row[3],
                'longitude': row[4],
                'timestamp': row[5]
            })
        
        return jsonify(locations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
