/**
 * MajorChord Frontend Integration
 * JavaScript functions to interact with the Flask backend API
 */

class MajorChordAPI {
    constructor(baseURL = 'http://localhost:5000/api') {
        this.baseURL = baseURL;
        this.user = null;
    }

    // Authentication Methods
    async register(username, email, password) {
        try {
            const response = await fetch(`${this.baseURL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.user = data;
                this.saveUserToStorage(data);
                return { success: true, data };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.user = data;
                this.saveUserToStorage(data);
                return { success: true, data };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async logout() {
        try {
            const response = await fetch(`${this.baseURL}/logout`, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                this.user = null;
                this.clearUserFromStorage();
                return { success: true };
            } else {
                return { success: false, error: 'Logout failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Health Profile Methods
    async updateHealthProfile(healthData) {
        try {
            const response = await fetch(`${this.baseURL}/health-profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(healthData),
                credentials: 'include'
            });

            if (response.ok) {
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async getHealthProfile() {
        try {
            const response = await fetch(`${this.baseURL}/health-profile`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                return { success: false, error: 'No health profile found' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async getHealthInsights() {
        try {
            const response = await fetch(`${this.baseURL}/health-insights`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                return { success: false, error: 'Failed to get health insights' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Music Recommendation Methods
    async getRecommendations(limit = 10) {
        try {
            const response = await fetch(`${this.baseURL}/recommendations?limit=${limit}`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                return { success: false, error: 'Failed to get recommendations' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async searchMusic(query, genre = '', mood = '') {
        try {
            const params = new URLSearchParams();
            if (query) params.append('q', query);
            if (genre) params.append('genre', genre);
            if (mood) params.append('mood', mood);

            const response = await fetch(`${this.baseURL}/search?${params}`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                return { success: false, error: 'Search failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Playlist Methods
    async createPlaylist(name, description = '') {
        try {
            const response = await fetch(`${this.baseURL}/playlists`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, description }),
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async getPlaylists() {
        try {
            const response = await fetch(`${this.baseURL}/playlists`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            } else {
                return { success: false, error: 'Failed to get playlists' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async addTrackToPlaylist(playlistId, trackId) {
        try {
            const response = await fetch(`${this.baseURL}/playlists/${playlistId}/tracks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ track_id: trackId }),
                credentials: 'include'
            });

            if (response.ok) {
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Storage Methods
    saveUserToStorage(userData) {
        localStorage.setItem('majorchord_user', JSON.stringify(userData));
    }

    clearUserFromStorage() {
        localStorage.removeItem('majorchord_user');
    }

    loadUserFromStorage() {
        const userData = localStorage.getItem('majorchord_user');
        if (userData) {
            this.user = JSON.parse(userData);
            return this.user;
        }
        return null;
    }

    isLoggedIn() {
        return this.user !== null;
    }
}

// Example usage functions
async function exampleUsage() {
    const api = new MajorChordAPI();

    // Check if user is already logged in
    const savedUser = api.loadUserFromStorage();
    if (savedUser) {
        console.log('User already logged in:', savedUser.username);
    }

    // Example: Register a new user
    const registerResult = await api.register('john_doe', 'john@example.com', 'password123');
    if (registerResult.success) {
        console.log('Registration successful:', registerResult.data);
    } else {
        console.log('Registration failed:', registerResult.error);
    }

    // Example: Update health profile
    const healthData = {
        stress_level: 7,
        sleep_quality: 4,
        mood_score: 6,
        energy_level: 5,
        symptoms: ['anxiety', 'stress', 'insomnia']
    };

    const healthResult = await api.updateHealthProfile(healthData);
    if (healthResult.success) {
        console.log('Health profile updated successfully');
    } else {
        console.log('Health profile update failed:', healthResult.error);
    }

    // Example: Get music recommendations
    const recommendationsResult = await api.getRecommendations(5);
    if (recommendationsResult.success) {
        console.log('Music recommendations:', recommendationsResult.data.recommendations);
    } else {
        console.log('Failed to get recommendations:', recommendationsResult.error);
    }

    // Example: Get health insights
    const insightsResult = await api.getHealthInsights();
    if (insightsResult.success) {
        console.log('Health insights:', insightsResult.data);
    } else {
        console.log('Failed to get insights:', insightsResult.error);
    }

    // Example: Search for music
    const searchResult = await api.searchMusic('calm');
    if (searchResult.success) {
        console.log('Search results:', searchResult.data.tracks);
    } else {
        console.log('Search failed:', searchResult.error);
    }

    // Example: Create a playlist
    const playlistResult = await api.createPlaylist('My Wellness Playlist', 'Personalized music for my health journey');
    if (playlistResult.success) {
        console.log('Playlist created:', playlistResult.data);
    } else {
        console.log('Playlist creation failed:', playlistResult.error);
    }
}

// UI Helper Functions
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    if (!container) return;

    container.innerHTML = '';
    
    recommendations.forEach((track, index) => {
        const trackElement = document.createElement('div');
        trackElement.className = 'recommendation-track';
        trackElement.innerHTML = `
            <h3>${track.title}</h3>
            <p>by ${track.artist}</p>
            <p>Genre: ${track.genre} | Mood: ${track.mood}</p>
            <button onclick="addToPlaylist(${track.id})">Add to Playlist</button>
        `;
        container.appendChild(trackElement);
    });
}

function displayHealthInsights(insights) {
    const container = document.getElementById('health-insights-container');
    if (!container) return;

    container.innerHTML = `
        <h2>Your Health Insights</h2>
        <div class="health-metrics">
            <div class="metric">
                <span class="label">Stress Level:</span>
                <span class="value">${insights.average_stress_level}/10</span>
            </div>
            <div class="metric">
                <span class="label">Sleep Quality:</span>
                <span class="value">${insights.average_sleep_quality}/10</span>
            </div>
            <div class="metric">
                <span class="label">Mood Score:</span>
                <span class="value">${insights.average_mood_score}/10</span>
            </div>
            <div class="metric">
                <span class="label">Energy Level:</span>
                <span class="value">${insights.average_energy_level}/10</span>
            </div>
        </div>
        ${insights.recommendations ? `
            <div class="recommendations">
                <h3>Personalized Recommendations</h3>
                ${insights.recommendations.map(rec => `
                    <div class="recommendation">
                        <p>${rec.message}</p>
                    </div>
                `).join('')}
            </div>
        ` : ''}
    `;
}

// === Global functions for test_buttons.html compatibility ===
window.goToHealthPage = function() {
    console.log('goToHealthPage called');
    // Example: redirect or show health page
    alert('Navigating to Health Page (stub)');
};
window.goToSessionsPage = function() {
    console.log('goToSessionsPage called');
    alert('Navigating to Sessions Page (stub)');
};
window.goToPlaylistPage = function() {
    console.log('goToPlaylistPage called');
    alert('Navigating to Playlist Page (stub)');
};
window.goBackToPage2 = function() {
    console.log('goBackToPage2 called');
    alert('Going back to Page 2 (stub)');
};
window.searchMusic = function(query) {
    console.log('searchMusic called with query:', query);
    alert('Searching music for: ' + query + ' (stub)');
    // Optionally call MajorChordAPI.searchMusic
};
window.playSearchTrack = function(title, artist) {
    console.log('playSearchTrack called:', title, artist);
    alert('Playing track: ' + title + ' by ' + artist + ' (stub)');
};
window.playPlaylist = function(name) {
    console.log('playPlaylist called:', name);
    alert('Playing playlist: ' + name + ' (stub)');
};
window.displaySearchResults = function() {
    console.log('displaySearchResults called');
    alert('Displaying search results (stub)');
};
window.showMusicDiscoveryModal = function() {
    console.log('showMusicDiscoveryModal called');
    alert('Showing music discovery modal (stub)');
};

// Initialize API when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.majorChordAPI = new MajorChordAPI();
    
    // Check if user is logged in
    const user = window.majorChordAPI.loadUserFromStorage();
    if (user) {
        console.log('User logged in:', user.username);
        // Update UI to show logged-in state
        updateUIForLoggedInUser(user);
    } else {
        console.log('No user logged in');
        // Update UI to show login/register options
        updateUIForLoggedOutUser();
    }
});

function updateUIForLoggedInUser(user) {
    // Update navigation
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.innerHTML = `
            <span>Welcome, ${user.username}!</span>
            <button onclick="logout()">Sign Out</button>
        `;
    }

    // Load user's health profile and recommendations
    loadUserData();
}

function updateUIForLoggedOutUser() {
    // Update navigation
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.innerHTML = `
            <a href="signin.html">Sign In</a>
            <a href="signup.html">Sign Up</a>
        `;
    }
}

async function loadUserData() {
    if (!window.majorChordAPI.isLoggedIn()) return;

    // Load health insights
    const insightsResult = await window.majorChordAPI.getHealthInsights();
    if (insightsResult.success) {
        displayHealthInsights(insightsResult.data);
    }

    // Load recommendations
    const recommendationsResult = await window.majorChordAPI.getRecommendations(6);
    if (recommendationsResult.success) {
        displayRecommendations(recommendationsResult.data.recommendations);
    }
}

async function logout() {
    if (!window.majorChordAPI) return;

    const result = await window.majorChordAPI.logout();
    if (result.success) {
        updateUIForLoggedOutUser();
        window.location.reload();
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MajorChordAPI;
} 