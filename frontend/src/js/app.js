/**
 * Main Application Module
 * Coordinates all components and handles user interactions
 */

const { ipcRenderer } = require('electron');
const axios = require('axios');

class FlightTrackApp {
    constructor() {
        this.mapManager = new MapManager();
        this.chartManager = new ChartManager();
        this.animationController = null;
        this.airplaneIconPath = null;
        
        this.flightData = null;
        this.backendUrl = 'http://127.0.0.1:8000';
        
        this.initialize();
    }
    

    /**
     * Initialize the application
     */
    async initialize() {
        // Get backend URL
        this.backendUrl = await ipcRenderer.invoke('get-backend-url');

        // Get airplane icon path
        this.airplaneIconPath = await ipcRenderer.invoke('get-airplane-icon-path');
        console.log('Airplane icon path:', this.airplaneIconPath);
        this.mapManager.setAirplaneIconPath(this.airplaneIconPath);
        
        // Initialize map
        this.mapManager.initialize();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Check backend health
        await this.checkBackendHealth();
    }

    /**
     * Check if backend is ready
     */
    async checkBackendHealth() {
        let attempts = 0;
        const maxAttempts = 10;
        
        const check = async () => {
            try {
                const response = await axios.get(`${this.backendUrl}/health`, { timeout: 2000 });
                if (response.data.status === 'healthy') {
                    console.log('Backend is ready');
                    return true;
                }
            } catch (error) {
                attempts++;
                if (attempts < maxAttempts) {
                    console.log(`Backend not ready, retrying... (${attempts}/${maxAttempts})`);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    return check();
                } else {
                    alert('Failed to connect to backend server. Please restart the application.');
                    return false;
                }
            }
        };
        
        await check();
    }

    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // File selection
        document.getElementById('browseBtn').addEventListener('click', () => this.browseFile());
        document.getElementById('processBtn').addEventListener('click', () => this.processFile());
        
        // Animation controls
        document.getElementById('playPauseBtn').addEventListener('click', () => this.togglePlayPause());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetAnimation());
        document.getElementById('progressSlider').addEventListener('input', (e) => this.onProgressChange(e));
        document.getElementById('speedSelect').addEventListener('change', (e) => this.onSpeedChange(e));
        
        // Save buttons
        document.getElementById('saveMapBtn').addEventListener('click', () => this.saveMapImage());
        document.getElementById('saveAltBtn').addEventListener('click', () => this.saveChartImage('altitude'));
        document.getElementById('saveSpeedBtn').addEventListener('click', () => this.saveChartImage('speed'));
        document.getElementById('saveDistanceBtn').addEventListener('click', () => this.saveChartImage('distance'));
        
        // Distance modal
        document.getElementById('showDistanceBtn').addEventListener('click', () => this.showDistanceChart());
        document.getElementById('closeDistanceBtn').addEventListener('click', () => this.closeDistanceModal());
    }

    /**
     * Browse for CSV file
     */
    async browseFile() {
        const filePath = await ipcRenderer.invoke('select-csv-file');
        if (filePath) {
            document.getElementById('fileName').textContent = filePath.split(/[\\/]/).pop();
            document.getElementById('processBtn').disabled = false;
            window.selectedFilePath = filePath;
        }
    }

    /**
     * Process selected CSV file
     */
    async processFile() {
        try {
            this.showLoading(true);
            document.getElementById('processBtn').disabled = true;
            
            let formData = new FormData();
            
            if (window.selectedFilePath) {
                const fs = require('fs');
                const fileBuffer = fs.readFileSync(window.selectedFilePath);
                const blob = new Blob([fileBuffer], { type: 'text/csv' });
                formData.append('file', blob, window.selectedFilePath.split(/[\\/]/).pop());
            }
            
            const response = await axios.post(
                `${this.backendUrl}/api/analyze-flight`,
                formData,
                {
                    headers: { 'Content-Type': 'multipart/form-data' },
                    timeout: 30000
                }
            );
            
            if (response.data.success) {
                this.flightData = response.data.data;
                this.initializeVisualization();
                this.enableControls();
                this.showFlightInfo();
            }
            
        } catch (error) {
            console.error('Error processing flight data:', error);
            alert(`Error: ${error.response?.data?.detail || error.message}`);
            document.getElementById('processBtn').disabled = false;
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Initialize visualization with flight data
     */
    initializeVisualization() {
        // Clear previous data
        this.mapManager.clear();
        
        // Create flight path
        const coordinates = this.flightData.flightPoints.map(point => [point.latitude, point.longitude]);
        this.mapManager.createFlightPath(coordinates);
        
        // Create aircraft marker
        const firstPoint = this.flightData.flightPoints[0];
        this.mapManager.createAircraftMarker(
            firstPoint.latitude,
            firstPoint.longitude,
            firstPoint.heading
        );
        
        // Create charts
        this.chartManager.createAltitudeChart(
            this.flightData.plots.altitude.x,
            this.flightData.plots.altitude.y
        );
        this.chartManager.createSpeedChart(
            this.flightData.plots.speed.x,
            this.flightData.plots.speed.y
        );
        
        // Initialize animation controller
        this.animationController = new AnimationController(
            this.mapManager,
            (state) => this.onAnimationUpdate(state)
        );
        this.animationController.setFlightData(this.flightData);
    }

    /**
     * Animation update callback
     */
    onAnimationUpdate(state) {
        document.getElementById('progressSlider').value = state.progress;
        document.getElementById('progressLabel').textContent = `${Math.round(state.progress)}%`;
        
        const icon = document.getElementById('playPauseIcon');
        icon.textContent = state.isPlaying ? '⏸️' : '▶️';
    }

    /**
     * Toggle play/pause
     */
    togglePlayPause() {
        if (!this.animationController) return;
        
        const state = this.animationController.getState();
        if (state.isPlaying) {
            this.animationController.pause();
        } else {
            this.animationController.play();
        }
    }

    /**
     * Reset animation
     */
    resetAnimation() {
        if (!this.animationController) return;
        this.animationController.reset();
        this.onAnimationUpdate(this.animationController.getState());
    }

    /**
     * Handle progress slider change
     */
    onProgressChange(e) {
        if (!this.animationController) return;
        const progress = parseFloat(e.target.value);
        this.animationController.seek(progress);
        this.onAnimationUpdate(this.animationController.getState());
    }

    /**
     * Handle speed change
     */
    onSpeedChange(e) {
        if (!this.animationController) return;
        const speed = parseFloat(e.target.value);
        this.animationController.setSpeed(speed);
    }

    /**
     * Show/hide loading overlay
     */
    showLoading(show) {
        const overlay = document.getElementById('mapLoading');
        if (show) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }

    /**
     * Enable controls after data is loaded
     */
    enableControls() {
        document.getElementById('playPauseBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;
        document.getElementById('progressSlider').disabled = false;
        document.getElementById('speedSelect').disabled = false;
        document.getElementById('saveMapBtn').disabled = false;
        document.getElementById('saveAltBtn').disabled = false;
        document.getElementById('saveSpeedBtn').disabled = false;
        document.getElementById('showDistanceBtn').disabled = false;
    }

    /**
     * Show flight information
     */
    showFlightInfo() {
        if (!this.flightData) return;
        
        const stats = this.flightData.statistics;
        
        document.getElementById('infoCallsign').textContent = stats.callsign;
        document.getElementById('infoMaxAlt').textContent = `${stats.maxAltitude} ft`;
        document.getElementById('infoMaxSpeed').textContent = `${stats.maxSpeed} kts`;
        document.getElementById('infoDistance').textContent = `${(stats.totalDistance / 1000).toFixed(2)} km`;
        document.getElementById('infoDuration').textContent = this.formatDuration(stats.duration);
        document.getElementById('infoPoints').textContent = stats.totalPoints;
        
        document.getElementById('flightInfo').style.display = 'block';
    }

    /**
     * Format duration in seconds to readable string
     */
    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}m ${secs}s`;
    }

    /**
     * Show distance chart modal
     */
    showDistanceChart() {
        const modal = document.getElementById('distanceModal');
        modal.classList.add('show');
        
        if (!this.chartManager.getChart('distance')) {
            this.chartManager.createDistanceChart(
                this.flightData.plots.distance.x,
                this.flightData.plots.distance.y
            );
        }
    }

    /**
     * Close distance modal
     */
    closeDistanceModal() {
        document.getElementById('distanceModal').classList.remove('show');
    }

    /**
     * Save map as image
     */
    async saveMapImage() {
        try {
            const mapElement = document.getElementById('map');
            const saveBtn = document.getElementById('saveMapBtn');
            const originalText = saveBtn.innerHTML;
            
            saveBtn.innerHTML = '<span>⏳</span> Capturing...';
            saveBtn.disabled = true;
            
            const canvas = await html2canvas(mapElement, {
                useCORS: true,
                allowTaint: true,
                backgroundColor: '#2c2c2c',
                scale: 2,
                logging: false
            });
            
            const dataUrl = canvas.toDataURL('image/png');
            const fileName = `flight_map_${Date.now()}.png`;
            
            const result = await ipcRenderer.invoke('save-image', dataUrl, fileName);
            
            if (result && result.success) {
                saveBtn.innerHTML = '<span>✓</span> Saved!';
                saveBtn.style.background = 'linear-gradient(135deg, #27ae60, #229954)';
                setTimeout(() => {
                    saveBtn.innerHTML = originalText;
                    saveBtn.style.background = '';
                    saveBtn.disabled = false;
                }, 2000);
            }
        } catch (error) {
            console.error('Error saving map:', error);
        }
    }

    /**
     * Save chart as image
     */
    async saveChartImage(chartType) {
        try {
            const chart = this.chartManager.getChart(chartType);
            if (!chart) return;
            
            const dataUrl = chart.toBase64Image();
            const fileName = `flight_${chartType}_${Date.now()}.png`;
            
            const result = await ipcRenderer.invoke('save-image', dataUrl, fileName);
            
            if (result && result.success) {
                const btnId = chartType === 'altitude' ? 'saveAltBtn' : 
                             chartType === 'speed' ? 'saveSpeedBtn' : 
                             'saveDistanceBtn';
                const btn = document.getElementById(btnId);
                
                if (btn) {
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '<span>✓</span> Saved!';
                    btn.style.background = 'linear-gradient(135deg, #27ae60, #229954)';
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.style.background = '';
                    }, 2000);
                }
            }
        } catch (error) {
            console.error('Error saving chart:', error);
        }
    }

    /**
     * Cleanup
     */
    destroy() {
        if (this.animationController) {
            this.animationController.destroy();
        }
        this.chartManager.destroyAll();
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.flightTrackApp = new FlightTrackApp();
});

// Cleanup on window close
window.addEventListener('beforeunload', () => {
    if (window.flightTrackApp) {
        window.flightTrackApp.destroy();
    }
});