"""
BART API Service
Handles all interactions with the BART API for real-time transit data
"""
import requests
from datetime import datetime
from typing import List, Dict, Optional
from config import Config

class BARTService:
    """Service for interacting with BART API"""
    
    def __init__(self):
        self.api_key = Config.BART_API_KEY
        self.base_url = Config.BART_API_BASE_URL
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to BART API"""
        params['key'] = self.api_key
        params['json'] = 'y'  # Request JSON response
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making BART API request: {e}")
            return {}
    
    def get_all_stations(self) -> List[Dict]:
        """Get list of all BART stations"""
        data = self._make_request('stn.aspx', {'cmd': 'stns'})
        
        if 'root' in data and 'stations' in data['root']:
            stations = data['root']['stations']['station']
            return stations
        return []
    
    def get_station_info(self, station_abbr: str) -> Dict:
        """Get detailed info for a specific station"""
        data = self._make_request('stn.aspx', {
            'cmd': 'stninfo',
            'orig': station_abbr
        })
        
        if 'root' in data and 'stations' in data['root']:
            return data['root']['stations']['station']
        return {}
    
    def get_real_time_departures(self, station_abbr: str) -> List[Dict]:
        """Get real-time departure estimates for a station"""
        data = self._make_request('etd.aspx', {
            'cmd': 'etd',
            'orig': station_abbr
        })
        
        departures = []
        if 'root' in data and 'station' in data['root']:
            station_data = data['root']['station'][0]
            
            if 'etd' in station_data:
                for dest in station_data['etd']:
                    destination = dest['destination']
                    
                    for estimate in dest['estimate']:
                        departures.append({
                            'destination': destination,
                            'minutes': estimate['minutes'],
                            'platform': estimate['platform'],
                            'direction': estimate['direction'],
                            'length': estimate['length'],
                            'color': estimate['color'],
                            'hexcolor': estimate['hexcolor'],
                            'bikeflag': estimate['bikeflag'] == '1'
                        })
        
        return departures
    
    def get_route_schedule(self, origin: str, destination: str) -> List[Dict]:
        """Get route schedule between two stations"""
        data = self._make_request('sched.aspx', {
            'cmd': 'depart',
            'orig': origin,
            'dest': destination,
            'b': '0',  # Number of trips before current time
            'a': '4'   # Number of trips after current time
        })
        
        trips = []
        if 'root' in data and 'schedule' in data['root']:
            schedule = data['root']['schedule']
            
            if 'request' in schedule and 'trip' in schedule['request']:
                for trip in schedule['request']['trip']:
                    trips.append({
                        'origin': trip['@origin'],
                        'destination': trip['@destination'],
                        'fare': trip['@fare'],
                        'orig_time': trip['@origTimeMin'],
                        'dest_time': trip['@destTimeMin'],
                        'trip_time': trip['@tripTime'],
                        'legs': trip.get('leg', [])
                    })
        
        return trips
    
    def get_advisories(self) -> List[Dict]:
        """Get current service advisories and delays"""
        data = self._make_request('bsa.aspx', {'cmd': 'bsa'})
        
        advisories = []
        if 'root' in data and 'bsa' in data['root']:
            bsa_list = data['root']['bsa']
            
            if isinstance(bsa_list, list):
                for advisory in bsa_list:
                    advisories.append({
                        'station': advisory.get('station', 'System-wide'),
                        'type': advisory.get('type', 'DELAY'),
                        'description': advisory.get('description', {}).get('#cdata-section', ''),
                        'posted': advisory.get('posted', '')
                    })
        
        return advisories
    
    def find_nearest_station(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Find the nearest BART station to given coordinates"""
        stations = self.get_all_stations()
        
        if not stations:
            return None
        
        from geopy.distance import geodesic
        
        min_distance = float('inf')
        nearest_station = None
        
        for station in stations:
            if 'gtfs_latitude' in station and 'gtfs_longitude' in station:
                station_coords = (
                    float(station['gtfs_latitude']),
                    float(station['gtfs_longitude'])
                )
                user_coords = (latitude, longitude)
                
                distance = geodesic(user_coords, station_coords).km
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = {
                        'name': station['name'],
                        'abbr': station['abbr'],
                        'address': station.get('address', ''),
                        'distance_km': round(distance, 2)
                    }
        
        return nearest_station
    
    def format_departure_message(self, departures: List[Dict], limit: int = 5) -> str:
        """Format departure info into a friendly message"""
        if not departures:
            return "No trains scheduled right now 😕"
        
        message = "🚇 **Next Trains:**\n\n"
        
        for i, dep in enumerate(departures[:limit]):
            minutes = dep['minutes']
            if minutes == 'Leaving':
                time_str = "🔥 **LEAVING NOW**"
            else:
                time_str = f"⏱️ {minutes} min"
            
            bike_flag = "🚴" if dep['bikeflag'] else ""
            
            message += f"{time_str} → **{dep['destination']}** {bike_flag}\n"
            message += f"   Platform {dep['platform']} | {dep['length']} cars\n\n"
        
        return message

# Singleton instance
bart_service = BARTService()
