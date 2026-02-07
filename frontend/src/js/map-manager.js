/**
 * Map Module
 * Handles Leaflet map initialization, flight path rendering, and aircraft marker
 */

class MapManager {
    constructor() {
        this.map = null;
        this.flightPath = null;
        this.aircraftMarker = null;
        this.progressPath = null;
        this.airplaneIconPath = null;
    }

    /**
     * Initialize Leaflet map
     */
    initialize() {
        this.map = L.map('map').setView([42.187, -71.176], 13);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.map.invalidateSize();
        });
    }

    setAirplaneIconPath(p) {
        this.airplaneIconPath = p;
    }

    /**
     * Create flight path polyline
     * @param {Array} coordinates - Array of [lat, lon] coordinates
     */
    createFlightPath(coordinates) {
        // Remove previous path if exists
        if (this.flightPath) {
            this.map.removeLayer(this.flightPath);
        }
        
        this.flightPath = L.polyline(coordinates, {
            color: '#3498db',
            weight: 3,
            opacity: 0.7
        }).addTo(this.map);
        
        // Fit map to path
        this.map.fitBounds(this.flightPath.getBounds(), { padding: [50, 50] });
    }

    toFileUrl(p) {
        // Convert Windows backslashes to forward slashes and encode spaces etc.
        const normalized = p.replace(/\\/g, '/');
        return encodeURI('file:///' + normalized);
    }

    /**
     * Create aircraft marker with rotation
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     * @param {number} heading - Aircraft heading in degrees
     */
    createAircraftMarker(lat, lon, heading) {
        const src = this.airplaneIconPath ? this.toFileUrl(this.airplaneIconPath) : '';

        console.log('Airplane icon URL:', this.toFileUrl(this.airplaneIconPath));

        const airplaneIcon = L.divIcon({
            html: `<img
            src="${src}"
            style="width: 32px; height: 32px; transform: rotate(${heading}deg); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));"
            >`,
            className: 'airplane-marker',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        this.aircraftMarker = L.marker([lat, lon], { icon: airplaneIcon }).addTo(this.map);
    }


    /**
     * Update aircraft position and rotation
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     * @param {number} heading - Aircraft heading in degrees
     */
    updateAircraftPosition(lat, lon, heading) {
        if (!this.aircraftMarker) return;

        this.aircraftMarker.setLatLng([lat, lon]);

        const src = this.airplaneIconPath ? this.toFileUrl(this.airplaneIconPath) : '';

        const airplaneIcon = L.divIcon({
            html: `<img
            src="${src}"
            style="width: 32px; height: 32px; transform: rotate(${heading}deg); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));"
            >`,
            className: 'airplane-marker',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        this.aircraftMarker.setIcon(airplaneIcon);
    }


    /**
     * Update progress path (show traveled portion)
     * @param {Array} fullPath - Complete flight path coordinates
     * @param {number} currentIndex - Current position index
     */
    updateProgressPath(fullPath, currentIndex) {
        // Remove old paths
        if (this.flightPath) {
            this.map.removeLayer(this.flightPath);
        }
        if (this.progressPath) {
            this.map.removeLayer(this.progressPath);
        }
        
        // Draw full path in gray
        this.flightPath = L.polyline(fullPath, {
            color: '#34495e',
            weight: 3,
            opacity: 0.3
        }).addTo(this.map);
        
        // Draw traveled portion in blue
        const traveledPath = fullPath.slice(0, currentIndex + 1);
        if (traveledPath.length > 1) {
            this.progressPath = L.polyline(traveledPath, {
                color: '#3498db',
                weight: 4,
                opacity: 0.9
            }).addTo(this.map);
        }
    }

    /**
     * Clear all map layers
     */
    clear() {
        if (this.flightPath) {
            this.map.removeLayer(this.flightPath);
            this.flightPath = null;
        }
        if (this.aircraftMarker) {
            this.map.removeLayer(this.aircraftMarker);
            this.aircraftMarker = null;
        }
        if (this.progressPath) {
            this.map.removeLayer(this.progressPath);
            this.progressPath = null;
        }
    }

    /**
     * Get map instance
     * @returns {L.Map} Leaflet map instance
     */
    getMap() {
        return this.map;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MapManager };
}