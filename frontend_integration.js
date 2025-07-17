/**
 * MajorChord Frontend Integration
 * JavaScript functions to interact with the Flask backend API
 */

function getApiBaseUrl() {
    if (window.env && window.env.API_BASE_URL) {
        return window.env.API_BASE_URL;
    }
    
    // Dynamically determine the base URL based on current location
    const protocol = window.location.protocol;
    const host = window.location.host;
    const pathname = window.location.pathname;
    
    // If we're on a path that includes /Demo-Music, use the current origin
    if (pathname.includes('/Demo-Music')) {
        return `${protocol}//${host}/api`;
    }
    
    return 'http://localhost:5001/api';
}

// Helper function to generate navigation URLs that preserve path structure
function getNavigationUrl(page) {
    const currentPath = window.location.pathname;
    if (currentPath.includes('/Demo-Music')) {
        return `/Demo-Music/${page}`;
    }
    return `${page}.html`;
}

class MajorChordAPI {
    constructor() {
        this.baseURL = getApiBaseUrl();
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

    async login(email, password) {
        try {
            const response = await fetch(`${this.baseURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
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
            console.error('Login API error:', error);
            return { success: false, error: `Network error: ${error.message}` };
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

    // NEW: Validate session with backend
    async validateSession() {
        try {
            // Use the simpler session-check endpoint
            const response = await fetch(`${this.baseURL}/session-check`, {
                method: 'GET',
                credentials: 'include'
            });

            console.log('Session validation response status:', response.status);
            
            if (response.ok) {
                const data = await response.json();
                console.log('Session validation response data:', data);
                
                // If we get authenticated: true, session is valid
                if (data.authenticated) {
                    return { success: true, data: { user_id: data.user_id, username: data.username } };
                } else {
                    return { success: false, error: 'Session invalid' };
                }
            } else if (response.status === 401) {
                console.log('Session validation failed: 401 Unauthorized');
                return { success: false, error: 'Session invalid' };
            } else {
                console.log('Session validation failed: Unexpected status', response.status);
                return { success: false, error: 'Session validation failed' };
            }
        } catch (error) {
            console.error('Session validation error:', error);
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
        return userData ? JSON.parse(userData) : null;
    }

    isLoggedIn() {
        return this.user !== null;
    }
}

// Simplified Authentication Manager
class SimpleAuthManager {
    constructor() {
        this.api = new MajorChordAPI();
        this.currentUser = null;
        this.isInitialized = false;
    }

    // Initialize and validate session
    async init() {
        console.log('SimpleAuthManager: Initializing...');
        
        // First try to load from storage
        this.currentUser = this.api.loadUserFromStorage();
        console.log('SimpleAuthManager: User from storage:', this.currentUser);
        
        if (this.currentUser) {
            console.log('SimpleAuthManager: User found in storage, validating with backend...');
            
            // Validate session with backend
            const validation = await this.api.validateSession();
            console.log('SimpleAuthManager: Validation result:', validation);
            
            if (validation.success) {
                console.log('SimpleAuthManager: Session validated successfully');
                this.updateUI();
                this.isInitialized = true;
                return this.currentUser;
            } else {
                console.log('SimpleAuthManager: Session validation failed, but keeping user data as fallback. Error:', validation.error);
                // Don't clear user data immediately - keep it as a fallback
                // The user might still be logged in but the backend validation failed
                this.updateUI();
                this.isInitialized = true;
                return this.currentUser;
            }
        }
        
        console.log('SimpleAuthManager: No valid session found');
        this.updateUI();
        this.isInitialized = true;
        return null;
    }

    // Check if user is logged in
    isLoggedIn() {
        return this.currentUser !== null;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Login
    async login(email, password) {
        console.log('SimpleAuthManager: Attempting login...');
        const result = await this.api.login(email, password);
        console.log('SimpleAuthManager: Login result:', result);
        
        if (result.success) {
            this.currentUser = result.data;
            console.log('SimpleAuthManager: Login successful, user set to:', this.currentUser);
            this.updateUI();
        } else {
            console.log('SimpleAuthManager: Login failed:', result.error);
        }
        return result;
    }

    // Logout
    async logout() {
        const result = await this.api.logout();
        if (result.success) {
            this.currentUser = null;
            this.updateUI();
        }
        return result;
    }

    // Update UI based on auth state
    updateUI() {
        if (this.isLoggedIn()) {
            this.showLoggedInState();
        } else {
            this.showLoggedOutState();
        }
    }

    // Show logged in state
    showLoggedInState() {
        const user = this.currentUser;
        
        // Hide auth links
        const authLinks = document.getElementById('authLinks');
        const signinLink = document.getElementById('signinLink');
        const signupLink = document.getElementById('signupLink');
        
        if (authLinks) authLinks.style.display = 'none';
        if (signinLink) signinLink.style.display = 'none';
        if (signupLink) signupLink.style.display = 'none';

        // Show user section
        const userSection = document.getElementById('userSection');
        if (userSection) userSection.style.display = 'flex';

        // Update user info
        const userName = document.getElementById('userName');
        const profileName = document.getElementById('profileName');
        const profileEmail = document.getElementById('profileEmail');
        const profileInitials = document.getElementById('profileInitials');
        const profileInitialsLarge = document.getElementById('profileInitialsLarge');

        if (userName) userName.textContent = user.username || 'User';
        if (profileName) profileName.textContent = user.username || 'User';
        if (profileEmail) profileEmail.textContent = user.email || '';

        // Update profile initials
        const initials = (user.username || 'U').substring(0, 1).toUpperCase();
        if (profileInitials) profileInitials.textContent = initials;
        if (profileInitialsLarge) profileInitialsLarge.textContent = initials;
    }

    // Show logged out state
    showLoggedOutState() {
        // Show auth links
        const authLinks = document.getElementById('authLinks');
        const signinLink = document.getElementById('signinLink');
        const signupLink = document.getElementById('signupLink');
        
        if (authLinks) authLinks.style.display = 'flex';
        if (signinLink) signinLink.style.display = 'inline-block';
        if (signupLink) signupLink.style.display = 'inline-block';

        // Hide user section
        const userSection = document.getElementById('userSection');
        if (userSection) userSection.style.display = 'none';
    }

    // Check auth and redirect if needed
    async requireAuth(redirectUrl = null) {
        if (!this.isInitialized) {
            await this.init();
        }
        
        if (!this.isLoggedIn()) {
            const currentPath = window.location.pathname;
            if (currentPath.includes('/Demo-Music')) {
                window.location.href = redirectUrl || '/Demo-Music/signin';
            } else {
                window.location.href = redirectUrl || 'signin.html';
            }
            return false;
        }
        return true;
    }
}

// Initialize global auth manager
window.authManager = new SimpleAuthManager();

// Initialize when page loads
document.addEventListener('DOMContentLoaded', async function() {
    window.majorChordAPI = new MajorChordAPI();
    
    // Initialize authentication state
    const user = await window.authManager.init();
    
    if (user) {
        console.log('User logged in:', user.username);
    } else {
        console.log('No user logged in');
    }
});

// Legacy functions for backward compatibility
function updateUIForLoggedInUser(user) {
    if (window.authManager) {
        window.authManager.updateUI();
    }
}

function updateUIForLoggedOutUser() {
    if (window.authManager) {
        window.authManager.updateUI();
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
    if (!window.authManager) return;

    const result = await window.authManager.logout();
    if (result.success) {
        window.location.reload();
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MajorChordAPI;
}

// === SIMPLIFIED AUTH UTILITIES ===

// Simple auth check function that can be used on any page
async function checkAuth() {
    if (!window.authManager) {
        console.log('Auth manager not available');
        return false;
    }
    
    const isAuthenticated = await window.authManager.requireAuth();
    return isAuthenticated;
}

// Simple auth redirect function for public pages (signin/signup)
async function redirectIfLoggedIn() {
    if (!window.authManager) {
        return;
    }
    
    const user = await window.authManager.init();
    if (user) {
        const currentPath = window.location.pathname;
        if (currentPath.includes('/Demo-Music')) {
            window.location.href = '/Demo-Music/dashboard';
        } else {
            window.location.href = 'dashboard.html';
        }
    }
}

// Simple logout function
async function simpleLogout() {
    if (!window.authManager) {
        return;
    }
    
    const result = await window.authManager.logout();
    if (result.success) {
        const currentPath = window.location.pathname;
        if (currentPath.includes('/Demo-Music')) {
            window.location.href = '/Demo-Music/signin';
        } else {
            window.location.href = 'signin.html';
        }
    }
}

// Auth wrapper for protected pages
function protectPage() {
    document.addEventListener('DOMContentLoaded', async function() {
        const isAuthenticated = await checkAuth();
        if (!isAuthenticated) {
            return; // requireAuth handles the redirect
        }
        
        // Page is now authenticated, continue with normal initialization
        console.log('Page authenticated successfully');
    });
}

// Auth wrapper for public pages
function publicPage() {
    document.addEventListener('DOMContentLoaded', async function() {
        await redirectIfLoggedIn();
        console.log('Public page loaded');
    });
}

// Make auth utilities globally available
window.authUtils = {
    checkAuth,
    redirectIfLoggedIn,
    simpleLogout,
    protectPage,
    publicPage
}; 