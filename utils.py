import json
import sqlite3
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

def validate_health_data(data: Dict) -> Tuple[bool, str]:
    """Validate health profile data"""
    required_fields = ['stress_level', 'sleep_quality', 'mood_score', 'energy_level']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        
        value = data[field]
        if not isinstance(value, (int, float)) or value < 1 or value > 10:
            return False, f"{field} must be a number between 1 and 10"
    
    # Validate symptoms if provided
    if 'symptoms' in data:
        if not isinstance(data['symptoms'], list):
            return False, "Symptoms must be a list"
        
        for symptom in data['symptoms']:
            if not isinstance(symptom, str):
                return False, "All symptoms must be strings"
    
    return True, ""

def calculate_music_score(track_data: Dict, health_profile: Dict) -> float:
    """Calculate personalized score for a music track based on health profile"""
    score = 0.0
    
    stress_level = health_profile.get('stress_level', 5)
    sleep_quality = health_profile.get('sleep_quality', 5)
    mood_score = health_profile.get('mood_score', 5)
    energy_level = health_profile.get('energy_level', 5)
    symptoms = health_profile.get('symptoms', [])
    
    # Stress reduction scoring
    if stress_level > 6:
        score += track_data.get('stress_reduction_score', 5) * 3
    elif stress_level < 4:
        score += (10 - track_data.get('stress_reduction_score', 5)) * 2
    
    # Sleep quality scoring
    if sleep_quality < 4:
        score += track_data.get('sleep_aid_score', 5) * 3
    elif sleep_quality > 7:
        score += (10 - track_data.get('sleep_aid_score', 5)) * 1
    
    # Mood enhancement scoring
    if mood_score < 4:
        score += track_data.get('mood_boost_score', 5) * 3
    elif mood_score > 7:
        score += (10 - track_data.get('mood_boost_score', 5)) * 1
    
    # Energy level matching
    track_energy = track_data.get('energy_level', 5)
    if energy_level < 3:
        score += (10 - track_energy) * 2  # Low energy users need gentle music
    elif energy_level > 7:
        score += track_energy * 2  # High energy users need calming music
    
    # Symptom-based adjustments
    symptoms_lower = [s.lower() for s in symptoms]
    
    if any(s in symptoms_lower for s in ['anxiety', 'stress', 'worry']):
        score += track_data.get('focus_score', 5) * 2
    
    if any(s in symptoms_lower for s in ['insomnia', 'sleep', 'tired']):
        score += track_data.get('sleep_aid_score', 5) * 3
    
    if any(s in symptoms_lower for s in ['depression', 'sadness', 'down']):
        score += track_data.get('mood_boost_score', 5) * 3
    
    if any(s in symptoms_lower for s in ['focus', 'concentration', 'attention']):
        score += track_data.get('focus_score', 5) * 2
    
    return score

def analyze_health_trends(user_id: int, days: int = 7) -> Dict:
    """Analyze health trends over time"""
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Get health data for the specified period
    start_date = datetime.now() - timedelta(days=days)
    cursor.execute('''
        SELECT stress_level, sleep_quality, mood_score, energy_level, updated_at
        FROM health_profiles 
        WHERE user_id = ? AND updated_at >= ?
        ORDER BY updated_at DESC
    ''', (user_id, start_date.strftime('%Y-%m-%d')))
    
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        return {'message': 'No health data available for analysis'}
    
    # Calculate trends
    metrics = ['stress_level', 'sleep_quality', 'mood_score', 'energy_level']
    trends = {}
    
    for i, metric in enumerate(metrics):
        values = [row[i] for row in data]
        if len(values) >= 2:
            trend = 'improving' if values[0] > values[-1] else 'declining' if values[0] < values[-1] else 'stable'
            avg_value = sum(values) / len(values)
            trends[metric] = {
                'current': values[0],
                'average': round(avg_value, 1),
                'trend': trend,
                'data_points': len(values)
            }
    
    return trends

def generate_health_insights(health_profile: Dict) -> List[Dict]:
    """Generate personalized health insights and recommendations"""
    insights = []
    
    stress_level = health_profile.get('stress_level', 5)
    sleep_quality = health_profile.get('sleep_quality', 5)
    mood_score = health_profile.get('mood_score', 5)
    energy_level = health_profile.get('energy_level', 5)
    symptoms = health_profile.get('symptoms', [])
    
    # Stress insights
    if stress_level > 7:
        insights.append({
            'type': 'stress_warning',
            'severity': 'high',
            'message': 'Your stress levels are very high. Consider deep breathing exercises with calming music.',
            'recommendation': 'Try ambient music with nature sounds for 15-20 minutes daily.'
        })
    elif stress_level > 5:
        insights.append({
            'type': 'stress_alert',
            'severity': 'medium',
            'message': 'Your stress levels are elevated. Gentle music can help you relax.',
            'recommendation': 'Listen to classical or piano music during breaks.'
        })
    
    # Sleep insights
    if sleep_quality < 4:
        insights.append({
            'type': 'sleep_warning',
            'severity': 'high',
            'message': 'Your sleep quality needs improvement. Poor sleep affects overall health.',
            'recommendation': 'Create a bedtime routine with sleep-inducing ambient music.'
        })
    elif sleep_quality < 6:
        insights.append({
            'type': 'sleep_alert',
            'severity': 'medium',
            'message': 'Your sleep quality could be better. Consider relaxing music before bed.',
            'recommendation': 'Try white noise or gentle nature sounds 30 minutes before sleep.'
        })
    
    # Mood insights
    if mood_score < 4:
        insights.append({
            'type': 'mood_warning',
            'severity': 'high',
            'message': 'Your mood is low. Music can be a powerful mood booster.',
            'recommendation': 'Listen to upbeat, positive music to lift your spirits.'
        })
    elif mood_score < 6:
        insights.append({
            'type': 'mood_alert',
            'severity': 'medium',
            'message': 'Your mood could use a boost. Positive music can help.',
            'recommendation': 'Try cheerful pop or uplifting instrumental music.'
        })
    
    # Energy insights
    if energy_level < 3:
        insights.append({
            'type': 'energy_warning',
            'severity': 'medium',
            'message': 'Your energy levels are very low. Gentle music can help you recharge.',
            'recommendation': 'Start with calming music and gradually increase energy levels.'
        })
    elif energy_level > 8:
        insights.append({
            'type': 'energy_alert',
            'severity': 'low',
            'message': 'Your energy levels are very high. Consider calming music to balance.',
            'recommendation': 'Try relaxing ambient or classical music to find balance.'
        })
    
    # Symptom-specific insights
    symptoms_lower = [s.lower() for s in symptoms]
    
    if 'anxiety' in symptoms_lower:
        insights.append({
            'type': 'anxiety_support',
            'severity': 'high',
            'message': 'Anxiety can be managed with the right music therapy.',
            'recommendation': 'Focus on slow, steady rhythms and calming nature sounds.'
        })
    
    if 'insomnia' in symptoms_lower:
        insights.append({
            'type': 'sleep_support',
            'severity': 'high',
            'message': 'Insomnia can be improved with consistent sleep music therapy.',
            'recommendation': 'Use the same sleep-inducing music every night to create routine.'
        })
    
    if 'depression' in symptoms_lower:
        insights.append({
            'type': 'mood_support',
            'severity': 'high',
            'message': 'Music therapy can be an effective complement to depression treatment.',
            'recommendation': 'Start with gentle, positive music and gradually increase energy.'
        })
    
    return insights

def format_music_recommendation(track_data: Dict, score: float = None) -> Dict:
    """Format music track data for API response"""
    return {
        'id': track_data['id'],
        'title': track_data['title'],
        'artist': track_data['artist'],
        'genre': track_data['genre'],
        'mood': track_data['mood'],
        'tempo': track_data['tempo'],
        'energy_level': track_data['energy_level'],
        'score': round(score, 2) if score else None
    }

def validate_playlist_data(data: Dict) -> Tuple[bool, str]:
    """Validate playlist creation/update data"""
    if 'name' not in data or not data['name'].strip():
        return False, "Playlist name is required"
    
    if len(data['name'].strip()) > 100:
        return False, "Playlist name must be less than 100 characters"
    
    return True, ""

def get_user_stats(user_id: int) -> Dict:
    """Get user statistics and activity summary"""
    conn = sqlite3.connect('majorchord.db')
    cursor = conn.cursor()
    
    # Get total playlists
    cursor.execute('SELECT COUNT(*) FROM user_playlists WHERE user_id = ?', (user_id,))
    total_playlists = cursor.fetchone()[0]
    
    # Get total tracks in playlists
    cursor.execute('''
        SELECT COUNT(*) FROM playlist_tracks pt
        JOIN user_playlists up ON pt.playlist_id = up.id
        WHERE up.user_id = ?
    ''', (user_id,))
    total_tracks = cursor.fetchone()[0]
    
    # Get health profile count
    cursor.execute('SELECT COUNT(*) FROM health_profiles WHERE user_id = ?', (user_id,))
    health_entries = cursor.fetchone()[0]
    
    # Get latest health profile
    cursor.execute('''
        SELECT stress_level, sleep_quality, mood_score, energy_level
        FROM health_profiles WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1
    ''', (user_id,))
    latest_profile = cursor.fetchone()
    
    conn.close()
    
    stats = {
        'total_playlists': total_playlists,
        'total_tracks': total_tracks,
        'health_entries': health_entries,
        'latest_health_profile': None
    }
    
    if latest_profile:
        stats['latest_health_profile'] = {
            'stress_level': latest_profile[0],
            'sleep_quality': latest_profile[1],
            'mood_score': latest_profile[2],
            'energy_level': latest_profile[3]
        }
    
    return stats 