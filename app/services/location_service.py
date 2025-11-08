"""
Google Maps Service
Handles location tracking, distance calculations, and geocoding
"""
import googlemaps
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from config import Config
from geopy.distance import geodesic


class LocationService:
    """Service for Google Maps API and location operations"""
    
    def __init__(self):
        # Initialize Google Maps client
        # Note: Will use API key from config when available
        self.gmaps_client = None
        if Config.GOOGLE_MAPS_API_KEY:
            self.gmaps_client = googlemaps.Client(key=Config.GOOGLE_MAPS_API_KEY)
        
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> Dict:
        """
        Calculate distance between two GPS coordinates
        
        Args:
            point1: (latitude, longitude)
            point2: (latitude, longitude)
            
        Returns:
            {
                'distance_km': float,
                'distance_meters': float,
                'distance_miles': float
            }
        """
        distance_km = geodesic(point1, point2).kilometers
        
        return {
            'distance_km': round(distance_km, 2),
            'distance_meters': round(distance_km * 1000, 2),
            'distance_miles': round(distance_km * 0.621371, 2)
        }
    
    def find_nearest_point(
        self, 
        user_location: Tuple[float, float], 
        points: List[Dict]
    ) -> Optional[Dict]:
        """
        Find the nearest point from a list of points
        
        Args:
            user_location: (latitude, longitude)
            points: List of dicts with 'latitude', 'longitude', and other data
            
        Returns:
            Nearest point with added 'distance' field
        """
        if not points:
            return None
        
        min_distance = float('inf')
        nearest_point = None
        
        for point in points:
            point_coords = (point['latitude'], point['longitude'])
            distance = geodesic(user_location, point_coords).kilometers
            
            if distance < min_distance:
                min_distance = distance
                nearest_point = point.copy()
                nearest_point['distance'] = self.calculate_distance(user_location, point_coords)
        
        return nearest_point
    
    def is_near_location(
        self,
        current_location: Tuple[float, float],
        target_location: Tuple[float, float],
        threshold_meters: float = 100
    ) -> bool:
        """
        Check if current location is near target location
        
        Args:
            current_location: (latitude, longitude)
            target_location: (latitude, longitude)
            threshold_meters: Distance threshold in meters
            
        Returns:
            True if within threshold
        """
        distance = self.calculate_distance(current_location, target_location)
        return distance['distance_meters'] <= threshold_meters
    
    def get_walking_directions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict]:
        """
        Get walking directions between two points
        Requires Google Maps API key
        
        Args:
            origin: (latitude, longitude)
            destination: (latitude, longitude)
            
        Returns:
            {
                'duration_minutes': int,
                'distance': dict,
                'steps': list,
                'polyline': str
            }
        """
        if not self.gmaps_client:
            # Fallback: calculate straight-line distance
            distance = self.calculate_distance(origin, destination)
            # Rough estimate: 5 km/h walking speed
            duration_minutes = int((distance['distance_km'] / 5) * 60)
            
            return {
                'duration_minutes': duration_minutes,
                'distance': distance,
                'steps': [],
                'polyline': None,
                'note': 'Estimated - Google Maps API key not configured'
            }
        
        try:
            directions = self.gmaps_client.directions(
                origin=origin,
                destination=destination,
                mode='walking',
                departure_time=datetime.now()
            )
            
            if not directions:
                return None
            
            route = directions[0]
            leg = route['legs'][0]
            
            return {
                'duration_minutes': int(leg['duration']['value'] / 60),
                'distance': {
                    'distance_km': round(leg['distance']['value'] / 1000, 2),
                    'distance_meters': leg['distance']['value'],
                    'distance_miles': round(leg['distance']['value'] / 1609.34, 2)
                },
                'steps': [
                    {
                        'instruction': step['html_instructions'],
                        'distance': step['distance']['text'],
                        'duration': step['duration']['text']
                    }
                    for step in leg['steps']
                ],
                'polyline': route['overview_polyline']['points']
            }
        except Exception as e:
            print(f"Error getting walking directions: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address to GPS coordinates
        Requires Google Maps API key
        
        Args:
            address: Street address or place name
            
        Returns:
            (latitude, longitude) or None
        """
        if not self.gmaps_client:
            return None
        
        try:
            result = self.gmaps_client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return (location['lat'], location['lng'])
            return None
        except Exception as e:
            print(f"Error geocoding address: {e}")
            return None
    
    def reverse_geocode(self, location: Tuple[float, float]) -> Optional[str]:
        """
        Convert GPS coordinates to address
        Requires Google Maps API key
        
        Args:
            location: (latitude, longitude)
            
        Returns:
            Formatted address string or None
        """
        if not self.gmaps_client:
            return None
        
        try:
            result = self.gmaps_client.reverse_geocode(location)
            if result:
                return result[0]['formatted_address']
            return None
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return None
    
    def format_distance_message(self, distance: Dict) -> str:
        """
        Format distance for user-friendly message
        
        Args:
            distance: Distance dict from calculate_distance()
            
        Returns:
            Formatted string like "1.2 km" or "500 meters"
        """
        if distance['distance_km'] >= 1:
            return f"{distance['distance_km']} km"
        else:
            return f"{int(distance['distance_meters'])} meters"
    
    def estimate_walking_time(self, distance_km: float) -> int:
        """
        Estimate walking time in minutes
        Assumes average walking speed of 5 km/h
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Estimated minutes
        """
        return int((distance_km / 5) * 60)


# Singleton instance
location_service = LocationService()
