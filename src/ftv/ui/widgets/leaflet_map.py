# import json
# from PyQt6.QtWebEngineWidgets import QWebEngineView

# class LeafletMapCanvas(QWebEngineView):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.flight_data = None
#         self.current_frame = 0
        
#         # CHANGED: Added dark background to body
#         self.html_template = """
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
#             <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
#             <style> 
#                 body, html, #map { margin: 0; padding: 0; height: 100%; width: 100%; background-color: #222; } 
#             </style>
#         </head>
#         <body>
#             <div id="map"></div>
#             <script>
#                 // Initialize Map with a slightly darker background setting
#                 var map = L.map('map', {zoomControl: false}).setView([0, 0], 2);
                
#                 // --- CHANGED: Use CartoDB Dark Matter Tiles ---
#                 L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
#                     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
#                     subdomains: 'abcd',
#                     maxZoom: 20
#                 }).addTo(map);

#                 // --- CHANGED: Neon Cyan Path & Yellow Plane ---
#                 var flightPath = L.polyline([], {
#                     color: '#00ffff',  // Cyan (Radar look)
#                     weight: 2,
#                     opacity: 0.8
#                 }).addTo(map);
                
#                 var planeMarker = L.circleMarker([0, 0], {
#                     color: '#ffffff',      // White border
#                     fillColor: '#ffcc00',  // Yellow fill
#                     fillOpacity: 1.0,
#                     weight: 2,
#                     radius: 6
#                 }).addTo(map);

#                 function loadPath(latlngs) {
#                     flightPath.setLatLngs(latlngs);
#                     if (latlngs.length > 0) { map.fitBounds(flightPath.getBounds(), {padding: [50, 50]}); }
#                 }

#                 function updatePosition(lat, lon) {
#                     var newLatLng = [lat, lon];
#                     planeMarker.setLatLng(newLatLng);
#                 }
#             </script>
#         </body>
#         </html>
#         """
#         self.setHtml(self.html_template)
        
#     def load_flight_data(self, lats, lons):
#         self.flight_data = {'lat': lats, 'lon': lons}
#         self.current_frame = 0
        
#         # Downsample for JS performance (every ~5000th point for path, or max 1000 points)
#         step = max(1, len(lats) // 2000) 
#         path_points = [[float(lats[i]), float(lons[i])] for i in range(0, len(lats), step)]
        
#         self.page().runJavaScript(f"loadPath({json.dumps(path_points)});")

#     def update_marker(self, idx):
#         if not self.flight_data: return
#         lats, lons = self.flight_data['lat'], self.flight_data['lon']
#         if idx >= len(lats): idx = len(lats) - 1
        
#         lat, lon = float(lats[idx]), float(lons[idx])
#         self.page().runJavaScript(f"updatePosition({lat}, {lon});")

import json
from PyQt6.QtWebEngineWidgets import QWebEngineView

class LeafletMapCanvas(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flight_data = None
        self.current_frame = 0
        
        # Standard Light Map Template
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style> 
                body, html, #map { margin: 0; padding: 0; height: 100%; width: 100%; } 
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // Initialize Map
                var map = L.map('map').setView([0, 0], 2);
                
                // Use Standard OpenStreetMap Tiles (Light/Colorful)
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }).addTo(map);

                // Blue Flight Path (Standard)
                var flightPath = L.polyline([], {
                    color: 'blue', 
                    weight: 3
                }).addTo(map);
                
                // Red/Red-Orange Marker
                var planeMarker = L.circleMarker([0, 0], {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.9,
                    radius: 5
                }).addTo(map);

                function loadPath(latlngs) {
                    flightPath.setLatLngs(latlngs);
                    if (latlngs.length > 0) { map.fitBounds(flightPath.getBounds()); }
                }

                function updatePosition(lat, lon) {
                    var newLatLng = [lat, lon];
                    planeMarker.setLatLng(newLatLng);
                }
            </script>
        </body>
        </html>
        """
        self.setHtml(self.html_template)
        
    def load_flight_data(self, lats, lons):
        self.flight_data = {'lat': lats, 'lon': lons}
        self.current_frame = 0
        
        step = max(1, len(lats) // 2000) 
        path_points = [[float(lats[i]), float(lons[i])] for i in range(0, len(lats), step)]
        
        self.page().runJavaScript(f"loadPath({json.dumps(path_points)});")

    def update_marker(self, idx):
        if not self.flight_data: return
        lats, lons = self.flight_data['lat'], self.flight_data['lon']
        if idx >= len(lats): idx = len(lats) - 1
        
        lat, lon = float(lats[idx]), float(lons[idx])
        self.page().runJavaScript(f"updatePosition({lat}, {lon});")