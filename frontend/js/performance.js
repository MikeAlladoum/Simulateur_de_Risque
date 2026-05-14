/**
 * PERFORMANCE OPTIMIZATION
 * Optimisation du rendu et des performances
 */

// Lazy loading pour images
document.addEventListener('DOMContentLoaded', () => {
    // Observer pour chargement différé
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Débounce pour événements fréquents
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle pour événements très fréquents
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Optimiser les animations
if (!window.requestAnimationFrame) {
    window.requestAnimationFrame = (callback) => {
        return setTimeout(callback, 1000 / 60);
    };
}

// Cache les requêtes API
const apiCache = new Map();

function getCachedData(key) {
    const cached = apiCache.get(key);
    if (cached && Date.now() - cached.timestamp < 5 * 60 * 1000) {
        return cached.data;
    }
    apiCache.delete(key);
    return null;
}

function setCachedData(key, data) {
    apiCache.set(key, { data, timestamp: Date.now() });
}

// Cleanup timeout
setTimeout(() => {
    apiCache.clear();
    console.log('Cache API nettoyé');
}, 30 * 60 * 1000);
