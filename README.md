# MajorChord - AI Personalized Music for Your Everyday Life

## Overview

MajorChord is a comprehensive music therapy application that combines AI-powered mood assessment with personalized music recommendations. The platform helps users improve their mental well-being through evidence-based music therapy techniques.

## Features

### 🔐 Authentication System
- **User Registration**: Complete signup with email validation
- **User Login**: Secure authentication with localStorage
- **Session Management**: Persistent login sessions
- **Test Users**: Pre-configured demo accounts for testing

### 🧠 Mood Assessment Quiz
- **5-Question Assessment**: Comprehensive mood evaluation
- **Multiple Question Types**: Options selection and mood sliders
- **Real-time Progress**: Visual progress indicator
- **Personalized Analysis**: AI-powered mood profile generation
- **Smart Recommendations**: Context-aware music suggestions

### 🎵 Personalized Dashboard
- **Mood-Based Playlists**: AI-generated music collections
- **Interactive Stats**: Track your music therapy journey
- **Quick Actions**: Easy access to common features
- **Session Tracking**: Monitor your wellness progress

### 🤖 AI Music Assistant
- **Natural Language Chat**: Conversational music recommendations
- **Context-Aware Responses**: Understands your mood and goals
- **Personalized Suggestions**: Based on your assessment results
- **Real-time Interaction**: Instant responses to your queries

### 📊 Health Analytics
- **Session Tracking**: Monitor your music therapy sessions
- **Mood Trends**: Track your emotional well-being over time
- **Progress Metrics**: Visualize your wellness journey
- **Personalized Insights**: AI-generated health recommendations

## Test Users

### Demo User
- **Email**: `demo@example.com`
- **Password**: `demo123`

### Test User
- **Email**: `test@example.com`
- **Password**: `test123`

## User Flow

1. **Sign In/Up**: Authenticate with existing or new account
2. **Mood Assessment**: Complete the 5-question mood quiz
3. **Personalized Dashboard**: Access your customized music experience
4. **AI Chat**: Get real-time music recommendations
5. **Track Progress**: Monitor your wellness journey

## Technical Features

### Frontend Technologies
- **HTML5**: Semantic markup and modern structure
- **CSS3**: Glassmorphism design with smooth animations
- **JavaScript ES6+**: Modern JavaScript with classes and modules
- **LocalStorage**: Client-side data persistence
- **Responsive Design**: Mobile-first approach

### AI Integration
- **Mood Analysis**: Intelligent mood profile generation
- **Music Recommendations**: Context-aware playlist suggestions
- **Chat Assistant**: Natural language processing for music queries
- **Personalization**: User-specific content and recommendations

### Design System
- **Glassmorphism**: Modern glass-like UI elements
- **Gradient Backgrounds**: Beautiful color transitions
- **Smooth Animations**: Enhanced user experience
- **Accessibility**: Inclusive design principles

## New AI/ML Features & Improvements (2024)

### ✅ OpenAI-Powered Chatbot
- **chatbot.html**: AI chat assistant for symptom help, music/song recommendations, and dashboard updates.
- **Accessible from the Symptom Helper card** on the main page.
- **Integrates with OpenAI API** (requires API key, see below).

### ✅ Functionality Test Page
- **test_buttons.html**: Developer tool to verify all main navigation and music functions are present and working in the frontend.
- **Ensures robust integration and error-free UI.**

### ✅ Improved Error Handling & Robustness
- All main UI functions are now guaranteed to be present and callable.
- Placeholder alerts for unimplemented features.
- Better error messages and user feedback throughout the app.

### ✅ AI/ML Feature Checklist
- [x] Project analysis and integration points
- [x] OpenAI chatbot (chatbot.html)
- [x] Functionality test page (test_buttons.html)
- [x] Robust frontend function patching
- [ ] Text sentiment analysis (upcoming)
- [ ] Music/mood recommendation system (upcoming)
- [ ] Predictive mood model (upcoming)
- [ ] Audio classification (upcoming)

## OpenAI API Setup (for Chatbot)

1. **Get an OpenAI API Key:**
   - Sign up at https://platform.openai.com/ and create an API key.
2. **Set the API Key as an Environment Variable:**
   - On Windows (Command Prompt):
     ```
     set OPENAI_API_KEY=your_openai_api_key_here
     ```
   - On Mac/Linux:
     ```
     export OPENAI_API_KEY=your_openai_api_key_here
     ```
3. **Restart your Flask server after setting the key.**

## File Structure (updated)

```
MajorChord/
├── index.html              # Main landing page
├── signin.html            # User authentication
├── signup.html            # User registration
├── mood-assessment.html   # Mood assessment quiz
├── dashboard.html         # Personalized dashboard
├── chatbot.html           # AI-powered chatbot (NEW)
├── test_buttons.html      # Functionality test page (NEW)
├── app.py                # Flask backend server
├── config.py             # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Getting Started

1. **Start the Server**:
   ```bash
   python app.py
   ```

2. **Access the Application**:
   - Open your browser to `http://127.0.0.1:5000`

3. **Test the Features**:
   - Use the provided test user credentials
   - Complete the mood assessment
   - Explore the personalized dashboard
   - Try the AI chat assistant

## Key Features in Detail

### Mood Assessment System
- **Question Types**: Multiple choice and slider inputs
- **Progress Tracking**: Real-time completion indicator
- **Smart Analysis**: AI-powered mood categorization
- **Personalized Results**: Custom recommendations based on responses

### AI Chat Assistant
- **Natural Conversations**: Human-like interaction
- **Context Awareness**: Remembers your mood and preferences
- **Music Knowledge**: Extensive music recommendation database
- **Real-time Responses**: Instant feedback and suggestions

### Personalized Dashboard
- **Mood Indicators**: Visual representation of current state
- **Custom Playlists**: AI-generated music collections
- **Progress Tracking**: Session and wellness metrics
- **Quick Actions**: Easy access to common features

## Future Enhancements

- **Music Streaming Integration**: Connect with Spotify/Apple Music
- **Advanced Analytics**: Detailed wellness insights
- **Social Features**: Share playlists with friends
- **Mobile App**: Native iOS/Android applications
- **Voice Integration**: Voice-controlled music selection

## Contributing

This is a demonstration project showcasing modern web development techniques and AI integration for music therapy applications.

## License

This project is for educational and demonstration purposes.
