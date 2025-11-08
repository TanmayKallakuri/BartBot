"""
Enhanced BART Station Service
Combines BART API with location services for smart station finding
"""
from typing import List, Dict, Optional, Tuple
from app.services.bart_service import bart_service
from app.services.location_service import location_service


class StationLocationService:
    """Service for BART station location operations"""
    
    def find_nearest_stations(
        self, 
        user_location: Tuple[float, float],
        limit: int = 5
    ) -> List[Dict]:
        """
        Find nearest BART stations to user's location
        
        Args:
            user_location: (latitude, longitude)
            limit: Number of stations to return
            
        Returns:
            List of nearest stations with distance info
        """
        # Get all BART stations
        all_stations = bart_service.get_all_stations()
        
        # Calculate distances and sort
        stations_with_distance = []
        
        for station in all_stations:
            if 'gtfs_latitude' in station and 'gtfs_longitude' in station:
                station_coords = (
                    float(station['gtfs_latitude']),
                    float(station['gtfs_longitude'])
                )
                
                distance = location_service.calculate_distance(
                    user_location,
                    station_coords
                )
                
                stations_with_distance.append({
                    'name': station['name'],
                    'abbr': station['abbr'],
                    'address': station.get('address', ''),
                    'city': station.get('city', ''),
                    'latitude': float(station['gtfs_latitude']),
                    'longitude': float(station['gtfs_longitude']),
                    'distance': distance,
                    'walking_time_minutes': location_service.estimate_walking_time(
                        distance['distance_km']
                    )
                })
        
        # Sort by distance
        stations_with_distance.sort(key=lambda x: x['distance']['distance_km'])
        
        return stations_with_distance[:limit]
    
    def get_station_with_directions(
        self,
        user_location: Tuple[float, float],
        station_abbr: str
    ) -> Optional[Dict]:
        """
        Get station info with walking directions
        
        Args:
            user_location: (latitude, longitude)
            station_abbr: Station abbreviation (e.g., 'EMBR')
            
        Returns:
            Station info with directions
        """
        # Get station info
        station_info = bart_service.get_station_info(station_abbr)
        
        if not station_info:
            return None
        
        # Get coordinates
        if 'gtfs_latitude' not in station_info or 'gtfs_longitude' not in station_info:
            return None
        
        station_coords = (
            float(station_info['gtfs_latitude']),
            float(station_info['gtfs_longitude'])
        )
        
        # Calculate distance
        distance = location_service.calculate_distance(user_location, station_coords)
        
        # Get walking directions
        directions = location_service.get_walking_directions(
            user_location,
            station_coords
        )
        
        return {
            'station': {
                'name': station_info['name'],
                'abbr': station_info['abbr'],
                'address': station_info.get('address', ''),
                'city': station_info.get('city', ''),
                'latitude': float(station_info['gtfs_latitude']),
                'longitude': float(station_info['gtfs_longitude'])
            },
            'distance': distance,
            'directions': directions
        }
    
    def is_user_at_station(
        self,
        user_location: Tuple[float, float],
        station_abbr: str,
        threshold_meters: float = 200
    ) -> bool:
        """
        Check if user is at or near a station
        
        Args:
            user_location: (latitude, longitude)
            station_abbr: Station abbreviation
            threshold_meters: Distance threshold
            
        Returns:
            True if user is at station
        """
        station_info = bart_service.get_station_info(station_abbr)
        
        if not station_info:
            return False
        
        if 'gtfs_latitude' not in station_info or 'gtfs_longitude' not in station_info:
            return False
        
        station_coords = (
            float(station_info['gtfs_latitude']),
            float(station_info['gtfs_longitude'])
        )
        
        return location_service.is_near_location(
            user_location,
            station_coords,
            threshold_meters
        )
    
    def format_nearest_stations_message(
        self,
        user_location: Tuple[float, float],
        limit: int = 3
    ) -> str:
        """
        Format nearest stations into a friendly message
        
        Args:
            user_location: (latitude, longitude)
            limit: Number of stations to show
            
        Returns:
            Formatted message
        """
        stations = self.find_nearest_stations(user_location, limit)
        
        if not stations:
            return "❌ No BART stations found nearby"
        
        message = "📍 **Nearest BART Stations:**\n\n"
        
        for i, station in enumerate(stations, 1):
            distance_str = location_service.format_distance_message(station['distance'])
            walk_time = station['walking_time_minutes']
            
            message += f"**{i}. {station['name']}**\n"
            message += f"   📏 {distance_str} away (~{walk_time} min walk)\n"
            message += f"   📮 {station['address']}\n\n"
        
        return message
    
    def calculate_trip_progress(
        self,
        user_location: Tuple[float, float],
        start_station_abbr: str,
        end_station_abbr: str
    ) -> Dict:
        """
        Calculate trip progress based on user location
        
        Args:
            user_location: (latitude, longitude)
            start_station_abbr: Starting station
            end_station_abbr: Ending station
            
        Returns:
            {
                'at_start': bool,
                'at_end': bool,
                'closest_station': str,
                'progress_percent': float
            }
        """
        # Get station coordinates
        start_info = bart_service.get_station_info(start_station_abbr)
        end_info = bart_service.get_station_info(end_station_abbr)
        
        if not start_info or not end_info:
            return {}
        
        start_coords = (
            float(start_info['gtfs_latitude']),
            float(start_info['gtfs_longitude'])
        )
        end_coords = (
            float(end_info['gtfs_latitude']),
            float(end_info['gtfs_longitude'])
        )
        
        # Calculate distances
        distance_to_start = location_service.calculate_distance(
            user_location, start_coords
        )['distance_km']
        
        distance_to_end = location_service.calculate_distance(
            user_location, end_coords
        )['distance_km']
        
        total_distance = location_service.calculate_distance(
            start_coords, end_coords
        )['distance_km']
        
        # Calculate progress percentage
        if total_distance > 0:
            progress = ((total_distance - distance_to_end) / total_distance) * 100
            progress = max(0, min(100, progress))  # Clamp between 0-100
        else:
            progress = 0
        
        return {
            'at_start': distance_to_start <= 0.2,  # Within 200m
            'at_end': distance_to_end <= 0.2,
            'distance_to_end_km': round(distance_to_end, 2),
            'progress_percent': round(progress, 1),
            'almost_there': distance_to_end <= 2  # Within 2km
        }


# Singleton instance
station_location_service = StationLocationService()
