#!/usr/bin/env python3
"""
Script to reset today's progress via API
"""
import requests
import sys

API_BASE_URL = "http://localhost:8001"

def reset_today_via_api():
    """Reset today's progress via API call"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/admin/reset-today")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"📊 Deleted {data['deleted_activities']} activities from today")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on http://localhost:8001")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔄 Resetting today's progress via API...")
    reset_today_via_api()
    print("✅ Done!")
