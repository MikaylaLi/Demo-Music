from flask import Flask, request, jsonify, session, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import requests

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

app = Flask(__name__)
app.secret_key = 'majorchord_secret_key_2024'
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Quiz results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            primary_mood TEXT,
            energy_level INTEGER,
            primary_goal TEXT,
            preferred_music TEXT,
            session_duration TEXT,
            mood_category TEXT,
            stress_level INTEGER,
            sleep_quality INTEGER,
            mood_score INTEGER,
            symptoms TEXT,
            answers_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Health profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            stress_level INTEGER,
            sleep_quality INTEGER,
            mood_score INTEGER,
            energy_level INTEGER,
            symptoms TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Music library table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS music_library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            mood TEXT NOT NULL,
            tempo INTEGER,
            energy_level INTEGER,
            stress_reduction_score INTEGER,
            sleep_aid_score INTEGER,
            mood_boost_score INTEGER,
            focus_score INTEGER,
            audio_file TEXT,
            duration INTEGER
        )
    ''')
    
    # User playlists table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Playlist tracks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER,
            track_id INTEGER,
            position INTEGER,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (playlist_id) REFERENCES user_playlists (id),
            FOREIGN KEY (track_id) REFERENCES music_library (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database and populate with sample data
def populate_sample_data():
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Sample music library
    sample_tracks = [
        # Stress Relief & Relaxation
        ("Weightless", "Marconi Union", "Ambient", "calm", 60, 2, 9, 8, 7, 6, "weightless.mp3", 480),
        ("Claire de Lune", "Debussy", "Classical", "peaceful", 65, 3, 8, 9, 6, 7, "claire_de_lune.mp3", 300),
        ("River Flows in You", "Yiruma", "Piano", "serene", 70, 3, 7, 8, 7, 6, "river_flows.mp3", 240),
        ("The Sound of Silence", "Disturbed", "Rock", "contemplative", 75, 4, 6, 7, 5, 8, "sound_of_silence.mp3", 270),
        ("Moonlight Sonata", "Beethoven", "Classical", "tranquil", 60, 2, 9, 9, 6, 7, "moonlight_sonata.mp3", 900),
        ("Calm Melodies", "Piano Collection", "Piano", "soothing", 65, 2, 8, 8, 7, 6, "calm_melodies.mp3", 600),
        ("Relaxation Guide", "Meditation Sounds", "Ambient", "relaxing", 55, 2, 9, 8, 8, 5, "relaxation_guide.mp3", 1800),
        ("Stress Relief", "Healing Music", "Ambient", "calming", 60, 2, 9, 7, 7, 6, "stress_relief.mp3", 1200),
        ("Calm Heart", "Peaceful Sounds", "Ambient", "serene", 65, 2, 8, 8, 7, 6, "calm_heart.mp3", 1800),
        ("Relax Body", "Wellness Music", "Ambient", "gentle", 60, 2, 8, 8, 7, 6, "relax_body.mp3", 1200),
        
        # Energy & Motivation
        ("Eye of the Tiger", "Survivor", "Rock", "energetic", 120, 8, 4, 3, 9, 8, "eye_of_tiger.mp3", 264),
        ("Happy", "Pharrell Williams", "Pop", "joyful", 160, 9, 3, 2, 9, 7, "happy.mp3", 233),
        ("Can't Stop the Feeling!", "Justin Timberlake", "Pop", "upbeat", 140, 8, 3, 2, 9, 6, "cant_stop_feeling.mp3", 235),
        ("Shake It Off", "Taylor Swift", "Pop", "cheerful", 150, 9, 2, 1, 9, 5, "shake_it_off.mp3", 219),
        ("Here Comes the Sun", "The Beatles", "Pop", "uplifting", 130, 7, 4, 3, 9, 6, "here_comes_sun.mp3", 185),
        ("Walking on Sunshine", "Katrina & The Waves", "Pop", "bright", 140, 8, 3, 2, 9, 5, "walking_sunshine.mp3", 235),
        ("Good Vibes", "Positive Energy", "Pop", "uplifting", 130, 7, 4, 3, 8, 6, "good_vibes.mp3", 240),
        ("Sunshine", "Happy Tunes", "Pop", "bright", 140, 8, 3, 2, 9, 5, "sunshine.mp3", 210),
        ("Dance Party", "Energetic Beats", "Electronic", "exciting", 150, 9, 2, 1, 9, 4, "dance_party.mp3", 180),
        ("Uplifting Beats", "Energy Music", "Electronic", "energizing", 145, 8, 3, 2, 9, 5, "uplifting_beats.mp3", 240),
        ("Energy Boost", "Motivation Music", "Pop", "energetic", 155, 9, 2, 1, 9, 4, "energy_boost.mp3", 180),
        ("Energize Life", "Life Music", "Pop", "vibrant", 150, 8, 3, 2, 9, 5, "energize_life.mp3", 180),
        
        # Focus & Concentration
        ("Lofi Study Beats", "Various Artists", "Lo-Fi", "focused", 85, 4, 6, 5, 8, 9, "lofi_study.mp3", 1800),
        ("Classical Study Music", "Mozart", "Classical", "concentrated", 90, 5, 5, 6, 7, 9, "classical_study.mp3", 1200),
        ("White Noise", "Nature Sounds", "Ambient", "neutral", 70, 3, 7, 6, 8, 8, "white_noise.mp3", 3600),
        ("Brain.fm Focus", "Brain.fm", "Electronic", "focused", 80, 4, 6, 5, 8, 9, "brain_fm_focus.mp3", 1800),
        ("Concentration", "Focus Music", "Electronic", "concentrated", 85, 4, 6, 5, 8, 9, "concentration.mp3", 1800),
        ("Study Music", "Academic Sounds", "Lo-Fi", "focused", 80, 4, 6, 5, 8, 9, "study_music.mp3", 1200),
        ("Focus Enhancement", "Productivity Music", "Electronic", "concentrated", 85, 4, 6, 5, 8, 9, "focus_enhance.mp3", 1800),
        ("Focus Mind", "Mind Music", "Electronic", "focused", 80, 4, 6, 5, 8, 9, "focus_mind.mp3", 1800),
        ("Concentrate Focus", "Focus Sounds", "Electronic", "concentrated", 85, 4, 6, 5, 8, 9, "concentrate_focus.mp3", 1800),
        
        # Sleep & Rest
        ("Sleep Well", "Sleep Sounds", "Ambient", "soothing", 50, 2, 9, 9, 8, 4, "sleep_well.mp3", 3600),
        ("Ocean Waves", "Nature", "Ambient", "calming", 55, 2, 9, 9, 9, 3, "ocean_waves.mp3", 3600),
        ("Rain Sounds", "Nature", "Ambient", "relaxing", 60, 2, 8, 9, 9, 4, "rain_sounds.mp3", 3600),
        ("Deep Sleep", "Sleep Music", "Ambient", "tranquil", 45, 1, 9, 9, 9, 2, "deep_sleep.mp3", 3600),
        ("Insomnia Cure", "Sleep Therapy", "Ambient", "soothing", 50, 2, 9, 9, 8, 3, "insomnia_cure.mp3", 3600),
        ("Sleep Aid", "Rest Music", "Ambient", "tranquil", 45, 1, 9, 9, 9, 2, "sleep_aid.mp3", 3600),
        ("Sleep Deep", "Deep Rest", "Ambient", "soothing", 50, 2, 9, 9, 8, 3, "sleep_deep.mp3", 3600),
        ("Sleep Peace", "Peaceful Rest", "Ambient", "tranquil", 45, 1, 9, 9, 9, 2, "sleep_peace.mp3", 3600),
        
        # Anxiety Relief
        ("Anxiety Calm", "Calm Sounds", "Ambient", "soothing", 60, 2, 9, 7, 8, 6, "anxiety_calm.mp3", 1800),
        ("Calm Anxiety", "Anxiety Relief", "Ambient", "gentle", 65, 2, 8, 7, 8, 6, "calm_anxiety.mp3", 1800),
        ("Heal Anxiety", "Healing Sounds", "Ambient", "soothing", 60, 2, 9, 7, 8, 6, "heal_anxiety.mp3", 1800),
        ("Meditation Sounds", "Mindful Music", "Ambient", "peaceful", 55, 2, 9, 8, 8, 5, "meditation_sounds.mp3", 3600),
        ("Deep Breathing", "Breath Guide", "Ambient", "calming", 50, 2, 9, 8, 8, 5, "deep_breathing.mp3", 1800),
        ("Nature Sounds", "Natural Calm", "Ambient", "soothing", 60, 2, 8, 7, 8, 6, "nature_sounds.mp3", 3600),
        
        # Depression & Mood Enhancement
        ("Depression Lift", "Uplifting Music", "Pop", "bright", 140, 8, 3, 2, 9, 5, "depression_lift.mp3", 300),
        ("Lift Spirits", "Spirit Music", "Pop", "uplifting", 145, 8, 3, 2, 9, 5, "lift_spirits.mp3", 300),
        ("Uplift Depression", "Mood Music", "Pop", "bright", 140, 8, 3, 2, 9, 5, "uplift_depression.mp3", 300),
        ("Mood Boost", "Boost Music", "Pop", "uplifting", 145, 8, 3, 2, 9, 5, "mood_boost.mp3", 240),
        ("Boost Mood", "Mood Enhancement", "Pop", "bright", 140, 8, 3, 2, 9, 5, "boost_mood.mp3", 240),
        ("Uplift Soul", "Soul Music", "Pop", "uplifting", 145, 8, 3, 2, 9, 5, "uplift_soul.mp3", 300),
        
        # Chill & Relaxation
        ("Chill Vibes", "Relaxed Beats", "Lo-Fi", "mellow", 80, 4, 6, 5, 7, 6, "chill_vibes.mp3", 300),
        ("Calm Mind", "Mind Music", "Ambient", "peaceful", 65, 2, 8, 7, 8, 6, "calm_mind.mp3", 1800),
        ("Relax Muscles", "Muscle Music", "Ambient", "soothing", 60, 2, 8, 7, 8, 6, "relax_muscles.mp3", 1200),
        ("Relax Stress", "Stress Relief", "Ambient", "calming", 65, 2, 8, 7, 8, 6, "relax_stress.mp3", 1200),
    ]
    
    # Check if music library is empty
    cursor.execute("SELECT COUNT(*) FROM music_library")
    if cursor.fetchone()[0] == 0:
        for track in sample_tracks:
            cursor.execute('''
                INSERT INTO music_library 
                (title, artist, genre, mood, tempo, energy_level, stress_reduction_score, 
                 sleep_aid_score, mood_boost_score, focus_score, audio_file, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', track)
    
    conn.commit()
    conn.close()

# User authentication
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'username': username,
            'email': email
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400
    
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[3], password):
        session['user_id'] = user[0]
        return jsonify({
            'message': 'Login successful',
            'user_id': user[0],
            'username': user[1],
            'email': user[2]
        })
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# Quiz results API
@app.route('/api/quiz-results', methods=['POST'])
def save_quiz_results():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    user_id = session['user_id']
    
    # Extract quiz data
    mood_profile = data.get('moodProfile', {})
    answers = data.get('answers', {})
    
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO quiz_results 
            (user_id, primary_mood, energy_level, primary_goal, preferred_music, 
             session_duration, mood_category, stress_level, sleep_quality, mood_score, 
             symptoms, answers_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            mood_profile.get('primaryMood'),
            mood_profile.get('energyLevel'),
            mood_profile.get('primaryGoal'),
            mood_profile.get('preferredMusic'),
            mood_profile.get('sessionDuration'),
            mood_profile.get('category'),
            answers.get('stress_level', 5),
            answers.get('sleep_quality', 5),
            answers.get('mood_score', 5),
            answers.get('symptoms', ''),
            json.dumps(answers)
        ))
        
        conn.commit()
        return jsonify({'message': 'Quiz results saved successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    try:
        # Get user's latest quiz result
        cursor.execute('''
            SELECT primary_mood, energy_level, primary_goal, mood_category, 
                   stress_level, sleep_quality, mood_score, created_at
            FROM quiz_results 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (user_id,))
        user_quiz = cursor.fetchone()
        
        # Get user's playlists count
        cursor.execute('SELECT COUNT(*) FROM user_playlists WHERE user_id = ?', (user_id,))
        playlists_count = cursor.fetchone()[0]
        
        # Get user's total tracks
        cursor.execute('''
            SELECT COUNT(*) FROM playlist_tracks pt
            JOIN user_playlists up ON pt.playlist_id = up.id
            WHERE up.user_id = ?
        ''', (user_id,))
        tracks_count = cursor.fetchone()[0]
        
        # Get aggregated statistics from all users
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT user_id) as total_users,
                AVG(energy_level) as avg_energy,
                AVG(stress_level) as avg_stress,
                AVG(sleep_quality) as avg_sleep,
                AVG(mood_score) as avg_mood,
                COUNT(CASE WHEN mood_category = 'stressed' THEN 1 END) as stressed_users,
                COUNT(CASE WHEN mood_category = 'energetic' THEN 1 END) as energetic_users,
                COUNT(CASE WHEN mood_category = 'tired' THEN 1 END) as tired_users,
                COUNT(CASE WHEN mood_category = 'focused' THEN 1 END) as focused_users,
                COUNT(CASE WHEN mood_category = 'balanced' THEN 1 END) as balanced_users
            FROM quiz_results
        ''')
        aggregated_stats = cursor.fetchone()
        
        # Get recent quiz results from other users (anonymized)
        cursor.execute('''
            SELECT mood_category, primary_goal, preferred_music, created_at
            FROM quiz_results 
            WHERE user_id != ? 
            ORDER BY created_at DESC 
            LIMIT 10
        ''', (user_id,))
        recent_others = cursor.fetchall()
        
        # Get personalized recommendations based on user's mood
        personalized_tracks = []
        if user_quiz:
            mood_category = user_quiz[3]
            if mood_category == 'stressed':
                cursor.execute('''
                    SELECT title, artist, genre, stress_reduction_score
                    FROM music_library 
                    WHERE stress_reduction_score >= 7
                    ORDER BY stress_reduction_score DESC 
                    LIMIT 5
                ''')
            elif mood_category == 'energetic':
                cursor.execute('''
                    SELECT title, artist, genre, mood_boost_score
                    FROM music_library 
                    WHERE mood_boost_score >= 7
                    ORDER BY mood_boost_score DESC 
                    LIMIT 5
                ''')
            elif mood_category == 'tired':
                cursor.execute('''
                    SELECT title, artist, genre, sleep_aid_score
                    FROM music_library 
                    WHERE sleep_aid_score >= 7
                    ORDER BY sleep_aid_score DESC 
                    LIMIT 5
                ''')
            elif mood_category == 'focused':
                cursor.execute('''
                    SELECT title, artist, genre, focus_score
                    FROM music_library 
                    WHERE focus_score >= 7
                    ORDER BY focus_score DESC 
                    LIMIT 5
                ''')
            else:
                cursor.execute('''
                    SELECT title, artist, genre, 
                           (stress_reduction_score + mood_boost_score + focus_score) / 3 as avg_score
                    FROM music_library 
                    ORDER BY avg_score DESC 
                    LIMIT 5
                ''')
            personalized_tracks = cursor.fetchall()
        
        conn.close()
        
        # Format response
        response = {
            'user_stats': {
                'playlists_count': playlists_count,
                'tracks_count': tracks_count,
                'last_quiz_date': user_quiz[7] if user_quiz else None
            },
            'personalized_data': {
                'current_mood': user_quiz[0] if user_quiz else None,
                'energy_level': user_quiz[1] if user_quiz else None,
                'primary_goal': user_quiz[2] if user_quiz else None,
                'mood_category': user_quiz[3] if user_quiz else None,
                'stress_level': user_quiz[4] if user_quiz else None,
                'sleep_quality': user_quiz[5] if user_quiz else None,
                'mood_score': user_quiz[6] if user_quiz else None
            },
            'community_stats': {
                'total_users': aggregated_stats[0] if aggregated_stats else 0,
                'average_energy': round(aggregated_stats[1], 1) if aggregated_stats else 5,
                'average_stress': round(aggregated_stats[2], 1) if aggregated_stats else 5,
                'average_sleep': round(aggregated_stats[3], 1) if aggregated_stats else 5,
                'average_mood': round(aggregated_stats[4], 1) if aggregated_stats else 5,
                'mood_distribution': {
                    'stressed': aggregated_stats[5] if aggregated_stats else 0,
                    'energetic': aggregated_stats[6] if aggregated_stats else 0,
                    'tired': aggregated_stats[7] if aggregated_stats else 0,
                    'focused': aggregated_stats[8] if aggregated_stats else 0,
                    'balanced': aggregated_stats[9] if aggregated_stats else 0
                }
            },
            'recent_community_activity': [
                {
                    'mood_category': row[0],
                    'primary_goal': row[1],
                    'preferred_music': row[2],
                    'timestamp': row[3]
                } for row in recent_others
            ],
            'personalized_recommendations': [
                {
                    'title': row[0],
                    'artist': row[1],
                    'genre': row[2],
                    'score': row[3]
                } for row in personalized_tracks
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health profile management
@app.route('/api/health-profile', methods=['GET', 'POST', 'PUT'])
def health_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT stress_level, sleep_quality, mood_score, energy_level, symptoms, updated_at
            FROM health_profiles WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1
        ''', (user_id,))
        profile = cursor.fetchone()
        
        if profile:
            return jsonify({
                'stress_level': profile[0],
                'sleep_quality': profile[1],
                'mood_score': profile[2],
                'energy_level': profile[3],
                'symptoms': json.loads(profile[4]) if profile[4] else [],
                'updated_at': profile[5]
            })
        else:
            return jsonify({'message': 'No health profile found'}), 404
    
    elif request.method in ['POST', 'PUT']:
        data = request.get_json()
        
        stress_level = data.get('stress_level', 5)
        sleep_quality = data.get('sleep_quality', 5)
        mood_score = data.get('mood_score', 5)
        energy_level = data.get('energy_level', 5)
        symptoms = json.dumps(data.get('symptoms', []))
        
        if request.method == 'POST':
            cursor.execute('''
                INSERT INTO health_profiles 
                (user_id, stress_level, sleep_quality, mood_score, energy_level, symptoms)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, stress_level, sleep_quality, mood_score, energy_level, symptoms))
        else:  # PUT
            cursor.execute('''
                UPDATE health_profiles 
                SET stress_level = ?, sleep_quality = ?, mood_score = ?, 
                    energy_level = ?, symptoms = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (stress_level, sleep_quality, mood_score, energy_level, symptoms, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Health profile updated successfully'})

# Music recommendation algorithm
def get_recommendations(user_id, limit=10):
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Get user's latest health profile
    cursor.execute('''
        SELECT stress_level, sleep_quality, mood_score, energy_level, symptoms
        FROM health_profiles WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1
    ''', (user_id,))
    profile = cursor.fetchone()
    
    if not profile:
        # Return general recommendations if no profile
        cursor.execute('''
            SELECT id, title, artist, genre, mood, tempo, energy_level, audio_file
            FROM music_library ORDER BY RANDOM() LIMIT ?
        ''', (limit,))
        tracks = cursor.fetchall()
        conn.close()
        return [{'id': t[0], 'title': t[1], 'artist': t[2], 'genre': t[3], 
                'mood': t[4], 'tempo': t[5], 'energy_level': t[6], 'audio_file': t[7]} for t in tracks]
    
    stress_level, sleep_quality, mood_score, energy_level, symptoms = profile
    symptoms_list = json.loads(symptoms) if symptoms else []
    
    # Calculate recommendation scores based on health profile
    recommendations = []
    
    # Get all tracks with their scores
    cursor.execute('''
        SELECT id, title, artist, genre, mood, tempo, energy_level, audio_file,
               stress_reduction_score, sleep_aid_score, mood_boost_score, focus_score
        FROM music_library
    ''')
    tracks = cursor.fetchall()
    
    for track in tracks:
        track_id, title, artist, genre, mood, tempo, energy_level, audio_file, \
        stress_score, sleep_score, mood_score_track, focus_score = track
        
        # Calculate weighted score based on health profile
        score = 0
        
        # Stress reduction priority
        if stress_level > 6:
            score += stress_score * 3
        elif stress_level < 4:
            score += (10 - stress_score) * 2
        
        # Sleep quality priority
        if sleep_quality < 4:
            score += sleep_score * 3
        elif sleep_quality > 7:
            score += (10 - sleep_score) * 1
        
        # Mood enhancement priority
        if mood_score < 4:
            score += mood_score_track * 3
        elif mood_score > 7:
            score += (10 - mood_score_track) * 1
        
        # Energy level matching
        if energy_level < 3:
            score += energy_level * 2  # Low energy users need gentle music
        elif energy_level > 7:
            score += (10 - energy_level) * 2  # High energy users need calming music
        
        # Focus enhancement for specific symptoms
        if 'anxiety' in symptoms_list or 'stress' in symptoms_list:
            score += focus_score * 2
        
        if 'insomnia' in symptoms_list or 'sleep' in symptoms_list:
            score += sleep_score * 3
        
        if 'depression' in symptoms_list or 'sadness' in symptoms_list:
            score += mood_score_track * 3
        
        recommendations.append({
            'id': track_id,
            'title': title,
            'artist': artist,
            'genre': genre,
            'mood': mood,
            'tempo': tempo,
            'energy_level': energy_level,
            'audio_file': audio_file,
            'score': score
        })
    
    # Sort by score and return top recommendations
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    conn.close()
    
    return recommendations[:limit]

@app.route('/api/recommendations', methods=['GET'])
def get_music_recommendations():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    limit = request.args.get('limit', 10, type=int)
    
    recommendations = get_recommendations(user_id, limit)
    
    # Remove score from response
    for rec in recommendations:
        rec.pop('score', None)
    
    return jsonify({
        'recommendations': recommendations,
        'total': len(recommendations)
    })

# Playlist management
@app.route('/api/playlists', methods=['GET', 'POST'])
def playlists():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT id, name, description, created_at
            FROM user_playlists WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        playlists = cursor.fetchall()
        
        result = []
        for playlist in playlists:
            playlist_id, name, description, created_at = playlist
            
            # Get track count
            cursor.execute('SELECT COUNT(*) FROM playlist_tracks WHERE playlist_id = ?', (playlist_id,))
            track_count = cursor.fetchone()[0]
            
            result.append({
                'id': playlist_id,
                'name': name,
                'description': description,
                'created_at': created_at,
                'track_count': track_count
            })
        
        conn.close()
        return jsonify({'playlists': result})
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Playlist name is required'}), 400
        
        cursor.execute('''
            INSERT INTO user_playlists (user_id, name, description)
            VALUES (?, ?, ?)
        ''', (user_id, name, description))
        
        playlist_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Playlist created successfully',
            'playlist_id': playlist_id
        }), 201

@app.route('/api/playlists/<int:playlist_id>/tracks', methods=['GET', 'POST', 'DELETE'])
def playlist_tracks(playlist_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Verify playlist ownership
    cursor.execute('SELECT id FROM user_playlists WHERE id = ? AND user_id = ?', (playlist_id, user_id))
    if not cursor.fetchone():
        return jsonify({'error': 'Playlist not found'}), 404
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT ml.id, ml.title, ml.artist, ml.genre, ml.mood, pt.position, pt.added_at
            FROM playlist_tracks pt
            JOIN music_library ml ON pt.track_id = ml.id
            WHERE pt.playlist_id = ? ORDER BY pt.position
        ''', (playlist_id,))
        tracks = cursor.fetchall()
        
        result = []
        for track in tracks:
            result.append({
                'id': track[0],
                'title': track[1],
                'artist': track[2],
                'genre': track[3],
                'mood': track[4],
                'position': track[5],
                'added_at': track[6]
            })
        
        conn.close()
        return jsonify({'tracks': result})
    
    elif request.method == 'POST':
        data = request.get_json()
        track_id = data.get('track_id')
        
        if not track_id:
            return jsonify({'error': 'Track ID is required'}), 400
        
        # Get next position
        cursor.execute('SELECT MAX(position) FROM playlist_tracks WHERE playlist_id = ?', (playlist_id,))
        max_pos = cursor.fetchone()[0]
        next_position = (max_pos or 0) + 1
        
        cursor.execute('''
            INSERT INTO playlist_tracks (playlist_id, track_id, position)
            VALUES (?, ?, ?)
        ''', (playlist_id, track_id, next_position))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Track added to playlist'}), 201
    
    elif request.method == 'DELETE':
        data = request.get_json()
        track_id = data.get('track_id')
        
        if not track_id:
            return jsonify({'error': 'Track ID is required'}), 400
        
        cursor.execute('''
            DELETE FROM playlist_tracks 
            WHERE playlist_id = ? AND track_id = ?
        ''', (playlist_id, track_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Track removed from playlist'})

# Search functionality
@app.route('/api/search', methods=['GET'])
def search_music():
    query = request.args.get('q', '').strip()
    genre = request.args.get('genre', '')
    mood = request.args.get('mood', '')
    
    if not query and not genre and not mood:
        return jsonify({'error': 'Search query, genre, or mood is required'}), 400
    
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Build search query
    sql = '''
        SELECT id, title, artist, genre, mood, tempo, energy_level, audio_file
        FROM music_library WHERE 1=1
    '''
    params = []
    
    if query:
        sql += ' AND (title LIKE ? OR artist LIKE ? OR genre LIKE ?)'
        search_term = f'%{query}%'
        params.extend([search_term, search_term, search_term])
    
    if genre:
        sql += ' AND genre = ?'
        params.append(genre)
    
    if mood:
        sql += ' AND mood = ?'
        params.append(mood)
    
    sql += ' ORDER BY title LIMIT 20'
    
    cursor.execute(sql, params)
    tracks = cursor.fetchall()
    conn.close()
    
    result = []
    for track in tracks:
        result.append({
            'id': track[0],
            'title': track[1],
            'artist': track[2],
            'genre': track[3],
            'mood': track[4],
            'tempo': track[5],
            'energy_level': track[6],
            'audio_file': track[7]
        })
    
    return jsonify({'tracks': result, 'total': len(result)})

# Health insights
@app.route('/api/health-insights', methods=['GET'])
def health_insights():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Get recent health data
    cursor.execute('''
        SELECT stress_level, sleep_quality, mood_score, energy_level, updated_at
        FROM health_profiles WHERE user_id = ? ORDER BY updated_at DESC LIMIT 7
    ''', (user_id,))
    recent_data = cursor.fetchall()
    
    if not recent_data:
        return jsonify({'message': 'No health data available'}), 404
    
    # Calculate insights
    avg_stress = sum(row[0] for row in recent_data) / len(recent_data)
    avg_sleep = sum(row[1] for row in recent_data) / len(recent_data)
    avg_mood = sum(row[2] for row in recent_data) / len(recent_data)
    avg_energy = sum(row[3] for row in recent_data) / len(recent_data)
    
    insights = {
        'average_stress_level': round(avg_stress, 1),
        'average_sleep_quality': round(avg_sleep, 1),
        'average_mood_score': round(avg_mood, 1),
        'average_energy_level': round(avg_energy, 1),
        'recommendations': []
    }
    
    # Generate personalized recommendations
    if avg_stress > 6:
        insights['recommendations'].append({
            'type': 'stress_relief',
            'message': 'Your stress levels are elevated. Try calming music with nature sounds.',
            'priority': 'high'
        })
    
    if avg_sleep < 5:
        insights['recommendations'].append({
            'type': 'sleep_improvement',
            'message': 'Your sleep quality could improve. Consider gentle ambient music before bed.',
            'priority': 'high'
        })
    
    if avg_mood < 5:
        insights['recommendations'].append({
            'type': 'mood_boost',
            'message': 'Your mood could use a lift. Try upbeat, positive music.',
            'priority': 'medium'
        })
    
    if avg_energy < 4:
        insights['recommendations'].append({
            'type': 'energy_boost',
            'message': 'Your energy levels are low. Consider motivational music.',
            'priority': 'medium'
        })
    
    conn.close()
    return jsonify(insights)

# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/test')
def test_buttons():
    return send_from_directory('.', 'test_buttons.html')

@app.route('/api/audio/<filename>')
def serve_audio(filename):
    """Serve audio files from the audio directory"""
    try:
        return send_from_directory('audio', filename)
    except FileNotFoundError:
        return jsonify({'error': 'Audio file not found'}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Placeholder: If no API key, return a canned response
    if not OPENAI_API_KEY:
        return jsonify({'reply': "[AI] Sorry, the AI service is not configured yet. Please set your OpenAI API key.", 'sentiment': 'Unknown'})

    try:
        # Call OpenAI API for chat reply
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful health and music assistant for the MajorChord app. Give music and wellness advice, and ask if the user wants to update their dashboard based on new symptoms.'},
                    {'role': 'user', 'content': user_message}
                ],
                'max_tokens': 200,
                'temperature': 0.7
            }
        )
        result = response.json()
        ai_reply = result['choices'][0]['message']['content'] if 'choices' in result and result['choices'] else '[AI] Sorry, no response.'

        # Call OpenAI API for sentiment analysis
        sentiment_prompt = f"Classify the sentiment or mood of this message as Positive, Negative, or Neutral, and if possible, give a one-word mood label (e.g., Happy, Sad, Anxious, Calm): {user_message}"
        sentiment_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a mood and sentiment classifier. Reply with only the sentiment (Positive, Negative, Neutral) and a one-word mood label.'},
                    {'role': 'user', 'content': sentiment_prompt}
                ],
                'max_tokens': 20,
                'temperature': 0.0
            }
        )
        sentiment_result = sentiment_response.json()
        sentiment = sentiment_result['choices'][0]['message']['content'] if 'choices' in sentiment_result and sentiment_result['choices'] else 'Unknown'

        return jsonify({'reply': ai_reply, 'sentiment': sentiment})
    except Exception as e:
        return jsonify({'error': str(e), 'sentiment': 'Unknown'}), 500

if __name__ == '__main__':
    init_db()
    populate_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5000) 