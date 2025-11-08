"""
Google Maps Service
Handles location-based operations: nearest stations, distance calculations, directions
"""
import googlemaps
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from geopy.distance import geodesic
from config import Config


class GoogleMapsService:
    """Service for Google Maps API operations"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None
            print("⚠️ Warning: Google Maps API key not set. Location features disabled.")
    
    def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Convert address to coordinates
        Returns: {'lat': float, 'lng': float, 'formatted_address': str}
        """
        if not self.client:
            return None
        
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': result[0]['formatted_address']
                }
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Convert coordinates to address
        Returns: Formatted address string
        """
        if not self.client:
            return None
        
        try:
            result = self.client.reverse_geocode((latitude, longitude))
            if result:
                return result[0]['formatted_address']
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
        
        return None
    
    def calculate_distance(
        self, 
        origin: Tuple[float, float], 
        destination: Tuple[float, float]
    ) -> Dict:
        """
        Calculate distance between two coordinates
        Args:
            origin: (lat, lng)
            destination: (lat, lng)
        Returns: {'km': float, 'miles': float, 'meters': float}
        """
        distance_km = geodesic(origin, destination).km
        distance_miles = geodesic(origin, destination).miles
        distance_meters = geodesic(origin, destination).meters
        
        return {
            'km': round(distance_km, 2),
            'miles': round(distance_miles, 2),
            'meters': round(distance_meters, 2)
        }
    
    def get_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str],
        mode: str = "walking"
    ) -> Optional[Dict]:
        """
        Get distance and duration between multiple origins and destinations
        Args:
            origins: List of addresses or coordinates
            destinations: List of addresses or coordinates
            mode: 'driving', 'walking', 'bicycling', 'transit'
        """
        if not self.client:
            return None
        
        try:
            result = self.client.distance_matrix(
                origins=origins,
                destinations=destinations,
                mode=mode,
                units="metric"
            )
            return result
        except Exception as e:
            print(f"Distance matrix error: {e}")
        
        return None
    
    def get_walking_distance_to_station(
        self,
        user_location: Tuple[float, float],
        station_location: Tuple[float, float]
    ) -> Dict:
        """
        Get walking distance and time to station
        Returns: {
            'distance_km': float,
            'distance_text': str (e.g., "0.5 km"),
            'duration_minutes': int,
            'duration_text': str (e.g., "6 mins")
        }
        """
        if not self.client:
            # Fallback to simple distance calculation
            distance = self.calculate_distance(user_location, station_location)
            # Rough estimate: 5 km/h walking speed
            duration_minutes = int((distance['km'] / 5) * 60)
            return {
                'distance_km': distance['km'],
                'distance_text': f"{distance['km']} km",
                'duration_minutes': duration_minutes,
                'duration_text': f"{duration_minutes} mins"
            }
        
        try:
            result = self.client.distance_matrix(
                origins=[user_location],
                destinations=[station_location],
                mode="walking",
                units="metric"
            )
            
            if result['rows'][0]['elements'][0]['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                distance_km = element['distance']['value'] / 1000
                duration_minutes = element['duration']['value'] // 60
                
                return {
                    'distance_km': round(distance_km, 2),
                    'distance_text': element['distance']['text'],
                    'duration_minutes': duration_minutes,
                    'duration_text': element['duration']['text']
                }
        except Exception as e:
            print(f"Walking distance error: {e}")
        
        # Fallback
        distance = self.calculate_distance(user_location, station_location)
        duration_minutes = int((distance['km'] / 5) * 60)
        return {
            'distance_km': distance['km'],
            'distance_text': f"{distance['km']} km",
            'duration_minutes': duration_minutes,
            'duration_text': f"{duration_minutes} mins"
        }
    
    def get_directions(
        self,
        origin: str,
        destination: str,
        mode: str = "walking"
    ) -> Optional[Dict]:
        """
        Get directions between two points
        Args:
            origin: Address or coordinates
            destination: Address or coordinates
            mode: 'driving', 'walking', 'bicycling', 'transit'
        Returns: Direction steps and route info
        """
        if not self.client:
            return None
        
        try:
            result = self.client.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time=datetime.now()
            )
            
            if result:
                route = result[0]
                leg = route['legs'][0]
                
                return {
                    'distance': leg['distance']['text'],
                    'duration': leg['duration']['text'],
                    'start_address': leg['start_address'],
                    'end_address': leg['end_address'],
                    'steps': [
                        {
                            'instruction': step['html_instructions'],
                            'distance': step['distance']['text'],
                            'duration': step['duration']['text']
                        }
                        for step in leg['steps']
                    ]
                }
        except Exception as e:
            print(f"Directions error: {e}")
        
        return None
    
    def is_near_station(
        self,
        user_location: Tuple[float, float],
        station_location: Tuple[float, float],
        threshold_meters: float = 100
    ) -> bool:
        """
        Check if user is near a station (within threshold)
        Default threshold: 100 meters
        """
        distance = self.calculate_distance(user_location, station_location)
        return distance['meters'] <= threshold_meters
    
    def get_location_description(
        self,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Get a friendly description of a location
        Returns: "Near Market St & 5th St, San Francisco"
        """
        if not self.client:
            return f"Location: {latitude:.4f}, {longitude:.4f}"
        
        address = self.reverse_geocode(latitude, longitude)
        if address:
            # Simplify address
            parts = address.split(',')
            if len(parts) >= 2:
                return f"Near {parts[0]}, {parts[-2].strip()}"
            return parts[0]
        
        return f"Location: {latitude:.4f}, {longitude:.4f}"
    
    def find_nearest_from_list(
        self,
        user_location: Tuple[float, float],
        locations: List[Dict]
    ) -> Optional[Dict]:
        """
        Find nearest location from a list
        Args:
            user_location: (lat, lng)
            locations: List of dicts with 'lat', 'lng', and other data
        Returns: Nearest location dict with added 'distance' field
        """
        if not locations:
            return None
        
        min_distance = float('inf')
        nearest = None
        
        for location in locations:
            if 'lat' not in location or 'lng' not in location:
                continue
            
            loc_coords = (location['lat'], location['lng'])
            distance = self.calculate_distance(user_location, loc_coords)
            
            if distance['km'] < min_distance:
                min_distance = distance['km']
                nearest = location.copy()
                nearest['distance'] = distance
        
        return nearest
    
    def format_distance_friendly(self, distance_km: float) -> str:
        """
        Format distance in a friendly way
        Examples:
            0.05 km -> "50 meters"
            0.5 km -> "500 meters"
            1.2 km -> "1.2 km"
            5.8 km -> "5.8 km"
        """
        if distance_km < 1:
            meters = int(distance_km * 1000)
            return f"{meters} meters"
        else:
            return f"{distance_km:.1f} km"
    
    def get_eta_message(
        self,
        distance_km: float,
        mode: str = "walking"
    ) -> str:
        """
        Get estimated time message based on distance and mode
        """
        # Average speeds (km/h)
        speeds = {
            'walking': 5,
            'biking': 15,
            'driving': 30
        }
        
        speed = speeds.get(mode, 5)
        duration_minutes = int((distance_km / speed) * 60)
        
        if duration_minutes < 1:
            return "less than a minute"
        elif duration_minutes == 1:
            return "1 minute"
        else:
            return f"{duration_minutes} minutes"


# Singleton instance
maps_service = GoogleMapsService()
