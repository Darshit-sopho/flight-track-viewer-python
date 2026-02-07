"""
CSV parsing and data processing for flight track data
"""

import pandas as pd
from io import StringIO
from typing import Dict, List, Any
from .flight_utils import calculate_heading, calculate_distance, parse_position


class FlightDataProcessor:
    """Process flight trajectory data from CSV files"""
    
    def __init__(self):
        self.required_columns = ['Timestamp', 'UTC', 'Callsign', 'Position', 'Altitude', 'Speed', 'Direction']
    
    def detect_delimiter(self, csv_string: str) -> str:
        """
        Auto-detect CSV delimiter (tab or comma)
        
        Args:
            csv_string: Raw CSV content as string
        
        Returns:
            Delimiter character ('\\t' or ',')
        """
        first_line = csv_string.split('\n')[0]
        return '\t' if '\t' in first_line else ','
    
    def validate_csv(self, df: pd.DataFrame) -> bool:
        """
        Validate that CSV has all required columns
        
        Args:
            df: Pandas DataFrame to validate
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        return True
    
    def parse_csv(self, csv_content: bytes) -> pd.DataFrame:
        """
        Parse CSV content into DataFrame
        
        Args:
            csv_content: Raw CSV file content as bytes
        
        Returns:
            Pandas DataFrame with flight data
        """
        csv_string = csv_content.decode('utf-8')
        delimiter = self.detect_delimiter(csv_string)
        df = pd.read_csv(StringIO(csv_string), sep=delimiter)
        self.validate_csv(df)
        return df
    
    def process_positions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse Position column into separate Latitude and Longitude columns
        
        Args:
            df: DataFrame with Position column
        
        Returns:
            DataFrame with added Latitude and Longitude columns
        """
        positions = df['Position'].apply(parse_position)
        df['Latitude'] = [pos[0] for pos in positions]
        df['Longitude'] = [pos[1] for pos in positions]
        
        # Remove rows with invalid positions
        df = df.dropna(subset=['Latitude', 'Longitude'])
        
        if len(df) == 0:
            raise ValueError("No valid position data found in CSV")
        
        return df
    
    def calculate_headings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate headings between consecutive GPS points
        
        Args:
            df: DataFrame with Latitude and Longitude columns
        
        Returns:
            DataFrame with added Heading column
        """
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
        return df
    
    def calculate_distances(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate cumulative distance from starting point
        
        Args:
            df: DataFrame with Latitude and Longitude columns
        
        Returns:
            DataFrame with added DistanceFromStart column
        """
        start_lat = df.iloc[0]['Latitude']
        start_lon = df.iloc[0]['Longitude']
        
        distances = []
        for i in range(len(df)):
            curr_lat = df.iloc[i]['Latitude']
            curr_lon = df.iloc[i]['Longitude']
            distance = calculate_distance(start_lat, start_lon, curr_lat, curr_lon)
            distances.append(distance)
        
        df['DistanceFromStart'] = distances
        return df
    
    def calculate_time_series(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate relative time from start
        
        Args:
            df: DataFrame with Timestamp column
        
        Returns:
            DataFrame with added RelativeTime column
        """
        df['Timestamp'] = pd.to_numeric(df['Timestamp'])
        start_time = df.iloc[0]['Timestamp']
        df['RelativeTime'] = df['Timestamp'] - start_time
        return df
    
    def generate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate flight statistics
        
        Args:
            df: Processed DataFrame
        
        Returns:
            Dictionary of statistics
        """
        return {
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
    
    def generate_plot_data(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Generate data for charts
        
        Args:
            df: Processed DataFrame
        
        Returns:
            Dictionary with plot data for altitude, speed, and distance
        """
        return {
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
    
    def generate_flight_points(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate list of flight points for frontend
        
        Args:
            df: Processed DataFrame
        
        Returns:
            List of dictionaries containing point data
        """
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
        return flight_points
    
    def process_flight_data(self, csv_content: bytes) -> Dict[str, Any]:
        """
        Main processing pipeline for flight data
        
        Args:
            csv_content: Raw CSV file content
        
        Returns:
            Complete processed flight data
        """
        # Parse CSV
        df = self.parse_csv(csv_content)
        
        # Process data
        df = self.process_positions(df)
        df = self.calculate_headings(df)
        df = self.calculate_distances(df)
        df = self.calculate_time_series(df)
        
        # Generate output data
        return {
            'flightPoints': self.generate_flight_points(df),
            'statistics': self.generate_statistics(df),
            'plots': self.generate_plot_data(df)
        }