/**
 * Simple Auth Configuration for MajorChord
 * 
 * This file provides easy-to-use auth setup for any page.
 * Just include this file and call the appropriate function.
 */

// Auth configuration object
const AuthConfig = {
    // Protected pages - require authentication
    protectedPages: [
        'dashboard.html',
        'mood-assessment.html', 
        'goals.html',
        'chatbot.html',
        '/Demo-Music/dashboard',
        '/Demo-Music/mood-assessment',
        '/Demo-Music/goals',
        '/Demo-Music/chatbot'
    ],
    
    // Public pages - redirect if already logged in
    publicPages: [
        'signin.html',
        'signup.html',
        'index.html',
        '/Demo-Music/signin',
        '/Demo-Music/signup',
        '/Demo-Music'
    ],
    
    // Check if current page is protected
    isProtectedPage() {
        const currentPath = window.location.pathname;
        const currentPage = currentPath.split('/').pop() || 'index.html';
        
        return this.protectedPages.some(page => 
            currentPath.includes(page) || currentPage === page
        );
    },
    
    // Check if current page is public
    isPublicPage() {
        const currentPath = window.location.pathname;
        const currentPage = currentPath.split('/').pop() || 'index.html';
        
        return this.publicPages.some(page => 
            currentPath.includes(page) || currentPage === page
        );
    },
    
    // Auto-configure auth based on page type
    autoConfigure() {
        if (this.isProtectedPage()) {
            console.log('Auto-configuring protected page');
            this.protectPage();
        } else if (this.isPublicPage()) {
            console.log('Auto-configuring public page');
            this.publicPage();
        } else {
            console.log('Page type not configured, using default auth check');
            this.defaultAuth();
        }
    },
    
    // Protect a page (require authentication)
    protectPage() {
        document.addEventListener('DOMContentLoaded', async function() {
            if (window.authUtils) {
                const isAuthenticated = await window.authUtils.checkAuth();
                if (!isAuthenticated) {
                    return; // checkAuth handles the redirect
                }
                console.log('Protected page authenticated successfully');
            } else {
                console.log('Auth utilities not available');
            }
        });
    },
    
    // Public page (redirect if logged in)
    publicPage() {
        document.addEventListener('DOMContentLoaded', async function() {
            if (window.authUtils) {
                await window.authUtils.redirectIfLoggedIn();
                console.log('Public page loaded');
            } else {
                console.log('Auth utilities not available');
            }
        });
    },
    
    // Default auth behavior
    defaultAuth() {
        document.addEventListener('DOMContentLoaded', async function() {
            if (window.authManager) {
                await window.authManager.init();
                console.log('Default auth initialized');
            }
        });
    }
};

// Auto-configure when script loads
if (typeof window !== 'undefined') {
    // Wait for auth manager to be available
    const waitForAuth = () => {
        if (window.authManager && window.authUtils) {
            AuthConfig.autoConfigure();
        } else {
            setTimeout(waitForAuth, 100);
        }
    };
    waitForAuth();
}

// Make AuthConfig globally available
if (typeof window !== 'undefined') {
    window.AuthConfig = AuthConfig;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthConfig;
} 