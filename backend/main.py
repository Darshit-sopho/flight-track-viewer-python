"""
Flight Track Analyzer Backend
FastAPI server for processing flight trajectory data
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from io import StringIO
from typing import List, Dict, Any
import math
from datetime import datetime

app = FastAPI(title="Flight Track Analyzer API")

# Enable CORS for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_heading(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate bearing/heading between two GPS coordinates
    Returns heading in degrees (0-360)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon_diff = math.radians(lon2 - lon1)
    
    x = math.sin(lon_diff) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon_diff))
    
    heading = math.atan2(x, y)
    heading = math.degrees(heading)
    heading = (heading + 360) % 360
    
    return heading

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula
    Returns distance in meters
    """
    R = 6371000  # Earth's radius in meters
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return distance

def parse_position(position_str: str) -> tuple:
    """Parse position string 'lat,lon' into tuple (lat, lon)"""
    try:
        # Remove any quotes that might be around the position
        position_str = str(position_str).strip().strip('"').strip("'")
        lat, lon = position_str.split(',')
        return float(lat), float(lon)
    except:
        return None, None

@app.get("/")
async def root():
    return {"message": "Flight Track Analyzer API", "status": "running"}

@app.post("/api/analyze-flight")
async def analyze_flight(file: UploadFile = File(...)):
    """
    Analyze flight trajectory from CSV file
    Returns processed flight data with calculated metrics
    """
    try:
        # Read CSV file
        contents = await file.read()
        csv_string = contents.decode('utf-8')
        
        # Try to detect delimiter (tab or comma)
        first_line = csv_string.split('\n')[0]
        delimiter = '\t' if '\t' in first_line else ','
        
        df = pd.read_csv(StringIO(csv_string), sep=delimiter)
        
        # Validate required columns
        required_columns = ['Timestamp', 'UTC', 'Callsign', 'Position', 'Altitude', 'Speed', 'Direction']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail="Invalid CSV format. Missing required columns.")
        
        # Parse positions
        positions = df['Position'].apply(parse_position)
        df['Latitude'] = [pos[0] for pos in positions]
        df['Longitude'] = [pos[1] for pos in positions]
        
        # Remove rows with invalid positions
        df = df.dropna(subset=['Latitude', 'Longitude'])
        df = df.sort_values("Timestamp").reset_index(drop=True)
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="No valid position data found in CSV")
        
        # Calculate headings between consecutive points
        headings = []
        for i in range(len(df)):
            if i == 0:
                # Use provided direction for first point
                headings.append(float(df.iloc[i]['Direction']))
            else:
                prev_lat = df.iloc[i-1]['Latitude']
                prev_lon = df.iloc[i-1]['Longitude']
                curr_lat = df.iloc[i]['Latitude']
                curr_lon = df.iloc[i]['Longitude']
                heading = calculate_heading(prev_lat, prev_lon, curr_lat, curr_lon)
                headings.append(heading)
        
        df['Heading'] = headings
        
        # Calculate cumulative distance from starting point
        start_lat = df.iloc[0]['Latitude']
        start_lon = df.iloc[0]['Longitude']
        
        distances = []
        for i in range(len(df)):
            curr_lat = df.iloc[i]['Latitude']
            curr_lon = df.iloc[i]['Longitude']
            distance = calculate_distance(start_lat, start_lon, curr_lat, curr_lon)
            distances.append(distance)
        
        df['DistanceFromStart'] = distances
        
        # Calculate time differences
        df['Timestamp'] = pd.to_numeric(df['Timestamp'])
        start_time = df.iloc[0]['Timestamp']
        df['RelativeTime'] = df['Timestamp'] - start_time
        
        # Prepare response data
        flight_points = []
        for _, row in df.iterrows():
            flight_points.append({
                'timestamp': int(row['Timestamp']),
                'utc': row['UTC'],
                'callsign': row['Callsign'],
                'latitude': float(row['Latitude']),
                'longitude': float(row['Longitude']),
                'altitude': int(row['Altitude']),
                'speed': int(row['Speed']),
                'heading': float(row['Heading']),
                'distanceFromStart': float(row['DistanceFromStart']),
                'relativeTime': float(row['RelativeTime'])
            })
        
        # Calculate statistics
        stats = {
            'totalPoints': len(df),
            'callsign': df.iloc[0]['Callsign'],
            'maxAltitude': int(df['Altitude'].max()),
            'maxSpeed': int(df['Speed'].max()),
            'totalDistance': float(df['DistanceFromStart'].max()),
            'duration': float(df['RelativeTime'].max()),
            'startTime': df.iloc[0]['UTC'],
            'endTime': df.iloc[-1]['UTC'],
            'bounds': {
                'north': float(df['Latitude'].max()),
                'south': float(df['Latitude'].min()),
                'east': float(df['Longitude'].max()),
                'west': float(df['Longitude'].min())
            }
        }
        
        # Prepare plot data
        plots = {
            'altitude': {
                'x': df['RelativeTime'].tolist(),
                'y': df['Altitude'].tolist(),
                'label': 'Altitude (ft)'
            },
            'speed': {
                'x': df['RelativeTime'].tolist(),
                'y': df['Speed'].tolist(),
                'label': 'Speed (kts)'
            },
            'distance': {
                'x': df['RelativeTime'].tolist(),
                'y': df['DistanceFromStart'].tolist(),
                'label': 'Distance from Start (m)'
            }
        }
        
        return JSONResponse({
            'success': True,
            'data': {
                'flightPoints': flight_points,
                'statistics': stats,
                'plots': plots
            }
        })
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)