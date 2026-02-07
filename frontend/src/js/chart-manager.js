/**
 * Chart Manager Module
 * Handles Chart.js chart creation and management
 */

class ChartManager {
    constructor() {
        this.charts = {
            altitude: null,
            speed: null,
            distance: null
        };
        
        this.commonOptions = {
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
    }

    /**
     * Create altitude chart
     * @param {Array} xData - Time data
     * @param {Array} yData - Altitude data
     */
    createAltitudeChart(xData, yData) {
        const ctx = document.getElementById('altitudeChart').getContext('2d');
        
        if (this.charts.altitude) {
            this.charts.altitude.destroy();
        }
        
        this.charts.altitude = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xData,
                datasets: [{
                    label: 'Altitude (ft)',
                    data: yData,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                ...this.commonOptions,
                scales: {
                    ...this.commonOptions.scales,
                    y: {
                        ...this.commonOptions.scales.y,
                        title: {
                            display: true,
                            text: 'Altitude (ft)',
                            color: '#b0b0b0'
                        }
                    }
                }
            }
        });
    }

    /**
     * Create speed chart
     * @param {Array} xData - Time data
     * @param {Array} yData - Speed data
     */
    createSpeedChart(xData, yData) {
        const ctx = document.getElementById('speedChart').getContext('2d');
        
        if (this.charts.speed) {
            this.charts.speed.destroy();
        }
        
        this.charts.speed = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xData,
                datasets: [{
                    label: 'Speed (kts)',
                    data: yData,
                    borderColor: '#27ae60',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                ...this.commonOptions,
                scales: {
                    ...this.commonOptions.scales,
                    y: {
                        ...this.commonOptions.scales.y,
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

    /**
     * Create distance chart
     * @param {Array} xData - Time data
     * @param {Array} yData - Distance data
     */
    createDistanceChart(xData, yData) {
        const ctx = document.getElementById('distanceChart').getContext('2d');
        
        if (this.charts.distance) {
            this.charts.distance.destroy();
        }
        
        this.charts.distance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xData,
                datasets: [{
                    label: 'Distance from Start (m)',
                    data: yData,
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                ...this.commonOptions,
                scales: {
                    ...this.commonOptions.scales,
                    y: {
                        ...this.commonOptions.scales.y,
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

    /**
     * Get chart instance
     * @param {string} type - Chart type ('altitude', 'speed', or 'distance')
     * @returns {Chart} Chart.js instance
     */
    getChart(type) {
        return this.charts[type];
    }

    /**
     * Destroy all charts
     */
    destroyAll() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {
            altitude: null,
            speed: null,
            distance: null
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartManager };
}