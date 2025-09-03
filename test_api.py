#!/usr/bin/env python3
"""
Test script to verify Flask API endpoints are working
Run this after starting your Flask server with: python app_supabase.py
"""

import requests
import json

API_BASE = "http://localhost:5000/api"

def test_server():
    """Test if server is running"""
    try:
        response = requests.get("http://localhost:5000")
        print(f"✅ Server Status: {response.status_code} - {response.text}")
        return True
    except Exception as e:
        print(f"❌ Server offline: {e}")
        return False

def test_activity_booking():
    """Test activity booking endpoint"""
    data = {
        "name": "Test User",
        "phone": "+91 9876543210",
        "email": "test@example.com",
        "activity": "trekking",
        "location": "parasnath",
        "participants": 2,
        "date": "2024-02-15",
        "requirements": "Vegetarian food"
    }
    
    try:
        response = requests.post(f"{API_BASE}/book-activity", 
                               json=data, 
                               headers={"Content-Type": "application/json"})
        print(f"✅ Activity Booking: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Activity Booking failed: {e}")
        return False

def test_guide_booking():
    """Test guide booking endpoint"""
    data = {
        "name": "Test Guide User",
        "phone": "+91 9876543210",
        "email": "guide@example.com",
        "language": "English",
        "places": ["Ranchi", "Netarhat"],
        "date": "2024-02-20"
    }
    
    try:
        response = requests.post(f"{API_BASE}/book-guide", 
                               json=data, 
                               headers={"Content-Type": "application/json"})
        print(f"✅ Guide Booking: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Guide Booking failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Flask API Endpoints ===\n")
    
    if test_server():
        print("\n=== Testing Booking Endpoints ===")
        test_activity_booking()
        print()
        test_guide_booking()
    else:
        print("Start Flask server first: python app_supabase.py")