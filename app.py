from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return "Backend is running"

@app.route('/api/places', methods=['GET'])
def get_places():
    places = [
        {"id": 1, "name": "Ranchi", "description": "Capital city of Jharkhand"},
        {"id": 2, "name": "Jamshedpur", "description": "Steel city of India"},
        {"id": 3, "name": "Dhanbad", "description": "Coal capital of India"},
        {"id": 4, "name": "Deoghar", "description": "Temple town"},
        {"id": 5, "name": "Hazaribagh", "description": "Famous for wildlife sanctuary"}
    ]
    return jsonify(places)

@app.route('/api/book-guide', methods=['POST'])
def book_guide():
    data = request.get_json()
    response = {
        "success": True,
        "message": "Guide booking successful",
        "data": data
    }
    return jsonify(response)

@app.route('/api/book-transport', methods=['POST'])
def book_transport():
    data = request.get_json()
    response = {
        "success": True,
        "message": "Transport booking successful",
        "data": data
    }
    return jsonify(response)

@app.route('/api/book-activity', methods=['POST'])
def book_activity():
    data = request.get_json()
    response = {
        "success": True,
        "message": "Activity booking successful",
        "data": data
    }
    return jsonify(response)

@app.route('/api/admin/guide-bookings', methods=['GET'])
def get_guide_bookings():
    bookings = [
        {"name": "John Doe", "phone": "+91 9876543210", "email": "john@email.com", "language": "English, Hindi", "places": "Ranchi, Deoghar", "date": "2024-01-15"},
        {"name": "Jane Smith", "phone": "+91 8765432109", "email": "jane@email.com", "language": "Hindi", "places": "Jamshedpur", "date": "2024-01-16"}
    ]
    return jsonify(bookings)

@app.route('/api/admin/transport-bookings', methods=['GET'])
def get_transport_bookings():
    bookings = [
        {"name": "Mike Johnson", "phone": "+91 7654321098", "email": "mike@email.com", "pickup": "Ranchi Airport", "destination": "Deoghar", "vehicle": "SUV", "date": "2024-01-17"},
        {"name": "Sarah Wilson", "phone": "+91 6543210987", "email": "sarah@email.com", "pickup": "Jamshedpur", "destination": "Hazaribagh", "vehicle": "Sedan", "date": "2024-01-18"}
    ]
    return jsonify(bookings)

@app.route('/api/admin/activity-bookings', methods=['GET'])
def get_activity_bookings():
    bookings = [
        {"name": "David Brown", "phone": "+91 5432109876", "email": "david@email.com", "activity": "Wildlife Safari", "location": "Hazaribagh National Park", "participants": "4", "date": "2024-01-19"},
        {"name": "Lisa Davis", "phone": "+91 4321098765", "email": "lisa@email.com", "activity": "Temple Tour", "location": "Deoghar", "participants": "2", "date": "2024-01-20"}
    ]
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)