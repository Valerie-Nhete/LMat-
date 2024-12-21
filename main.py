from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running on Replit!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
users = {}
vitals = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    users[data['id']] = data
    return jsonify({"message": "User registered successfully!"})

@app.route('/submit_vitals', methods=['POST'])
def submit_vitals():
    data = request.json
    vitals[data['id']] = data['vitals']
    return jsonify({"message": "Vitals recorded!"})

@app.route('/education', methods=['GET'])
def education():
    return jsonify({"content": "Eat well, rest, and stay hydrated!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)