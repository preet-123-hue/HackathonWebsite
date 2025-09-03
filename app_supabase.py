from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type', 'Accept'])

# Handle preflight OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,POST,OPTIONS")
        return response

# Log all requests
@app.before_request
def log_request():
    if request.method != 'OPTIONS':  # Skip OPTIONS preflight logs
        print(f"\n=== {request.method} {request.path} ===")
    
# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    print(f"\n=== 404 ERROR ===")
    print(f"Path: {request.path}")
    print(f"Method: {request.method}")
    return jsonify({"success": False, "message": f"Route {request.path} not found"}), 404

# Supabase configuration
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("ERROR: Missing Supabase credentials in .env file")
    print("Please add SUPABASE_URL and SUPABASE_KEY to your .env file")
    exit(1)

print(f"Supabase URL: {url[:30]}...")
print(f"Supabase Key: {key[:20]}...")

try:
    supabase: Client = create_client(url, key)
    print("Supabase client initialized")
except Exception as e:
    print(f"Failed to initialize Supabase: {e}")
    exit(1)

@app.route('/')
def root():
    return "Backend is running"

@app.route('/api/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

@app.route('/api/book', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No JSON data received"}), 400
        
        booking_type = data.get('booking_type')
        table_name = f"{booking_type}_bookings" if booking_type in ['guide', 'transport', 'activity'] else 'user_bookings'
        
        print(f"\n=== CREATING {booking_type.upper()} BOOKING ===")
        print(f"Table: {table_name}")
        
        result = supabase.table(table_name).insert(data).execute()
        
        if hasattr(result, 'data') and result.data:
            print("SUCCESS: Booking created successfully")
            return jsonify({"success": True, "message": "Booking created successfully", "data": result.data})
        else:
            return jsonify({"success": False, "message": "Failed to insert booking"}), 500
            
    except Exception as e:
        print(f"EXCEPTION in create_booking: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/book-guide', methods=['POST'])
def book_guide():
    try:
        print("\n=== GUIDE BOOKING REQUEST ===")
        data = request.get_json()
        print(f"Guide data: {json.dumps(data, indent=2)}")
        
        if not data:
            return jsonify({"success": False, "message": "No JSON data received"}), 400
        
        # Map frontend fields to database fields
        guide_data = {
            'full_name': data.get('name'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'preferred_language': data.get('language'),
            'places_of_interest': data.get('places', []),
            'date': data.get('date')
        }
        
        result = supabase.table('guide_bookings').insert(guide_data).execute()
        print(f"Supabase result: {result}")
        
        if hasattr(result, 'data') and result.data:
            print("SUCCESS: Guide booking created")
            return jsonify({"success": True, "message": "Guide booking successful", "data": result.data})
        else:
            return jsonify({"success": False, "message": "Failed to create guide booking"}), 500
            
    except Exception as e:
        print(f"EXCEPTION in book_guide: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/book-transport', methods=['POST'])
def book_transport():
    try:
        print("\n=== TRANSPORT BOOKING REQUEST ===")
        data = request.get_json()
        print(f"Transport data: {json.dumps(data, indent=2)}")
        
        if not data:
            return jsonify({"success": False, "message": "No JSON data received"}), 400
        
        # Map frontend fields to database fields
        transport_data = {
            'full_name': data.get('name'),
            'pickup_location': data.get('pickup_location'),
            'destination': data.get('destination'),
            'vehicle_type': data.get('vehicle_type'),
            'datetime': data.get('datetime')
        }
        
        result = supabase.table('transport_bookings').insert(transport_data).execute()
        print(f"Supabase result: {result}")
        
        if hasattr(result, 'data') and result.data:
            print("SUCCESS: Transport booking created")
            return jsonify({"success": True, "message": "Transport booking successful", "data": result.data})
        else:
            return jsonify({"success": False, "message": "Failed to create transport booking"}), 500
            
    except Exception as e:
        print(f"EXCEPTION in book_transport: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/book-activity', methods=['POST', 'OPTIONS'])
def book_activity():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("\n=== ACTIVITY BOOKING REQUEST ===")
        print(f"Content-Type: {request.content_type}")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        
        # Check if request has JSON data
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({"success": False, "message": "Request must be JSON"}), 400
            
        data = request.get_json()
        print(f"Activity data received: {json.dumps(data, indent=2)}")
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({"success": False, "message": "No JSON data received"}), 400
        
        # Validate required fields
        required_fields = ['name', 'phone', 'activity', 'date']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"ERROR: {error_msg}")
            return jsonify({"success": False, "message": error_msg}), 400
        
        # Map frontend fields to database fields
        activity_data = {
            'full_name': data.get('name'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'activity': data.get('activity'),
            'location': data.get('location'),
            'participants': data.get('participants', 1),
            'date': data.get('date'),
            'special_requirements': data.get('requirements')
        }
        
        print(f"Inserting into Supabase: {json.dumps(activity_data, indent=2)}")
        result = supabase.table('activity_bookings').insert(activity_data).execute()
        print(f"Supabase result: {result}")
        
        if hasattr(result, 'data') and result.data:
            print("SUCCESS: Activity booking created")
            return jsonify({"success": True, "message": "Activity booking successful", "data": result.data})
        else:
            print(f"ERROR: Supabase insert failed - {result}")
            return jsonify({"success": False, "message": "Failed to create activity booking"}), 500
            
    except Exception as e:
        print(f"EXCEPTION in book_activity: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/bookings', methods=['GET'])
def get_all_bookings():
    try:
        print("\n=== FETCHING ALL BOOKINGS ===")
        guide_result = supabase.table('guide_bookings').select("*").execute()
        transport_result = supabase.table('transport_bookings').select("*").execute()
        activity_result = supabase.table('activity_bookings').select("*").execute()
        
        all_bookings = {
            'guide': guide_result.data or [],
            'transport': transport_result.data or [],
            'activity': activity_result.data or []
        }
        
        total = len(all_bookings['guide']) + len(all_bookings['transport']) + len(all_bookings['activity'])
        print(f"Total bookings: {total}")
        
        return jsonify({"success": True, "data": all_bookings})
    except Exception as e:
        print(f"EXCEPTION in get_all_bookings: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/bookings/guide', methods=['GET'])
def get_guide_bookings():
    try:
        print("\n=== FETCHING GUIDE BOOKINGS ===")
        result = supabase.table('guide_bookings').select("*").execute()
        print(f"Guide bookings: {len(result.data) if result.data else 0}")
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        print(f"EXCEPTION in get_guide_bookings: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/bookings/transport', methods=['GET'])
def get_transport_bookings():
    try:
        print("\n=== FETCHING TRANSPORT BOOKINGS ===")
        result = supabase.table('transport_bookings').select("*").execute()
        print(f"Transport bookings: {len(result.data) if result.data else 0}")
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        print(f"EXCEPTION in get_transport_bookings: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/bookings/activity', methods=['GET'])
def get_activity_bookings():
    try:
        print("\n=== FETCHING ACTIVITY BOOKINGS ===")
        result = supabase.table('activity_bookings').select("*").execute()
        print(f"Activity bookings: {len(result.data) if result.data else 0}")
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        print(f"EXCEPTION in get_activity_bookings: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/payment', methods=['POST'])
def process_payment():
    try:
        print("\n=== PROCESSING PAYMENT ===")
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No payment data received"}), 400
        
        result = supabase.table('user_bookings').insert(data).execute()
        
        if hasattr(result, 'data') and result.data:
            print("SUCCESS: Payment data saved successfully")
            return jsonify({"success": True, "message": "Payment processed and booking saved", "data": result.data})
        else:
            return jsonify({"success": False, "message": "Failed to save booking"}), 500
            
    except Exception as e:
        print(f"EXCEPTION in process_payment: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    try:
        print("\nFLASK SERVER STARTING")
        print("Available API routes:")
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/api'):
                print(f"  {list(rule.methods - {'OPTIONS', 'HEAD'})} {rule.rule}")
        
        print(f"\nServer running at: http://localhost:5000")
        print(f"Admin panel: http://localhost:5000/admin-panel.html")
        print(f"Main website: http://localhost:5000/index.html")
        print("\nPress Ctrl+C to stop\n")
        
        app.run(host='localhost', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Failed to start Flask server: {e}")
        import traceback
        traceback.print_exc()