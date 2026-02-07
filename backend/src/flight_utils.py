"""
Flight calculations utilities
Heading and distance calculations for GPS coordinates
"""

import math


def calculate_heading(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate bearing/heading between two GPS coordinates
    
    Args:
        lat1: Starting latitude in degrees
        lon1: Starting longitude in degrees
        lat2: Ending latitude in degrees
        lon2: Ending longitude in degrees
    
    Returns:
        Heading in degrees (0-360)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon_diff = math.radians(lon2 - lon1)
    
    x = math.sin(lon_diff) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon_diff)
    
    heading = math.atan2(x, y)
    heading = math.degrees(heading)
    heading = (heading + 360) % 360
    
    return heading


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula
    
    Args:
        lat1: Starting latitude in degrees
        lon1: Starting longitude in degrees
        lat2: Ending latitude in degrees
        lon2: Ending longitude in degrees
    
    Returns:
        Distance in meters
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
    """
    Parse position string 'lat,lon' into tuple (lat, lon)
    
    Args:
        position_str: Position string in format "latitude,longitude"
    
    Returns:
        Tuple of (latitude, longitude) or (None, None) if parsing fails
    """
    try:
        # Remove any quotes that might be around the position
        position_str = str(position_str).strip().strip('"').strip("'")
        lat, lon = position_str.split(',')
        return float(lat), float(lon)
    except:
        return None, None