const { ipcRenderer } = require('electron');
const axios = require('axios');

// Global state
let flightData = null;
let map = null;
let flightPath = null;
let aircraftMarker = null;
let animationFrameId = null;
let currentPointIndex = 0;
let isPlaying = false;
let animationSpeed = 1;
let charts = {
    altitude: null,
    speed: null,
    distance: null
};

// Airplane icon as base64 - placeholder (user will replace)
const AIRPLANE_ICON = './assets/orangePlane.png';

// Backend URL
let BACKEND_URL = 'http://127.0.0.1:8000';

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    BACKEND_URL = await ipcRenderer.invoke('get-backend-url');
    initializeMap();
    setupEventListeners();
    checkBackendHealth();
});

// Check if backend is ready
async function checkBackendHealth() {
    let attempts = 0;
    const maxAttempts = 10;
    
    const check = async () => {
        try {
            const response = await axios.get(`${BACKEND_URL}/health`, { timeout: 2000 });
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

// Initialize Leaflet map
function initializeMap() {
    map = L.map('map').setView([42.187, -71.176], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        map.invalidateSize();
    });
}

// Setup event listeners
function setupEventListeners() {
    // File selection
    document.getElementById('browseBtn').addEventListener('click', async () => {
        const filePath = await ipcRenderer.invoke('select-csv-file');
        if (filePath) {
            document.getElementById('fileName').textContent = filePath.split(/[\\/]/).pop();
            document.getElementById('processBtn').disabled = false;
            
            // Store file path for processing
            window.selectedFilePath = filePath;
        }
    });
    
    // Also support direct file input
    document.getElementById('csvFileInput').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('processBtn').disabled = false;
            window.selectedFile = file;
        }
    });
    
    // Process button
    document.getElementById('processBtn').addEventListener('click', processFlightData);
    
    // Animation controls
    document.getElementById('playPauseBtn').addEventListener('click', togglePlayPause);
    document.getElementById('resetBtn').addEventListener('click', resetAnimation);
    document.getElementById('progressSlider').addEventListener('input', onProgressChange);
    document.getElementById('speedSelect').addEventListener('change', onSpeedChange);
    
    // Save buttons
    document.getElementById('saveMapBtn').addEventListener('click', saveMapImage);
    document.getElementById('saveAltBtn').addEventListener('click', () => saveChartImage('altitude'));
    document.getElementById('saveSpeedBtn').addEventListener('click', () => saveChartImage('speed'));
    document.getElementById('saveDistanceBtn').addEventListener('click', () => saveChartImage('distance'));
    
    // Distance modal
    document.getElementById('showDistanceBtn').addEventListener('click', showDistanceChart);
    document.getElementById('closeDistanceBtn').addEventListener('click', closeDistanceModal);
}

// Process flight data
async function processFlightData() {
    try {
        showLoading(true);
        document.getElementById('processBtn').disabled = true;
        
        let formData = new FormData();
        
        // Use file from either source
        if (window.selectedFile) {
            formData.append('file', window.selectedFile);
        } else if (window.selectedFilePath) {
            // Read file from path
            const fs = require('fs');
            const fileBuffer = fs.readFileSync(window.selectedFilePath);
            const blob = new Blob([fileBuffer], { type: 'text/csv' });
            formData.append('file', blob, window.selectedFilePath.split(/[\\/]/).pop());
        }
        
        const response = await axios.post(
            `${BACKEND_URL}/api/analyze-flight`,
            formData,
            {
                headers: { 'Content-Type': 'multipart/form-data' },
                timeout: 30000
            }
        );
        
        if (response.data.success) {
            flightData = response.data.data;
            initializeFlightVisualization();
            enableControls();
            showFlightInfo();
            document.getElementById('processBtn').disabled = true;
        }
        
    } catch (error) {
        console.error('Error processing flight data:', error);
        alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
        showLoading(false);
        document.getElementById('processBtn').disabled = false;
    }
}

// Initialize flight visualization
function initializeFlightVisualization() {
    // Clear previous data
    if (flightPath) map.removeLayer(flightPath);
    if (aircraftMarker) map.removeLayer(aircraftMarker);
    
    // Create flight path
    const coordinates = flightData.flightPoints.map(point => [point.latitude, point.longitude]);
    
    flightPath = L.polyline(coordinates, {
        color: '#3498db',
        weight: 3,
        opacity: 0.7
    }).addTo(map);
    
    // Fit map to path
    map.fitBounds(flightPath.getBounds(), { padding: [50, 50] });
    
    // Create aircraft marker with custom icon
    const airplaneIcon = L.divIcon({
        html: `<img src="${AIRPLANE_ICON}" style="width: 32px; height: 32px; transform: rotate(0deg); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">`,
        className: 'airplane-marker',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });
    
    const firstPoint = flightData.flightPoints[0];
    aircraftMarker = L.marker([firstPoint.latitude, firstPoint.longitude], {
        icon: airplaneIcon,
        rotationAngle: 0,
        rotationOrigin: 'center'
    }).addTo(map);
    
    // Initialize charts
    createCharts();
    
    // Reset animation state
    currentPointIndex = 0;
    updateProgress();
}

// Create charts
function createCharts() {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff'
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#b0b0b0' },
                title: {
                    display: true,
                    text: 'Time (seconds)',
                    color: '#b0b0b0'
                }
            },
            y: {
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#b0b0b0' }
            }
        }
    };
    
    // Altitude chart
    const altCtx = document.getElementById('altitudeChart').getContext('2d');
    if (charts.altitude) charts.altitude.destroy();
    charts.altitude = new Chart(altCtx, {
        type: 'line',
        data: {
            labels: flightData.plots.altitude.x,
            datasets: [{
                label: 'Altitude (ft)',
                data: flightData.plots.altitude.y,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    title: {
                        display: true,
                        text: 'Altitude (ft)',
                        color: '#b0b0b0'
                    }
                }
            }
        }
    });
    
    // Speed chart
    const speedCtx = document.getElementById('speedChart').getContext('2d');
    if (charts.speed) charts.speed.destroy();
    charts.speed = new Chart(speedCtx, {
        type: 'line',
        data: {
            labels: flightData.plots.speed.x,
            datasets: [{
                label: 'Speed (kts)',
                data: flightData.plots.speed.y,
                borderColor: '#27ae60',
                backgroundColor: 'rgba(39, 174, 96, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    title: {
                        display: true,
                        text: 'Speed (kts)',
                        color: '#b0b0b0'
                    }
                }
            }
        }
    });
}

// Show distance chart in modal
function showDistanceChart() {
    const modal = document.getElementById('distanceModal');
    modal.classList.add('show');
    
    if (!charts.distance) {
        const distCtx = document.getElementById('distanceChart').getContext('2d');
        charts.distance = new Chart(distCtx, {
            type: 'line',
            data: {
                labels: flightData.plots.distance.x,
                datasets: [{
                    label: 'Distance from Start (m)',
                    data: flightData.plots.distance.y,
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b0b0b0' },
                        title: {
                            display: true,
                            text: 'Time (seconds)',
                            color: '#b0b0b0'
                        }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b0b0b0' },
                        title: {
                            display: true,
                            text: 'Distance from Start (m)',
                            color: '#b0b0b0'
                        }
                    }
                }
            }
        });
    }
}

function closeDistanceModal() {
    document.getElementById('distanceModal').classList.remove('show');
}

// Animation controls
function togglePlayPause() {
    isPlaying = !isPlaying;
    const icon = document.getElementById('playPauseIcon');
    
    if (isPlaying) {
        icon.textContent = '⏸️';
        startAnimation();
    } else {
        icon.textContent = '▶️';
        stopAnimation();
    }
}

function startAnimation() {
    const animate = () => {
        if (!isPlaying || !flightData) return;
        
        currentPointIndex += animationSpeed;
        
        if (currentPointIndex >= flightData.flightPoints.length) {
            currentPointIndex = flightData.flightPoints.length - 1;
            isPlaying = false;
            document.getElementById('playPauseIcon').textContent = '▶️';
            return;
        }
        
        updateAircraftPosition();
        updateProgress();
        
        animationFrameId = requestAnimationFrame(animate);
    };
    
    animate();
}

function stopAnimation() {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
}

function resetAnimation() {
    stopAnimation();
    isPlaying = false;
    currentPointIndex = 0;
    document.getElementById('playPauseIcon').textContent = '▶️';
    updateAircraftPosition();
    updateProgress();
}

function onProgressChange(e) {
    const progress = parseFloat(e.target.value);
    currentPointIndex = Math.floor((progress / 100) * (flightData.flightPoints.length - 1));
    updateAircraftPosition();
    updateProgress();
}

function onSpeedChange(e) {
    animationSpeed = parseFloat(e.target.value);
}

function updateAircraftPosition() {
    if (!flightData || !aircraftMarker) return;
    
    const index = Math.floor(currentPointIndex);
    const point = flightData.flightPoints[index];
    
    if (!point) return;
    
    // Update marker position
    aircraftMarker.setLatLng([point.latitude, point.longitude]);
    
    // Update rotation
    const airplaneIcon = L.divIcon({
        html: `<img src="${AIRPLANE_ICON}" style="width: 32px; height: 32px; transform: rotate(${point.heading}deg); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">`,
        className: 'airplane-marker',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });
    aircraftMarker.setIcon(airplaneIcon);
    
    // Create progress path (partial path from start to current position)
    if (flightPath) {
        map.removeLayer(flightPath);
    }
    
    const fullPath = flightData.flightPoints.map(p => [p.latitude, p.longitude]);
    const progressPath = fullPath.slice(0, index + 1);
    
    // Draw completed path in different color
    flightPath = L.polyline(fullPath, {
        color: '#34495e',
        weight: 3,
        opacity: 0.3
    }).addTo(map);
    
    // Draw traveled path
    if (progressPath.length > 1) {
        L.polyline(progressPath, {
            color: '#3498db',
            weight: 4,
            opacity: 0.9
        }).addTo(map);
    }
}

function updateProgress() {
    if (!flightData) return;
    
    const progress = (currentPointIndex / (flightData.flightPoints.length - 1)) * 100;
    document.getElementById('progressSlider').value = progress;
    document.getElementById('progressLabel').textContent = `${Math.round(progress)}%`;
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('mapLoading');
    if (show) {
        overlay.classList.add('show');
    } else {
        overlay.classList.remove('show');
    }
}

// Enable controls after data is loaded
function enableControls() {
    document.getElementById('playPauseBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    document.getElementById('progressSlider').disabled = false;
    document.getElementById('speedSelect').disabled = false;
    document.getElementById('saveMapBtn').disabled = false;
    document.getElementById('saveAltBtn').disabled = false;
    document.getElementById('saveSpeedBtn').disabled = false;
    document.getElementById('showDistanceBtn').disabled = false;
}

// Show flight information
function showFlightInfo() {
    if (!flightData) return;
    
    const stats = flightData.statistics;
    
    document.getElementById('infoCallsign').textContent = stats.callsign;
    document.getElementById('infoMaxAlt').textContent = `${stats.maxAltitude} ft`;
    document.getElementById('infoMaxSpeed').textContent = `${stats.maxSpeed} kts`;
    document.getElementById('infoDistance').textContent = `${(stats.totalDistance / 1000).toFixed(2)} km`;
    document.getElementById('infoDuration').textContent = formatDuration(stats.duration);
    document.getElementById('infoPoints').textContent = stats.totalPoints;
    
    document.getElementById('flightInfo').style.display = 'block';
}

function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}m ${secs}s`;
}

// Save map as image
async function saveMapImage() {
    try {
        const mapElement = document.getElementById('map');
        
        // Show loading indicator
        const saveBtn = document.getElementById('saveMapBtn');
        const originalText = saveBtn.innerHTML;
        saveBtn.innerHTML = '<span>⏳</span> Capturing...';
        saveBtn.disabled = true;
        
        // Use html2canvas to capture the map
        const canvas = await html2canvas(mapElement, {
            useCORS: true,
            allowTaint: true,
            backgroundColor: '#2c2c2c',
            scale: 2, // Higher quality
            logging: false
        });
        
        // Convert to data URL
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
        } else {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        }
        
    } catch (error) {
        console.error('Error saving map:', error);
        const saveBtn = document.getElementById('saveMapBtn');
        saveBtn.innerHTML = '<span>❌</span> Error';
        setTimeout(() => {
            saveBtn.innerHTML = '<span>💾</span> Save Map';
            saveBtn.disabled = false;
        }, 2000);
    }
}

// Save chart as image
async function saveChartImage(chartType) {
    try {
        const chart = charts[chartType];
        if (!chart) {
            console.error('Chart not found:', chartType);
            return;
        }
        
        const dataUrl = chart.toBase64Image();
        const fileName = `flight_${chartType}_${Date.now()}.png`;
        
        const result = await ipcRenderer.invoke('save-image', dataUrl, fileName);
        
        if (result && result.success) {
            // Show success message briefly
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
        // Don't show alert, just log the error
    }
}

// Utility functions
function formatNumber(num, decimals = 2) {
    return num.toFixed(decimals);
}

// Handle window close
window.addEventListener('beforeunload', () => {
    stopAnimation();
    if (charts.altitude) charts.altitude.destroy();
    if (charts.speed) charts.speed.destroy();
    if (charts.distance) charts.distance.destroy();
});
