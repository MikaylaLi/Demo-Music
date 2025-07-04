#!/usr/bin/env python3
"""
Test script for MajorChord Flask backend
Tests user registration, health profiles, and music recommendations
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def test_user_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    response = requests.post(f'{BASE_URL}/register', json=user_data)
    
    if response.status_code == 201:
        print("✅ User registration successful")
        return response.json()
    else:
        print(f"❌ User registration failed: {response.text}")
        return None

def test_user_login():
    """Test user login"""
    print("Testing user login...")
    
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    
    if response.status_code == 200:
        print("✅ User login successful")
        return response.json()
    else:
        print(f"❌ User login failed: {response.text}")
        return None

def test_health_profile():
    """Test health profile creation and update"""
    print("Testing health profile...")
    
    health_data = {
        'stress_level': 7,
        'sleep_quality': 4,
        'mood_score': 6,
        'energy_level': 5,
        'symptoms': ['anxiety', 'stress', 'insomnia']
    }
    
    # Create health profile
    response = requests.post(f'{BASE_URL}/health-profile', json=health_data)
    
    if response.status_code == 200:
        print("✅ Health profile created successfully")
    else:
        print(f"❌ Health profile creation failed: {response.text}")
        return False
    
    # Get health profile
    response = requests.get(f'{BASE_URL}/health-profile')
    
    if response.status_code == 200:
        profile = response.json()
        print(f"✅ Health profile retrieved: {profile}")
        return True
    else:
        print(f"❌ Health profile retrieval failed: {response.text}")
        return False

def test_music_recommendations():
    """Test music recommendations"""
    print("Testing music recommendations...")
    
    response = requests.get(f'{BASE_URL}/recommendations?limit=5')
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"✅ Got {len(recommendations['recommendations'])} recommendations")
        
        for i, rec in enumerate(recommendations['recommendations'][:3], 1):
            print(f"  {i}. {rec['title']} by {rec['artist']} ({rec['genre']})")
        
        return True
    else:
        print(f"❌ Music recommendations failed: {response.text}")
        return False

def test_health_insights():
    """Test health insights"""
    print("Testing health insights...")
    
    response = requests.get(f'{BASE_URL}/health-insights')
    
    if response.status_code == 200:
        insights = response.json()
        print("✅ Health insights retrieved:")
        print(f"  - Average stress level: {insights.get('average_stress_level', 'N/A')}")
        print(f"  - Average sleep quality: {insights.get('average_sleep_quality', 'N/A')}")
        print(f"  - Average mood score: {insights.get('average_mood_score', 'N/A')}")
        print(f"  - Average energy level: {insights.get('average_energy_level', 'N/A')}")
        
        if insights.get('recommendations'):
            print("  - Recommendations:")
            for rec in insights['recommendations']:
                print(f"    * {rec['message']}")
        
        return True
    else:
        print(f"❌ Health insights failed: {response.text}")
        return False

def test_playlist_creation():
    """Test playlist creation"""
    print("Testing playlist creation...")
    
    playlist_data = {
        'name': 'My Wellness Playlist',
        'description': 'Personalized music for my health journey'
    }
    
    response = requests.post(f'{BASE_URL}/playlists', json=playlist_data)
    
    if response.status_code == 201:
        playlist = response.json()
        print(f"✅ Playlist created: {playlist['playlist_id']}")
        return playlist['playlist_id']
    else:
        print(f"❌ Playlist creation failed: {response.text}")
        return None

def test_music_search():
    """Test music search functionality"""
    print("Testing music search...")
    
    # Search by query
    response = requests.get(f'{BASE_URL}/search?q=calm')
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Search found {results['total']} tracks for 'calm'")
        return True
    else:
        print(f"❌ Music search failed: {response.text}")
        return False

def test_backend_health():
    """Test basic backend health"""
    print("Testing backend health...")
    
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("✅ Backend is running and responding")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start the Flask server first.")
        return False

def main():
    """Run all tests"""
    print("🎵 MajorChord Backend Test Suite")
    print("=" * 40)
    
    # Test backend health first
    if not test_backend_health():
        print("\n❌ Backend is not available. Please start the Flask server:")
        print("   python app.py")
        return
    
    print("\n" + "=" * 40)
    
    # Run tests
    tests = [
        ("Backend Health", test_backend_health),
        ("User Registration", test_user_registration),
        ("User Login", test_user_login),
        ("Health Profile", test_health_profile),
        ("Music Recommendations", test_music_recommendations),
        ("Health Insights", test_health_insights),
        ("Playlist Creation", test_playlist_creation),
        ("Music Search", test_music_search)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the backend implementation.")

if __name__ == '__main__':
    main() 