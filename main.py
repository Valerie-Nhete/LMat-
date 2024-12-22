from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running on Replit!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'app.db'

# Function to connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Function to initialize the database (create tables)
def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS vitals (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            heart_rate INTEGER,
                            blood_pressure TEXT,
                            temperature REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS diet (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            meal TEXT,
                            food TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.commit()

# Home route
@app.route('/')
def home():
    return "Welcome to the Flask backend with SQLite!"

# Route to handle POST request for vitals
@app.route('/api/vitals', methods=['POST'])
def handle_vitals():
    data = request.get_json()
    heart_rate = data.get("heart_rate")
    blood_pressure = data.get("blood_pressure")
    temperature = data.get("temperature")

    # Save the vitals data into the database
    with get_db() as conn:
        conn.execute('''INSERT INTO vitals (heart_rate, blood_pressure, temperature) 
                        VALUES (?, ?, ?)''', (heart_rate, blood_pressure, temperature))
        conn.commit()

    return jsonify({
        "message": "Vitals saved successfully",
        "data": {
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature
        }
    })

# Route to handle GET request for all vitals
@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    with get_db() as conn:
        vitals = conn.execute('SELECT * FROM vitals ORDER BY timestamp DESC').fetchall()

    vitals_list = []
    for vital in vitals:
        vitals_list.append({
            "heart_rate": vital["heart_rate"],
            "blood_pressure": vital["blood_pressure"],
            "temperature": vital["temperature"],
            "timestamp": vital["timestamp"]
        })

    return jsonify(vitals_list)

# Route to handle POST request for daily diet
@app.route('/api/diet', methods=['POST'])
def handle_diet():
    data = request.get_json()
    meal = data.get("meal")
    food = data.get("food")

    # Save the diet data into the database
    with get_db() as conn:
        conn.execute('''INSERT INTO diet (meal, food) 
                        VALUES (?, ?)''', (meal, food))
        conn.commit()

    return jsonify({
        "message": "Diet saved successfully",
        "data": {
            "meal": meal,
            "food": food
        }
    })

# Route to handle GET request for all diet entries
@app.route('/api/diet', methods=['GET'])
def get_diet():
    with get_db() as conn:
        diet_entries = conn.execute('SELECT * FROM diet ORDER BY timestamp DESC').fetchall()

    diet_list = []
    for entry in diet_entries:
        diet_list.append({
            "meal": entry["meal"],
            "food": entry["food"],
            "timestamp": entry["timestamp"]
        })

    return jsonify(diet_list)

# Initialize the database
init_db()

# Starting the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your Google API Key
API_KEY = "AIzaSyCYmU68TvDbrTFq9JIdz9rs6Yb-LqybVV4"
BASE_URL = "https://www.googleapis.com/fitness/v1/users/me"

@app.route('/datasources', methods=['GET', 'POST'])
def manage_data_sources():
    """List or Create Data Sources"""
    headers = {"Authorization": f"Bearer {request.headers.get('Authorization')}"}
    if request.method == 'POST':
        data = request.json  # JSON body for new data source
        response = requests.post(f"{BASE_URL}/dataSources?key={API_KEY}", headers=headers, json=data)
    else:
        response = requests.get(f"{BASE_URL}/dataSources?key={API_KEY}", headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/datasets/<data_source_id>/<dataset_id>', methods=['GET', 'PATCH'])
def manage_datasets(data_source_id, dataset_id):
    """Insert or Query Dataset"""
    headers = {"Authorization": f"Bearer {request.headers.get('Authorization')}"}
    if request.method == 'PATCH':
        data = request.json  # JSON body for new data points
        response = requests.patch(
            f"{BASE_URL}/dataSources/{data_source_id}/datasets/{dataset_id}?key={API_KEY}",
            headers=headers, json=data
        )
    else:
        response = requests.get(
            f"{BASE_URL}/dataSources/{data_source_id}/datasets/{dataset_id}?key={API_KEY}", headers=headers
        )
    return jsonify(response.json()), response.status_code

@app.route('/sessions', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_sessions():
    """List, Create, Update, or Delete Sessions"""
    headers = {"Authorization": f"Bearer {request.headers.get('Authorization')}"}
    session_id = request.args.get('session_id', '')
    if request.method == 'POST':
        data = request.json  # JSON body for new session
        response = requests.post(f"{BASE_URL}/sessions?key={API_KEY}", headers=headers, json=data)
    elif request.method == 'PUT':
        data = request.json  # JSON body for updated session
        response = requests.put(f"{BASE_URL}/sessions/{session_id}?key={API_KEY}", headers=headers, json=data)
    elif request.method == 'DELETE':
        response = requests.delete(f"{BASE_URL}/sessions/{session_id}?key={API_KEY}", headers=headers)
    else:
        response = requests.get(f"{BASE_URL}/sessions?key={API_KEY}", headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/aggregate', methods=['POST'])
def aggregate_data():
    """Aggregate Data"""
    headers = {"Authorization": f"Bearer {request.headers.get('Authorization')}"}
    data = request.json  # JSON body for aggregation
    response = requests.post(f"{BASE_URL}/dataset:aggregate?key={API_KEY}", headers=headers, json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)