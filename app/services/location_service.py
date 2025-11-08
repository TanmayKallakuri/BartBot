"""
Google Maps Service
Handles location tracking, distance calculations, and geocoding
"""
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from config import Config
from geopy.distance import geodesic

# Try to import googlemaps, but make it optional
try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False


class LocationService:
    """Service for Google Maps API and location operations"""

    def __init__(self):
        # Initialize Google Maps client
        # Note: Will use API key from config when available
        self.gmaps_client = None
        if Config.GOOGLE_MAPS_API_KEY and GOOGLEMAPS_AVAILABLE:
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

    def get_transit_directions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        mode: str = 'transit'
    ) -> Optional[Dict]:
        """
        Get transit directions (public transportation + walking)
        Requires Google Maps API key

        Args:
            origin: (latitude, longitude)
            destination: (latitude, longitude)
            mode: 'transit', 'walking', 'driving', or 'bicycling'

        Returns:
            {
                'duration_minutes': int,
                'distance': dict,
                'steps': list,
                'departure_time': str,
                'arrival_time': str,
                'transit_details': list,
                'polyline': str
            }
        """
        if not self.gmaps_client:
            # Fallback for when API is not available
            distance = self.calculate_distance(origin, destination)
            duration_minutes = self.estimate_walking_time(distance['distance_km'])

            return {
                'duration_minutes': duration_minutes,
                'distance': distance,
                'steps': [],
                'mode': mode,
                'polyline': None,
                'note': 'Estimated - Google Maps API key not configured'
            }

        try:
            directions = self.gmaps_client.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time=datetime.now()
            )

            if not directions:
                return None

            route = directions[0]
            leg = route['legs'][0]

            # Extract transit details
            transit_details = []
            steps_formatted = []

            for step in leg['steps']:
                step_info = {
                    'instruction': step.get('html_instructions', ''),
                    'distance': step['distance']['text'],
                    'duration': step['duration']['text'],
                    'travel_mode': step.get('travel_mode', '')
                }

                # Extract transit info (bus, train, etc.)
                if 'transit_details' in step:
                    transit = step['transit_details']
                    transit_info = {
                        'type': transit['line']['vehicle']['type'],  # BUS, RAIL, etc.
                        'line_name': transit['line'].get('name', ''),
                        'line_short_name': transit['line'].get('short_name', ''),
                        'departure_stop': transit['departure_stop']['name'],
                        'arrival_stop': transit['arrival_stop']['name'],
                        'num_stops': transit.get('num_stops', 0),
                        'departure_time': transit.get('departure_time', {}).get('text', ''),
                        'arrival_time': transit.get('arrival_time', {}).get('text', ''),
                        'headsign': transit.get('headsign', '')
                    }
                    step_info['transit'] = transit_info
                    transit_details.append(transit_info)

                steps_formatted.append(step_info)

            return {
                'duration_minutes': int(leg['duration']['value'] / 60),
                'distance': {
                    'distance_km': round(leg['distance']['value'] / 1000, 2),
                    'distance_meters': leg['distance']['value'],
                    'distance_miles': round(leg['distance']['value'] / 1609.34, 2)
                },
                'steps': steps_formatted,
                'departure_time': leg.get('departure_time', {}).get('text', ''),
                'arrival_time': leg.get('arrival_time', {}).get('text', ''),
                'transit_details': transit_details,
                'polyline': route['overview_polyline']['points'],
                'mode': mode
            }
        except Exception as e:
            print(f"Error getting transit directions: {e}")
            return None

    def find_nearby_bus_stops(
        self,
        location: Tuple[float, float],
        radius_meters: int = 500
    ) -> List[Dict]:
        """
        Find nearby bus stops using Google Places API
        Requires Google Maps API key

        Args:
            location: (latitude, longitude)
            radius_meters: Search radius in meters (default 500m)

        Returns:
            List of nearby bus stops with details
        """
        if not self.gmaps_client:
            return []

        try:
            results = self.gmaps_client.places_nearby(
                location=location,
                radius=radius_meters,
                type='bus_station'
            )

            bus_stops = []
            for place in results.get('results', []):
                stop_location = place['geometry']['location']
                stop_coords = (stop_location['lat'], stop_location['lng'])
                distance = self.calculate_distance(location, stop_coords)

                bus_stops.append({
                    'name': place.get('name', 'Unknown Stop'),
                    'address': place.get('vicinity', ''),
                    'latitude': stop_location['lat'],
                    'longitude': stop_location['lng'],
                    'distance': distance,
                    'place_id': place.get('place_id', ''),
                    'rating': place.get('rating', None)
                })

            # Sort by distance
            bus_stops.sort(key=lambda x: x['distance']['distance_meters'])

            return bus_stops
        except Exception as e:
            print(f"Error finding bus stops: {e}")
            return []

    def find_nearby_transit_hubs(
        self,
        location: Tuple[float, float],
        radius_meters: int = 1000
    ) -> List[Dict]:
        """
        Find nearby transit hubs (train stations, subway, bus terminals)
        Requires Google Maps API key

        Args:
            location: (latitude, longitude)
            radius_meters: Search radius in meters (default 1km)

        Returns:
            List of nearby transit hubs
        """
        if not self.gmaps_client:
            return []

        try:
            # Search for different types of transit stations
            transit_types = ['subway_station', 'train_station', 'transit_station', 'bus_station']
            all_hubs = []
            seen_place_ids = set()

            for transit_type in transit_types:
                results = self.gmaps_client.places_nearby(
                    location=location,
                    radius=radius_meters,
                    type=transit_type
                )

                for place in results.get('results', []):
                    place_id = place.get('place_id', '')

                    # Avoid duplicates
                    if place_id in seen_place_ids:
                        continue
                    seen_place_ids.add(place_id)

                    stop_location = place['geometry']['location']
                    stop_coords = (stop_location['lat'], stop_location['lng'])
                    distance = self.calculate_distance(location, stop_coords)

                    all_hubs.append({
                        'name': place.get('name', 'Unknown Hub'),
                        'type': transit_type.replace('_', ' ').title(),
                        'address': place.get('vicinity', ''),
                        'latitude': stop_location['lat'],
                        'longitude': stop_location['lng'],
                        'distance': distance,
                        'place_id': place_id,
                        'rating': place.get('rating', None)
                    })

            # Sort by distance
            all_hubs.sort(key=lambda x: x['distance']['distance_meters'])

            return all_hubs
        except Exception as e:
            print(f"Error finding transit hubs: {e}")
            return []

    def get_directions_with_alternatives(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        modes: List[str] = ['walking', 'transit']
    ) -> Dict:
        """
        Get directions using multiple transportation modes

        Args:
            origin: (latitude, longitude)
            destination: (latitude, longitude)
            modes: List of modes to try ['walking', 'transit', 'driving', 'bicycling']

        Returns:
            Dict with directions for each mode
        """
        results = {}

        for mode in modes:
            if mode == 'walking':
                results[mode] = self.get_walking_directions(origin, destination)
            else:
                results[mode] = self.get_transit_directions(origin, destination, mode)

        return results


# Singleton instance
location_service = LocationService()
