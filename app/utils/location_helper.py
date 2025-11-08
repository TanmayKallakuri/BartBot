"""
Location Helper Utilities
Helper functions for location-based operations
"""
from typing import Tuple, Dict, List, Optional
from app.services.maps_service import maps_service
from app.services.bart_service import bart_service


class LocationHelper:
    """Helper class for location operations"""
    
    @staticmethod
    def find_nearest_bart_station(
        latitude: float,
        longitude: float
    ) -> Optional[Dict]:
        """
        Find nearest BART station to user's location
        Returns: {
            'station': {...},  # Station info from BART API
            'distance': {...},  # Distance info from Maps
            'walking_time': int  # Minutes
        }
        """
        # Get nearest station from BART API
        nearest_bart = bart_service.find_nearest_station(latitude, longitude)
        
        if not nearest_bart:
            return None
        
        # Get walking distance/time from Google Maps
        user_location = (latitude, longitude)
        
        # Get station coordinates from BART API
        all_stations = bart_service.get_all_stations()
        station_data = next(
            (s for s in all_stations if s['abbr'] == nearest_bart['abbr']),
            None
        )
        
        if station_data and 'gtfs_latitude' in station_data:
            station_location = (
                float(station_data['gtfs_latitude']),
                float(station_data['gtfs_longitude'])
            )
            
            walking_info = maps_service.get_walking_distance_to_station(
                user_location,
                station_location
            )
            
            return {
                'station': nearest_bart,
                'distance': walking_info,
                'coordinates': {
                    'lat': station_data['gtfs_latitude'],
                    'lng': station_data['gtfs_longitude']
                }
            }
        
        return {
            'station': nearest_bart,
            'distance': {
                'distance_km': nearest_bart['distance_km'],
                'distance_text': f"{nearest_bart['distance_km']} km",
                'duration_minutes': int((nearest_bart['distance_km'] / 5) * 60),
                'duration_text': f"{int((nearest_bart['distance_km'] / 5) * 60)} mins"
            },
            'coordinates': None
        }
    
    @staticmethod
    def get_station_coordinates(station_abbr: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a BART station"""
        all_stations = bart_service.get_all_stations()
        station = next(
            (s for s in all_stations if s['abbr'] == station_abbr),
            None
        )
        
        if station and 'gtfs_latitude' in station:
            return (
                float(station['gtfs_latitude']),
                float(station['gtfs_longitude'])
            )
        
        return None
    
    @staticmethod
    def is_user_near_station(
        user_lat: float,
        user_lng: float,
        station_abbr: str,
        threshold_meters: float = 100
    ) -> bool:
        """
        Check if user is near a specific station
        Default threshold: 100 meters (about 1 city block)
        """
        station_coords = LocationHelper.get_station_coordinates(station_abbr)
        
        if not station_coords:
            return False
        
        return maps_service.is_near_station(
            (user_lat, user_lng),
            station_coords,
            threshold_meters
        )
    
    @staticmethod
    def calculate_route_progress(
        user_lat: float,
        user_lng: float,
        start_station: str,
        end_station: str
    ) -> Dict:
        """
        Calculate how far along a route the user is
        Returns: {
            'distance_from_start_km': float,
            'distance_to_end_km': float,
            'progress_percentage': float,
            'is_near_destination': bool
        }
        """
        start_coords = LocationHelper.get_station_coordinates(start_station)
        end_coords = LocationHelper.get_station_coordinates(end_station)
        user_coords = (user_lat, user_lng)
        
        if not start_coords or not end_coords:
            return {}
        
        # Calculate distances
        dist_from_start = maps_service.calculate_distance(user_coords, start_coords)
        dist_to_end = maps_service.calculate_distance(user_coords, end_coords)
        total_route = maps_service.calculate_distance(start_coords, end_coords)
        
        # Calculate progress (rough estimate)
        progress = (dist_from_start['km'] / total_route['km']) * 100
        progress = min(100, max(0, progress))  # Clamp between 0-100
        
        # Check if near destination (within 200 meters)
        is_near_destination = dist_to_end['meters'] <= 200
        
        return {
            'distance_from_start_km': dist_from_start['km'],
            'distance_to_end_km': dist_to_end['km'],
            'progress_percentage': round(progress, 1),
            'is_near_destination': is_near_destination,
            'meters_to_destination': dist_to_end['meters']
        }
    
    @staticmethod
    def should_send_get_off_alert(
        user_lat: float,
        user_lng: float,
        destination_station: str,
        threshold_meters: float = 500
    ) -> Dict:
        """
        Determine if "get off" alert should be sent
        Returns: {
            'should_alert': bool,
            'distance_to_station': float (meters),
            'alert_type': 'approaching' | 'at_station' | 'passed'
        }
        """
        station_coords = LocationHelper.get_station_coordinates(destination_station)
        
        if not station_coords:
            return {'should_alert': False}
        
        user_coords = (user_lat, user_lng)
        distance = maps_service.calculate_distance(user_coords, station_coords)
        
        # Within 100 meters - AT STATION
        if distance['meters'] <= 100:
            return {
                'should_alert': True,
                'distance_to_station': distance['meters'],
                'alert_type': 'at_station'
            }
        
        # Within 500 meters - APPROACHING
        elif distance['meters'] <= threshold_meters:
            return {
                'should_alert': True,
                'distance_to_station': distance['meters'],
                'alert_type': 'approaching'
            }
        
        # More than 500 meters - NO ALERT
        else:
            return {
                'should_alert': False,
                'distance_to_station': distance['meters'],
                'alert_type': 'far'
            }
    
    @staticmethod
    def format_location_message(
        latitude: float,
        longitude: float,
        include_nearby_station: bool = True
    ) -> str:
        """
        Format a friendly location message
        Example: "You're near Market St, San Francisco (0.3 km from Embarcadero station)"
        """
        description = maps_service.get_location_description(latitude, longitude)
        
        if include_nearby_station:
            nearest = LocationHelper.find_nearest_bart_station(latitude, longitude)
            if nearest:
                station_name = nearest['station']['name']
                distance = nearest['distance']['distance_text']
                return f"{description} ({distance} from {station_name} station)"
        
        return description
    
    @staticmethod
    def get_walking_directions_to_station(
        user_lat: float,
        user_lng: float,
        station_abbr: str
    ) -> Optional[Dict]:
        """
        Get step-by-step walking directions to a station
        """
        station_coords = LocationHelper.get_station_coordinates(station_abbr)
        
        if not station_coords:
            return None
        
        origin = f"{user_lat},{user_lng}"
        destination = f"{station_coords[0]},{station_coords[1]}"
        
        return maps_service.get_directions(origin, destination, mode="walking")


# Singleton instance
location_helper = LocationHelper()
