from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

<<<<<<< HEAD
# Database configuration
db_config = {
    'host': 'your-database-host',     # Replace with your database host URL
    'user': 'your-database-user',     # Replace with your database username
    'password': 'your-database-password',  # Replace with your database password
    'database': 'vehicle_tracking_db' # Replace with your database name
}

# Home route to render HTML dashboard
=======
# Database Configuration
db_config = {
    'host': 'sql.freehost.com',  # Replace with your free hosting SQL server
    'user': 'your_user',         
    'password': 'your_password',  
    'database': 'vehicle_tracking_db'
}

def get_connection():
    return mysql.connector.connect(**db_config)

>>>>>>> ce93ed2f804946a27e39ffcdd8acc82a880c5ff7
@app.route('/')
def index():
    return render_template('dashboard.html')

<<<<<<< HEAD
# Endpoint to receive location data from the Android app
@app.route('/location', methods=['POST'])
def location():
=======
@app.route('/location', methods=['POST'])
def update_location():
>>>>>>> ce93ed2f804946a27e39ffcdd8acc82a880c5ff7
    data = request.json
    driver_id = data['driver_id']
    name = data['name']
    mobile = data['mobile']
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
<<<<<<< HEAD
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO driver_location (driver_id, name, mobile, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (driver_id, name, mobile, latitude, longitude, timestamp)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Location saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
=======
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
>>>>>>> ce93ed2f804946a27e39ffcdd8acc82a880c5ff7
