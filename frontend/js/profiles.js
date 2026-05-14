/**
 * Profils de Sinistres par Domaine d'Activite
 * Permet aux utilisateurs de choisir leur secteur d'activite
 */

const PROFILES_MODULE = {
    /**
     * Definition des profils de sinistres par domaine
     */
    profiles: {
        medical: {
            label: 'Assurance Sante',
            description: 'Risques medicaux et hospitaliers',
            icon: '[+] SANTE',
            sinistres: {
                consultation: { lambda: 2.0, cout_moyen: 5000, nom_complet: 'Consultation medicale' },
                hospitalisation: { lambda: 0.3, cout_moyen: 250000, nom_complet: 'Hospitalisation' },
                chirurgie: { lambda: 0.1, cout_moyen: 1000000, nom_complet: 'Chirurgie' },
                medicaments: { lambda: 1.5, cout_moyen: 30000, nom_complet: 'Medicaments' }
            }
        },
        automobile: {
            label: 'Assurance Automobile',
            description: 'Sinistres automobiles et responsabilite civile',
            icon: 'TRANSPORT',
            sinistres: {
                tierce: { lambda: 0.2, cout_moyen: 50000, nom_complet: 'Responsabilite Civile' },
                dommages: { lambda: 0.15, cout_moyen: 150000, nom_complet: 'Dommages Materiel' },
                vol: { lambda: 0.05, cout_moyen: 500000, nom_complet: 'Vol du Vehicle' },
                assistance: { lambda: 0.1, cout_moyen: 20000, nom_complet: 'Assistance Routiere' }
            }
        },
        immobilier: {
            label: 'Assurance Immobiliere',
            description: 'Sinistres lies aux biens immobiliers',
            icon: 'BATIMENT',
            sinistres: {
                incendie: { lambda: 0.05, cout_moyen: 1000000, nom_complet: 'Incendie' },
                degats_eau: { lambda: 0.08, cout_moyen: 300000, nom_complet: 'Degats des Eaux' },
                vol_cambriolage: { lambda: 0.03, cout_moyen: 500000, nom_complet: 'Vol et Cambriolage' },
                responsabilite: { lambda: 0.02, cout_moyen: 100000, nom_complet: 'Responsabilite Civile' }
            }
        },
        commerce: {
            label: 'Assurance Commerciale',
            description: 'Risques lies a l\'activite commerciale',
            icon: 'MAGASIN',
            sinistres: {
                pertes_exploitation: { lambda: 0.1, cout_moyen: 500000, nom_complet: 'Pertes d\'Exploitation' },
                responsabilite_civile: { lambda: 0.08, cout_moyen: 200000, nom_complet: 'Responsabilite Civile' },
                vol_marchandises: { lambda: 0.05, cout_moyen: 300000, nom_complet: 'Vol de Marchandises' },
                clients_insolvables: { lambda: 0.12, cout_moyen: 100000, nom_complet: 'Clients Insolvables' }
            }
        },
        agriculture: {
            label: 'Assurance Agricole',
            description: 'Sinistres agricoles et recoltes',
            icon: 'CULTURE',
            sinistres: {
                secheresse: { lambda: 0.15, cout_moyen: 800000, nom_complet: 'Secheresse' },
                gelees: { lambda: 0.08, cout_moyen: 600000, nom_complet: 'Gelees' },
                tempetes: { lambda: 0.1, cout_moyen: 750000, nom_complet: 'Tempetes' },
                maladies_cultures: { lambda: 0.06, cout_moyen: 400000, nom_complet: 'Maladies des Cultures' }
            }
        },
        cyber: {
            label: 'Assurance Cyber',
            description: 'Risques cybernetiques et donnees',
            icon: 'CYBER',
            sinistres: {
                violation_donnees: { lambda: 0.05, cout_moyen: 1000000, nom_complet: 'Violation de Donnees' },
                ransomware: { lambda: 0.08, cout_moyen: 800000, nom_complet: 'Attaque Ransomware' },
                indisponibilite: { lambda: 0.1, cout_moyen: 300000, nom_complet: 'Indisponibilite Systeme' },
                responsabilite: { lambda: 0.03, cout_moyen: 500000, nom_complet: 'Responsabilite Civile Cyber' }
            }
        }
    },

    /**
     * Profil actuellement selectionne
     */
    currentProfile: 'medical',

    /**
     * Initialiser les profils
     */
    init() {
        this.loadProfile(this.currentProfile);
    },

    /**
     * Obtenir la liste des profils disponibles
     */
    getProfiles() {
        return Object.keys(this.profiles).map(key => ({
            id: key,
            ...this.profiles[key]
        }));
    },

    /**
     * Obtenir un profil par sa clef
     */
    getProfile(profileId) {
        return this.profiles[profileId] || this.profiles['medical'];
    },

    /**
     * Charger un profil et mettre a jour les sinistres
     */
    loadProfile(profileId) {
        if (!this.profiles[profileId]) {
            console.error('Profil introuvable:', profileId);
            return false;
        }

        this.currentProfile = profileId;
        const profile = this.profiles[profileId];

        // Mettre a jour le module des sinistres
        if (typeof SINISTRES_MODULE !== 'undefined') {
            SINISTRES_MODULE.sinistres = JSON.parse(JSON.stringify(profile.sinistres));
            SINISTRES_MODULE.createFormFields('sinistreContainer');
        }

        console.log('Profil charge:', profileId, profile.label);
        return true;
    },

    /**
     * Obtenir le label d'un profil
     */
    getProfileLabel(profileId) {
        return this.profiles[profileId]?.label || 'Inconnu';
    },

    /**
     * Obtenir la description d'un profil
     */
    getProfileDescription(profileId) {
        return this.profiles[profileId]?.description || '';
    },

    /**
     * Creer les boutons de selection des profils
     */
    createProfileSelector(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';
        container.style.display = 'grid';
        container.style.gridTemplateColumns = 'repeat(auto-fit, minmax(150px, 1fr))';
        container.style.gap = '12px';
        container.style.marginBottom = '20px';

        const profiles = this.getProfiles();

        for (const profile of profiles) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'profile-btn';
            if (profile.id === this.currentProfile) {
                btn.classList.add('active');
            }

            btn.innerHTML = `
                <div style="font-size: 24px; margin-bottom: 8px;">${profile.icon}</div>
                <div style="font-weight: 600; font-size: 13px; margin-bottom: 4px;">${profile.label}</div>
                <div style="font-size: 11px; color: #94A3B8;">${profile.description}</div>
            `;

            btn.addEventListener('click', () => {
                this.loadProfile(profile.id);
                this.createProfileSelector(containerId);
            });

            container.appendChild(btn);
        }
    }
};
