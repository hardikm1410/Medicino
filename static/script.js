// Medicino Web Application - Complete JavaScript Implementation
// Author: AI Assistant
// Version: 1.1

// Global Configuration
// Dynamically set API URLs based on the environment
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

const CONFIG = {
    // Correctly set API_BASE_URL for both environments
    API_BASE_URL: isLocalhost ? 'http://localhost:5000/api' : '/api',
    CURRENT_BACKEND: 'flask', // 'flask' or 'django'
    VOICE_RECOGNITION_TIMEOUT: 10000,
    API_TIMEOUT: 10000
};

// Global State Management
const AppState = {
    isListening: false,
    currentDiagnosis: null,
    diagnosisHistory: [],
    allMedicines: [],
    isLoading: false
};

// Utility Functions
const Utils = {
    // Show/hide elements with animation
    show: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.classList.remove('hidden');
            element.style.animation = 'fadeIn 0.5s ease-out';
        }
    },

    hide: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.classList.add('hidden');
        }
    },

    // Show loading state
    showLoader: (loaderId) => {
        Utils.show(loaderId);
    },

    hideLoader: (loaderId) => {
        Utils.hide(loaderId);
    },

    // Format text for display
    formatText: (text) => {
        if (!text) return 'Not available';
        return text.charAt(0).toUpperCase() + text.slice(1);
    },

    // Clean and validate symptoms input
    cleanSymptoms: (symptoms) => {
        return symptoms
            .toLowerCase()
            .trim()
            .replace(/[^\w\s,.-]/g, '')
            .replace(/\s+/g, ' ');
    },

    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
        `;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
            font-weight: 500;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    },

    // Validate symptoms input
    validateSymptoms: (symptoms) => {
        const cleaned = Utils.cleanSymptoms(symptoms);
        if (!cleaned || cleaned.length < 3) {
            return { valid: false, message: 'Please enter at least 3 characters describing your symptoms' };
        }
        if (cleaned.length > 500) {
            return { valid: false, message: 'Symptoms description is too long (max 500 characters)' };
        }
        return { valid: true, cleaned: cleaned };
    }
};

// API Service
const ApiService = {
    // Generic API request function
    request: async (endpoint, options = {}) => {
        // Use the common API_BASE_URL for all requests
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: CONFIG.API_TIMEOUT
        };

        const requestOptions = { ...defaultOptions, ...options };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), requestOptions.timeout);

            const response = await fetch(url, {
                ...requestOptions,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout. Please check your connection and try again.');
            }
            throw error;
        }
    },

    // Diagnose symptoms
    diagnose: async (symptoms) => {
        // Correct endpoint for Flask backend
        const endpoint = '/diagnose';
        return await ApiService.request(endpoint, {
            method: 'POST',
            body: JSON.stringify({ symptoms: symptoms })
        });
    },

    // Get medicine information
    getMedicine: async (medicineName) => {
        // Correct endpoint for Flask backend
        const endpoint = `/medicine/${encodeURIComponent(medicineName)}`;
        return await ApiService.request(endpoint);
    },

    // Get all medicines
    getAllMedicines: async () => {
        // Correct endpoint for Flask backend
        const endpoint = '/medicines';
        return await ApiService.request(endpoint);
    },

    // Get diagnosis history
    getHistory: async () => {
        // Correct endpoint for Flask backend
        const endpoint = '/history';
        return await ApiService.request(endpoint);
    }
};

// Voice Recognition Service
const VoiceService = {
    recognition: null,
    isSupported: false,

    init: () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            VoiceService.recognition = new SpeechRecognition();
            VoiceService.recognition.continuous = false;
            VoiceService.recognition.interimResults = false;
            VoiceService.recognition.lang = 'en-US';
            VoiceService.isSupported = true;

            VoiceService.recognition.onstart = () => {
                AppState.isListening = true;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
                Utils.showNotification('Listening... Please speak your symptoms clearly', 'info');
            };

            VoiceService.recognition.onend = () => {
                AppState.isListening = false;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';
            };

            VoiceService.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                AppState.isListening = false;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';

                let errorMessage = 'Voice recognition error. ';
                switch (event.error) {
                    case 'no-speech':
                        errorMessage += 'No speech detected. Please try again.';
                        break;
                    case 'network':
                        errorMessage += 'Network error. Please check your connection.';
                        break;
                    case 'not-allowed':
                        errorMessage += 'Microphone access denied. Please enable microphone permissions.';
                        break;
                    default:
                        errorMessage += 'Please try again.';
                }
                Utils.showNotification(errorMessage, 'error');
            };

            VoiceService.recognition.onresult = (event) => {
                const result = event.results[0][0].transcript;
                document.getElementById('symptomsInput').value = result;
                Utils.showNotification(`Voice input received: "${result}"`, 'success');
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    },

    start: () => {
        if (VoiceService.isSupported && VoiceService.recognition && !AppState.isListening) {
            try {
                VoiceService.recognition.start();
            } catch (error) {
                console.error('Error starting voice recognition:', error);
                Utils.showNotification('Could not start voice recognition. Please try again.', 'error');
            }
        } else if (!VoiceService.isSupported) {
            Utils.showNotification('Voice recognition is not supported in your browser', 'error');
        }
    },

    stop: () => {
        if (VoiceService.recognition && AppState.isListening) {
            VoiceService.recognition.stop();
        }
    }
};

// Diagnosis Handler
const DiagnosisHandler = {
    diagnose: async () => {
        console.log('🚀 DiagnosisHandler.diagnose() called');
        const symptomsInput = document.getElementById('symptomsInput');
        const symptoms = symptomsInput.value.trim();

        // Validate input
        const validation = Utils.validateSymptoms(symptoms);
        if (!validation.valid) {
            Utils.showNotification(validation.message, 'error');
            symptomsInput.focus();
            return;
        }

        const cleanedSymptoms = validation.cleaned;

        // Show loading state
        Utils.showLoader('diagnosisLoader');
        Utils.hide('diagnosisResult');

        const diagnoseBtn = document.getElementById('diagnoseBtn');
        const originalBtnText = diagnoseBtn.innerHTML;
        diagnoseBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        diagnoseBtn.disabled = true;

        try {
            const response = await ApiService.diagnose(cleanedSymptoms);

            if (response.success && response.data) {
                AppState.currentDiagnosis = response.data;
                DiagnosisHandler.displayResults(response.data);
                Utils.showNotification('Diagnosis completed successfully!', 'success');
            } else {
                throw new Error(response.message || 'Diagnosis failed');
            }
        } catch (error) {
            console.error('Diagnosis error:', error);
            Utils.showNotification(`Diagnosis failed: ${error.message}`, 'error');
            Utils.hide('diagnosisResult');
        } finally {
            Utils.hideLoader('diagnosisLoader');
            diagnoseBtn.innerHTML = originalBtnText;
            diagnoseBtn.disabled = false;
        }
    },

    displayResults: (data) => {
        // Update disease output
        document.getElementById('diseaseOutput').textContent = Utils.formatText(data.disease);

        // Update severity badge
        const severityBadge = document.getElementById('severityBadge');
        const severity = data.severity || 'unknown';
        severityBadge.innerHTML = `<span class="severity-badge severity-${severity}">
            <i class="fas fa-${DiagnosisHandler.getSeverityIcon(severity)}"></i>
            ${Utils.formatText(severity)} Severity
        </span>`;

        // Update Ayurvedic remedy
        document.getElementById('ayurvedicOutput').textContent = data.ayurvedic || 'No Ayurvedic remedy available';

        // Update medicine suggestion
        document.getElementById('medicineOutput').textContent = data.medicine || 'No medicine suggestion available';

        // Update confidence score
        const confidence = Math.min(Math.max(data.confidence || 0, 0), 100);
        document.getElementById('confidenceText').textContent = `${confidence.toFixed(1)}%`;

        // Animate confidence bar
        const confidenceFill = document.getElementById('confidenceFill');
        setTimeout(() => {
            confidenceFill.style.width = `${confidence}%`;
        }, 300);

        // Show results
        Utils.show('diagnosisResult');

        // Scroll to results
        document.getElementById('diagnosisResult').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    },

    getSeverityIcon: (severity) => {
        switch (severity.toLowerCase()) {
            case 'mild': return 'smile';
            case 'moderate': return 'meh';
            case 'severe': return 'frown';
            case 'critical': return 'exclamation-triangle';
            default: return 'question-circle';
        }
    },

    clear: () => {
        document.getElementById('symptomsInput').value = '';
        Utils.hide('diagnosisResult');
        Utils.hide('diagnosisLoader');
        AppState.currentDiagnosis = null;

        // Reset confidence bar
        document.getElementById('confidenceFill').style.width = '0%';
    }
};

// Medicine Handler
const MedicineHandler = {
    search: async () => {
        console.log('🚀 MedicineHandler.search() called');
        const medicineInput = document.getElementById('medicineInput');
        const medicineName = medicineInput.value.trim();

        if (!medicineName) {
            Utils.showNotification('Please enter a medicine name', 'error');
            medicineInput.focus();
            return;
        }

        if (medicineName.length < 2) {
            Utils.showNotification('Please enter at least 2 characters', 'error');
            return;
        }

        // Show loading state
        Utils.showLoader('medicineLoader');
        Utils.hide('medicineInfoResult');

        const searchBtn = document.getElementById('searchMedicineBtn');
        const originalBtnText = searchBtn.innerHTML;
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
        searchBtn.disabled = true;

        try {
            const response = await ApiService.getMedicine(medicineName);

            if (response.success && response.data) {
                MedicineHandler.displayMedicineInfo([response.data]);
                Utils.showNotification('Medicine found successfully!', 'success');
            } else {
                Utils.showNotification('Medicine not found. Try a different name or check spelling.', 'error');
                document.getElementById('medicineInfoResult').innerHTML = `
                    <div class="medicine-card" style="text-align: center; color: var(--text-secondary);">
                        <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                        <h3>Medicine Not Found</h3>
                        <p>We couldn't find "${medicineName}" in our database.</p>
                        <p>Try searching with a different name or check the spelling.</p>
                    </div>
                `;
                Utils.show('medicineInfoResult');
            }
        } catch (error) {
            console.error('Medicine search error:', error);
            Utils.showNotification(`Search failed: ${error.message}`, 'error');
        } finally {
            Utils.hideLoader('medicineLoader');
            searchBtn.innerHTML = originalBtnText;
            searchBtn.disabled = false;
        }
    },

    showAll: async () => {
        console.log('🚀 MedicineHandler.showAll() called');
        Utils.showLoader('medicineLoader');
        Utils.hide('medicineInfoResult');

        const showAllBtn = document.getElementById('showAllBtn');
        const originalBtnText = showAllBtn.innerHTML;
        showAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        showAllBtn.disabled = true;

        try {
            const response = await ApiService.getAllMedicines();

            if (response.success && response.data && response.data.length > 0) {
                AppState.allMedicines = response.data;
                MedicineHandler.displayMedicineInfo(response.data);
                Utils.showNotification(`Found ${response.data.length} medicines`, 'success');
            } else {
                Utils.showNotification('No medicines found in database', 'error');
            }
        } catch (error) {
            console.error('Error loading medicines:', error);
            Utils.showNotification(`Failed to load medicines: ${error.message}`, 'error');
        } finally {
            Utils.hideLoader('medicineLoader');
            showAllBtn.innerHTML = originalBtnText;
            showAllBtn.disabled = false;
        }
    },

    displayMedicineInfo: (medicines) => {
        console.log('🚀 MedicineHandler.displayMedicineInfo() called');
        const resultDiv = document.getElementById('medicineInfoResult');

        if (!medicines || medicines.length === 0) {
            resultDiv.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No medicines found.</p>';
            Utils.show('medicineInfoResult');
            return;
        }

        let html = '';

        if (medicines.length > 1) {
            html += `<h3 style="margin-bottom: 1.5rem; color: #f093fb;">
                <i class="fas fa-pills"></i> Found ${medicines.length} Medicines
            </h3>`;
        }

        medicines.forEach(medicine => {
            html += `
                <div class="medicine-card">
                    <div class="medicine-name">
                        <i class="fas fa-capsules"></i>
                        ${Utils.formatText(medicine.name)}
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-info-circle"></i> Description:</strong>
                        <span>${medicine.description || 'Not available'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-prescription-bottle-alt"></i> Dosage:</strong>
                        <span>${medicine.dosage || 'Consult healthcare provider'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-exclamation-triangle"></i> Side Effects:</strong>
                        <span>${medicine.side_effects || 'Not specified'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-ban"></i> Contraindications:</strong>
                        <span>${medicine.contraindications || 'Not specified'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-tag"></i> Category:</strong>
                        <span class="category-tag">${Utils.formatText(medicine.category || 'general')}</span>
                    </div>

                    <div class="medicine-detail" style="align-items: center; margin-top: 1rem;">
                        <strong><i class="fas fa-rupee-sign"></i> Price:</strong>
                        <span class="price-tag">
                            <i class="fas fa-rupee-sign"></i>
                            ${medicine.price ? parseFloat(medicine.price).toFixed(2) : 'N/A'}
                        </span>
                    </div>
                </div>
            `;
        });

        resultDiv.innerHTML = html;
        Utils.show('medicineInfoResult');

        // Scroll to results if showing all medicines
        if (medicines.length > 3) {
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
};

// Backend Switcher (for testing different backends)
const BackendSwitcher = {
    // Note: The original `switch` function has been removed because it's no longer needed
    // with the dynamic API URL in the CONFIG object.

    detectAvailableBackend: async () => {
        // Try Flask first
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/medicines`, {
                method: 'GET',
                timeout: 3000
            });
            if (response.ok) {
                CONFIG.CURRENT_BACKEND = 'flask';
                console.log('Flask backend detected and active');
                return 'flask';
            }
        } catch (error) {
            console.log('Flask backend not available:', error.message);
        }

        // Try Django (Removed the call to django backend as it is not needed now.)
        // Django URLs can be different so the logic might need to be
        // re-introduced if django backend needs to be supported.
       
        // No backend available
        Utils.showNotification('No backend server detected. Please start Flask server.', 'error');
        return null;
    }
};

// --- MODAL HANDLERS (FIXED) ---

const EmergencyHandler = {
    show: () => {
        const modalContainer = document.createElement('div');
        modalContainer.className = 'modal-overlay';
        modalContainer.onclick = EmergencyHandler.close;

        modalContainer.innerHTML = `
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header emergency-header">
                    <h2><i class="fas fa-exclamation-triangle"></i> Emergency Guidelines</h2>
                    <button class="close-btn" onclick="EmergencyHandler.close()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="emergency-section">
                        <h3><i class="fas fa-phone"></i> Emergency Numbers (India)</h3>
                        <ul>
                            <li><strong>108</strong> - Emergency Ambulance</li>
                            <li><strong>102</strong> - Medical Emergency</li>
                            <li><strong>100</strong> - Police</li>
                            <li><strong>101</strong> - Fire Department</li>
                        </ul>
                    </div>
                    <div class="emergency-section">
                        <h3><i class="fas fa-heart"></i> When to Seek Immediate Medical Attention</h3>
                        <ul>
                            <li>Chest pain or pressure</li>
                            <li>Difficulty breathing</li>
                            <li>Severe allergic reactions</li>
                            <li>High fever (above 103°F/39.4°C)</li>
                            <li>Severe head injury</li>
                            <li>Unconsciousness</li>
                            <li>Severe bleeding</li>
                            <li>Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency)</li>
                        </ul>
                    </div>
                    <div class="emergency-section">
                        <h3><i class="fas fa-first-aid"></i> Basic First Aid</h3>
                        <ul>
                            <li><strong>For cuts:</strong> Apply pressure with clean cloth</li>
                            <li><strong>For burns:</strong> Cool with cold water for 10-20 minutes</li>
                            <li><strong>For choking:</strong> Perform Heimlich maneuver</li>
                            <li><strong>For unconsciousness:</strong> Check breathing, place in recovery position</li>
                        </ul>
                    </div>
                    <div class="emergency-disclaimer">
                        <p><strong>⚠️ Disclaimer:</strong> This app is for informational purposes only and should not replace professional medical advice. In case of emergency, always call emergency services immediately.</p>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modalContainer);
    },
    close: () => {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }
};

const AboutHandler = {
    show: () => {
        const modalContainer = document.createElement('div');
        modalContainer.className = 'modal-overlay';
        modalContainer.onclick = AboutHandler.close;

        modalContainer.innerHTML = `
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h2><i class="fas fa-info-circle"></i> About Medicino</h2>
                    <button class="close-btn" onclick="AboutHandler.close()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="about-section">
                        <h3><i class="fas fa-brain"></i> What is Medicino?</h3>
                        <p>Medicino is an AI-powered medical assistant that helps you understand your symptoms and provides intelligent health recommendations. Our system combines modern medical knowledge with traditional Ayurvedic wisdom to offer comprehensive health guidance.</p>
                    </div>
                    <div class="about-section">
                        <h3><i class="fas fa-cogs"></i> Features</h3>
                        <ul>
                            <li><strong>Smart Symptom Analysis:</strong> AI-powered diagnosis with confidence scoring</li>
                            <li><strong>Dual Treatment Approach:</strong> Modern medicine + Ayurvedic remedies</li>
                            <li><strong>Medicine Database:</strong> Comprehensive information on medications</li>
                            <li><strong>Voice Input:</strong> Speak your symptoms naturally</li>
                            <li><strong>History Tracking:</strong> Keep track of your consultations</li>
                            <li><strong>Emergency Guidelines:</strong> Quick access to emergency information</li>
                        </ul>
                    </div>
                    <div class="about-section">
                        <h3><i class="fas fa-shield-alt"></i> Technology Stack</h3>
                        <ul>
                            <li><strong>Frontend:</strong> HTML5, CSS3, JavaScript (ES6+)</li>
                            <li><strong>Backend:</strong> Flask/Django Python Framework</li>
                            <li><strong>Database:</strong> SQLite with optimized indexing</li>
                            <li><strong>AI Engine:</strong> Custom symptom matching algorithm</li>
                            <li><strong>Voice Recognition:</strong> Web Speech API</li>
                        </ul>
                    </div>
                    <div class="about-section">
                        <h3><i class="fas fa-users"></i> How It Works</h3>
                        <ol>
                            <li>Enter your symptoms via text or voice input</li>
                            <li>Our AI analyzes your symptoms against medical database</li>
                            <li>Receive diagnosis with confidence score</li>
                            <li>Get both modern medicine and Ayurvedic recommendations</li>
                            <li>Access detailed medicine information from our database</li>
                        </ol>
                    </div>
                    <div class="about-disclaimer">
                        <h4><i class="fas fa-exclamation-triangle"></i> Important Disclaimer</h4>
                        <p>Medicino is designed for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns. In case of emergency, contact emergency services immediately.</p>
                    </div>
                    <div class="about-footer">
                        <p><strong>Version:</strong> 1.0.0</p>
                        <p><strong>Last Updated:</strong> ${new Date().toLocaleDateString()}</p>
                        <p><strong>Support:</strong> For technical support or feedback, please contact our development team.</p>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modalContainer);
    },
    close: () => {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }
};

const HistoryHandler = {
    show: async () => {
        // This is a mock implementation since ApiService is not available here.
        // In your real script, this would make an API call.
        const mockHistory = [
            { created_at: new Date(), symptoms: 'fever, headache', diagnosed_condition: 'Viral Fever', confidence_score: 85, ayurvedic_remedy: 'Drink warm water with ginger and honey.', medicine_suggestion: 'Paracetamol' },
            { created_at: new Date(Date.now() - 86400000), symptoms: 'cough, sore throat', diagnosed_condition: 'Common Cold', confidence_score: 92, ayurvedic_remedy: 'Gargle with warm salt water.', medicine_suggestion: 'Cetirizine' }
        ];
        HistoryHandler.displayHistory(mockHistory);
    },
    displayHistory: (history) => {
        const modalContainer = document.createElement('div');
        modalContainer.className = 'modal-overlay';
        modalContainer.onclick = HistoryHandler.close;
        
        let historyContent = '';
        if (!history || history.length === 0) {
            historyContent = `
                <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                    <i class="fas fa-history" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <h3>No Diagnosis History</h3>
                    <p>You haven't made any diagnoses yet. Start by analyzing your symptoms!</p>
                </div>
            `;
        } else {
            historyContent = `<div class="history-list">` + history.map((record, index) => `
                <div class="history-item">
                    <div class="history-header">
                        <strong>Diagnosis #${history.length - index}</strong>
                        <span class="history-date">${new Date(record.created_at).toLocaleString()}</span>
                    </div>
                    <div class="history-content">
                        <p><strong>Symptoms:</strong> ${record.symptoms}</p>
                        <p><strong>Condition:</strong> ${record.diagnosed_condition}</p>
                        <p><strong>Confidence:</strong> ${record.confidence_score}%</p>
                        <p><strong>Ayurvedic Remedy:</strong> ${record.ayurvedic_remedy}</p>
                        <p><strong>Medicine:</strong> ${record.medicine_suggestion}</p>
                    </div>
                </div>
            `).join('') + `</div>`;
        }

        modalContainer.innerHTML = `
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h2><i class="fas fa-history"></i> Diagnosis History</h2>
                    <button class="close-btn" onclick="HistoryHandler.close()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${historyContent}
                </div>
            </div>
        `;
        document.body.appendChild(modalContainer);
    },
    close: () => {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }
};

// Event Listeners Setup
const EventListeners = {
    init: () => {
        console.log('🔧 Initializing event listeners...');
        
        try {
            // Diagnosis functionality
            const diagnoseBtn = document.getElementById('diagnoseBtn');
            const voiceBtn = document.getElementById('voiceBtn');
            const clearBtn = document.getElementById('clearBtn');
            
            if (diagnoseBtn) {
                diagnoseBtn.addEventListener('click', DiagnosisHandler.diagnose);
                console.log('✅ diagnoseBtn listener added');
            } else {
                console.error('❌ diagnoseBtn not found');
            }
            
            if (voiceBtn) {
                voiceBtn.addEventListener('click', VoiceService.start);
                console.log('✅ voiceBtn listener added');
            } else {
                console.error('❌ voiceBtn not found');
            }
            
            if (clearBtn) {
                clearBtn.addEventListener('click', DiagnosisHandler.clear);
                console.log('✅ clearBtn listener added');
            } else {
                console.error('❌ clearBtn not found');
            }

            // Medicine functionality
            const searchMedicineBtn = document.getElementById('searchMedicineBtn');
            const showAllBtn = document.getElementById('showAllBtn');
            
            if (searchMedicineBtn) {
                searchMedicineBtn.addEventListener('click', MedicineHandler.search);
                console.log('✅ searchMedicineBtn listener added');
            } else {
                console.error('❌ searchMedicineBtn not found');
            }
            
            if (showAllBtn) {
                showAllBtn.addEventListener('click', MedicineHandler.showAll);
                console.log('✅ showAllBtn listener added');
            } else {
                console.error('❌ showAllBtn not found');
            }

            // Quick actions
            const historyBtn = document.getElementById('historyBtn');
            const emergencyBtn = document.getElementById('emergencyBtn');
            const aboutBtn = document.getElementById('aboutBtn');
            
            if (historyBtn) {
                historyBtn.addEventListener('click', (e) => {
                    console.log('🔘 historyBtn clicked!');
                    e.target.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        e.target.style.transform = '';
                    }, 150);
                    HistoryHandler.show();
                });
                console.log('✅ historyBtn listener added');
            } else {
                console.error('❌ historyBtn not found');
            }
            
            if (emergencyBtn) {
                emergencyBtn.addEventListener('click', (e) => {
                    console.log('🔘 emergencyBtn clicked!');
                    e.target.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        e.target.style.transform = '';
                    }, 150);
                    EmergencyHandler.show();
                });
                console.log('✅ emergencyBtn listener added');
            } else {
                console.error('❌ emergencyBtn not found');
            }
            
            if (aboutBtn) {
                aboutBtn.addEventListener('click', (e) => {
                    console.log('🔘 aboutBtn clicked!');
                    e.target.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        e.target.style.transform = '';
                    }, 150);
                    AboutHandler.show();
                });
                console.log('✅ aboutBtn listener added');
            } else {
                console.error('❌ aboutBtn not found');
            }

            // Enter key support for inputs
            const symptomsInput = document.getElementById('symptomsInput');
            const medicineInput = document.getElementById('medicineInput');
            
            if (symptomsInput) {
                symptomsInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        DiagnosisHandler.diagnose();
                    }
                });
                console.log('✅ symptomsInput listener added');
            } else {
                console.error('❌ symptomsInput not found');
            }

            if (medicineInput) {
                medicineInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        MedicineHandler.search();
                    }
                });
                console.log('✅ medicineInput listener added');
            } else {
                console.error('❌ medicineInput not found');
            }

            // Auto-resize textarea
            if (symptomsInput) {
                symptomsInput.addEventListener('input', () => {
                    symptomsInput.style.height = 'auto';
                    symptomsInput.style.height = Math.min(symptomsInput.scrollHeight, 200) + 'px';
                });
            }

            // Symptom tag functionality
            const symptomTags = document.querySelectorAll('.symptom-tag');
            console.log(`Found ${symptomTags.length} symptom tags`);
            
            symptomTags.forEach((tag, index) => {
                tag.addEventListener('click', () => {
                    const symptom = tag.getAttribute('data-symptom');
                    const currentValue = symptomsInput ? symptomsInput.value.trim() : '';
                    
                    if (symptomsInput) {
                        if (currentValue) {
                            // Add comma and space if there's already content
                            symptomsInput.value = currentValue + ', ' + symptom;
                        } else {
                            // Just add the symptom if input is empty
                            symptomsInput.value = symptom;
                        }
                        
                        // Trigger input event to resize textarea
                        symptomsInput.dispatchEvent(new Event('input'));
                    }
                    
                    // Add visual feedback
                    tag.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        tag.style.transform = '';
                    }, 150);
                });
                console.log(`✅ Symptom tag ${index + 1} listener added`);
            });

            // Voice button state management
            if (voiceBtn) {
                voiceBtn.addEventListener('click', () => {
                    if (AppState.isListening) {
                        VoiceService.stop();
                    } else {
                        VoiceService.start();
                    }
                });
            }

            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                // Ctrl+Enter for diagnosis
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    DiagnosisHandler.diagnose();
                }

                // Ctrl+Shift+V for voice input
                if (e.ctrlKey && e.shiftKey && e.key === 'V') {
                    e.preventDefault();
                    VoiceService.start();
                }

                // Escape to close modals
                if (e.key === 'Escape') {
                    EmergencyHandler.close();
                    AboutHandler.close();
                    HistoryHandler.close();
                }
            });

            console.log('✅ All event listeners initialized successfully');

        } catch (error) {
            console.error('❌ Error initializing event listeners:', error);
        }
    }
};

// Application Initialization
const App = {
    init: async () => {
        console.log('🚀 Initializing Medicino Application...');

        try {
            // Initialize voice recognition
            VoiceService.init();

            // Setup event listeners
            EventListeners.init();

            // Initialize flash message auto-dismiss
            App.initFlashMessages();

            // Detect available backend
            await BackendSwitcher.detectAvailableBackend();

            // Show welcome message
           
            // Add loading animations
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease-in';

            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 100);

            console.log('✅ Medicino Application initialized successfully');

        } catch (error) {
            console.error('❌ Error initializing application:', error);
            Utils.showNotification('Application initialization failed. Please refresh the page.', 'error');
        }
    },

    // Initialize flash message functionality
    initFlashMessages: () => {
        const flashMessages = document.querySelectorAll('.flash-message');
        
        flashMessages.forEach(message => {
            // Check if this is a logout notification and remove it instantly
            if (message.textContent.includes('logged out') || message.textContent.includes('You have been logged out')) {
                // Remove logout notification instantly
                App.dismissFlashMessage(message);
                return;
            }

            // Auto-dismiss other messages after 5 seconds
            const autoDismissTimer = setTimeout(() => {
                App.dismissFlashMessage(message);
            }, 5000);

            // Manual dismiss on click
            message.addEventListener('click', () => {
                clearTimeout(autoDismissTimer);
                App.dismissFlashMessage(message);
            });

            // Add close button functionality
            message.addEventListener('mouseenter', () => {
                clearTimeout(autoDismissTimer);
            });
        });
    },

    // Dismiss flash message with animation
    dismissFlashMessage: (message) => {
        message.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 300);
    },

    // Cleanup function
    cleanup: () => {
        // Stop voice recognition if active
        if (AppState.isListening) {
            VoiceService.stop();
        }

        // Clear any timers or intervals
        console.log('🧹 Application cleanup completed');
    }
};

// Performance monitoring
const Performance = {
    startTime: Date.now(),

    measureApiCall: (apiName, startTime) => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        console.log(`📊 API Call [${apiName}]: ${duration}ms`);

        if (duration > 5000) {
            console.warn(`⚠️ Slow API call detected: ${apiName} took ${duration}ms`);
        }
    },

    logMemoryUsage: () => {
        if (performance.memory) {
            const memory = performance.memory;
            console.log('💾 Memory Usage:', {
                used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + ' MB',
                total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + ' MB',
                limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
            });
        }
    }
};

// Error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    Utils.showNotification('An unexpected error occurred. Please try again.', 'error');
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    Utils.showNotification('A network error occurred. Please check your connection.', 'error');
});

// Application lifecycle
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM Content Loaded - Initializing App...');
    App.init();
});

window.addEventListener('load', () => {
    console.log('🌐 Window Loaded - App should be ready...');
    // Fallback initialization if DOMContentLoaded didn't work
    if (!document.getElementById('historyBtn') || !document.getElementById('emergencyBtn') || !document.getElementById('aboutBtn')) {
        console.log('🔄 Re-initializing event listeners...');
        setTimeout(() => {
            EventListeners.init();
        }, 100);
    }
});

window.addEventListener('beforeunload', App.cleanup);

// Periodic performance monitoring (development only)
if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    setInterval(() => {
        Performance.logMemoryUsage();
    }, 30000); // Every 30 seconds
}

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CONFIG,
        AppState,
        Utils,
        ApiService,
        VoiceService,
        DiagnosisHandler,
        MedicineHandler,
        HistoryHandler,
        EmergencyHandler,
        AboutHandler
    };
}

console.log('📋 Medicino JavaScript loaded successfully');
