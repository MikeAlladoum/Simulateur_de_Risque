/**
 * Module d'Authentification JWT
 * Gère login/logout et stockage du token
 */

const AUTH = {
    // Nom de la clé de stockage du token
    TOKEN_KEY: 'simulateur_token',
    USER_KEY: 'simulateur_user',
    
    /**
     * Effectue la connexion
     */
    async login(username, password) {
        try {
            const response = await fetch(`${CONFIG.API.BASE_URL.replace('/api', '')}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Erreur de connexion');
            }
            
            // Stockage du token et de l'utilisateur
            localStorage.setItem(AUTH.TOKEN_KEY, data.access_token);
            localStorage.setItem(AUTH.USER_KEY, data.user);
            
            return {
                success: true,
                user: data.user,
                message: data.message
            };
        } catch (error) {
            console.error('Erreur login:', error.message);
            return {
                success: false,
                error: error.message
            };
        }
    },
    
    /**
     * Effectue la déconnexion
     */
    logout() {
        localStorage.removeItem(AUTH.TOKEN_KEY);
        localStorage.removeItem(AUTH.USER_KEY);
        window.location.href = '/';
    },
    
    /**
     * Récupère le token stocké
     */
    getToken() {
        return localStorage.getItem(AUTH.TOKEN_KEY);
    },
    
    /**
     * Récupère l'utilisateur connecté
     */
    getCurrentUser() {
        return localStorage.getItem(AUTH.USER_KEY);
    },
    
    /**
     * Vérifie si l'utilisateur est connecté
     */
    isAuthenticated() {
        return !!AUTH.getToken();
    },
    
    /**
     * Redirige vers la page de login si pas connecté
     */
    requireAuth() {
        if (!AUTH.isAuthenticated()) {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    }
};

// Export pour utilisation
window.AUTH = AUTH;
