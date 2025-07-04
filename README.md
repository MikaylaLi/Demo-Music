# MajorChord - AI-Powered Music for Wellness

MajorChord is an AI-powered music companion that provides personalized playlists based on your health and wellness needs. Whether you're stressed, need better sleep, want to boost your mood, or improve focus, MajorChord adapts to your unique health profile.

## Features

### 🎵 Smart Music Recommendations
- **Health-Based Algorithm**: Music recommendations based on stress levels, sleep quality, mood, and energy
- **Symptom Tracking**: Personalized recommendations for anxiety, insomnia, depression, and more
- **Real-Time Adaptation**: Recommendations update as your health profile changes

### 🧘 Wellness Integration
- **Health Profile Management**: Track stress, sleep, mood, and energy levels
- **Symptom Tracking**: Log specific symptoms for targeted music therapy
- **Health Insights**: Get personalized wellness recommendations and trends

### 🎼 Music Library
- **Diverse Genres**: Classical, Ambient, Lo-Fi, Pop, Rock, and more
- **Mood-Based Categorization**: Calm, Energetic, Focused, Uplifting, Soothing
- **Health Scores**: Each track rated for stress reduction, sleep aid, mood boost, and focus

### 📱 User Experience
- **Personal Playlists**: Create and manage custom playlists
- **Search & Discover**: Find music by title, artist, genre, or mood
- **Health Tracking**: Monitor your wellness journey over time

## Backend API

The Flask backend provides comprehensive APIs for:

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout

### Health Management
- `GET /api/health-profile` - Get current health profile
- `POST /api/health-profile` - Create new health profile
- `PUT /api/health-profile` - Update health profile
- `GET /api/health-insights` - Get personalized health insights

### Music Recommendations
- `GET /api/recommendations` - Get personalized music recommendations
- `GET /api/search` - Search music library
- `GET /api/playlists` - Get user playlists
- `POST /api/playlists` - Create new playlist
- `GET /api/playlists/<id>/tracks` - Get playlist tracks
- `POST /api/playlists/<id>/tracks` - Add track to playlist
- `DELETE /api/playlists/<id>/tracks` - Remove track from playlist

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Backend Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask backend:
   ```bash
   python app.py
   ```
4. The API will be available at `http://localhost:5000`

### Database
The application uses SQLite with automatic initialization:
- Users table for authentication
- Health profiles for wellness tracking
- Music library with health scores
- User playlists and tracks

## Health-Based Recommendation Algorithm

The recommendation system considers:

### Stress Levels (1-10)
- **High Stress (7-10)**: Prioritizes stress reduction scores
- **Low Stress (1-3)**: Includes energizing music
- **Moderate (4-6)**: Balanced recommendations

### Sleep Quality (1-10)
- **Poor Sleep (1-4)**: High sleep aid scores
- **Good Sleep (7-10)**: Avoids sleep-inducing music

### Mood Scores (1-10)
- **Low Mood (1-4)**: High mood boost scores
- **High Mood (7-10)**: Maintains positive energy

### Energy Levels (1-10)
- **Low Energy (1-3)**: Gentle, calming music
- **High Energy (7-10)**: Soothing, relaxing tracks

### Symptom-Based Adjustments
- **Anxiety/Stress**: Increased focus scores
- **Insomnia**: Maximum sleep aid scores
- **Depression**: High mood boost scores

## API Examples

### Register User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "password123"}'
```

### Update Health Profile
```bash
curl -X POST http://localhost:5000/api/health-profile \
  -H "Content-Type: application/json" \
  -d '{
    "stress_level": 7,
    "sleep_quality": 4,
    "mood_score": 6,
    "energy_level": 5,
    "symptoms": ["anxiety", "stress"]
  }'
```

### Get Recommendations
```bash
curl -X GET "http://localhost:5000/api/recommendations?limit=10"
```

## Frontend Integration

The frontend can integrate with the backend APIs to:
- Display personalized recommendations
- Track health metrics
- Manage playlists
- Search and discover music

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**MajorChord** - Where Music Meets Wellness 🎵✨
