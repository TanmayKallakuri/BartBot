"""
Message Parser
Understands user messages and extracts intent and entities
"""
import re
from typing import Dict, Optional, List
from datetime import datetime


class MessageParser:
    """Parse user messages to understand intent"""
    
    # Command patterns
    PATTERNS = {
        'greeting': [
            r'^(hi|hello|hey|yo|sup|what\'s up|whats up)',
            r'^good (morning|afternoon|evening)'
        ],
        'find_station': [
            r'(nearest|closest|near me) (station|bart)',
            r'where.*station',
            r'find.*station'
        ],
        'get_departures': [
            r'(when|what time).*train',
            r'next train',
            r'train.*time',
            r'departures?.*from',
            r'when.*leaving'
        ],
        'plan_route': [
            r'get (me )?to',
            r'go to',
            r'take me to',
            r'how do i get to',
            r'route (to|from)',
            r'heading to',
            r'going to',
            r'\bto\b.*\bstation\b',
            r'from.*to',
            r'need to get to'
        ],
        'start_trip': [
            r'start trip',
            r'begin trip',
            r'trip mode',
            r'let\'s go',
            r'im ready',
            r'i\'m ready'
        ],
        'stop_trip': [
            r'stop trip',
            r'end trip',
            r'cancel trip',
            r'i\'m here',
            r'im here',
            r'arrived'
        ],
        'create_profile': [
            r'save (this )?route',
            r'create profile',
            r'save as (\w+)',
            r'make.*profile'
        ],
        'list_profiles': [
            r'(show|list|my) profile',
            r'saved routes',
            r'my routes'
        ],
        'help': [
            r'^help',
            r'what can you do',
            r'commands',
            r'how.*work'
        ],
        'status': [
            r'(any )?delays',
            r'service.*status',
            r'bart.*status',
            r'problems',
            r'issues'
        ]
    }
    
    # Station abbreviations mapping
    STATION_KEYWORDS = {
        'embarcadero': 'EMBR',
        'montgomery': 'MONT',
        'powell': 'POWL',
        'civic center': 'CIVC',
        '16th': '16TH',
        'mission': '16TH',
        '24th': '24TH',
        'glen park': 'GLEN',
        'balboa': 'BALB',
        'daly city': 'DALY',
        'colma': 'COLM',
        'sfo': 'SFIA',
        'airport': 'SFIA',
        'millbrae': 'MLBR',
        'san bruno': 'SBRN',
        'south san francisco': 'SSAN',
        'coliseum': 'COLS',
        'fruitvale': 'FTVL',
        'lake merritt': 'LAKE',
        '12th': '12TH',
        'oakland': '12TH',
        '19th': '19TH',
        'macarthur': 'MCAR',
        'ashby': 'ASHB',
        'berkeley': 'DBRK',
        'downtown berkeley': 'DBRK',
        'north berkeley': 'NBRK',
        'el cerrito plaza': 'PLZA',
        'el cerrito del norte': 'DELN',
        'richmond': 'RICH',
        'fremont': 'FRMT',
        'union city': 'UCTY',
        'dublin': 'DUBL',
        'pleasanton': 'DUBL',
        'west oakland': 'WOAK',
        'walnut creek': 'WCRK',
        'lafayette': 'LAFY',
        'orinda': 'ORIN',
        'rockridge': 'ROCK',
        'antioch': 'ANTC',
        'pittsburg': 'PITT',
        'concord': 'CONC',
        'pleasant hill': 'PHIL',
        'castro valley': 'CAST',
        'bay fair': 'BAYF',
        'san leandro': 'SANL',
        'hayward': 'HAYW',
        'south hayward': 'SHAY',
        'warm springs': 'WARM'
    }
    
    def parse(self, message: str) -> Dict:
        """
        Parse a user message
        
        Args:
            message: User's message text
            
        Returns:
            {
                'intent': str,
                'confidence': float,
                'entities': dict,
                'original_message': str
            }
        """
        if not message or not message.strip():
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'entities': {},
                'original_message': message
            }
        
        message_lower = message.lower().strip()
        
        # Check each intent pattern
        for intent, patterns in self.PATTERNS.items():
            for pattern in patterns:
                try:
                    match = re.search(pattern, message_lower, re.IGNORECASE)
                    if match:
                        entities = self._extract_entities(message_lower, match)
                        return {
                            'intent': intent,
                            'confidence': 0.9,
                            'entities': entities,
                            'original_message': message,
                            'match': match.group(0) if match else None
                        }
                except Exception as e:
                    print(f"Error matching pattern {pattern}: {e}")
                    continue
        
        # No pattern matched - unknown intent
        return {
            'intent': 'unknown',
            'confidence': 0.0,
            'entities': {},
            'original_message': message
        }
    
    def _extract_entities(self, message: str, match) -> Dict:
        """Extract entities like station names from message"""
        entities = {}
        
        # Extract station names
        stations = self._extract_stations(message)
        if stations:
            entities['stations'] = stations
            if len(stations) >= 1:
                entities['origin'] = stations[0]
            if len(stations) >= 2:
                entities['destination'] = stations[1]
        
        # Extract profile name (from "save as Work")
        profile_match = re.search(r'save as (\w+)', message)
        if profile_match:
            entities['profile_name'] = profile_match.group(1)
        
        return entities
    
    def _extract_stations(self, message: str) -> List[str]:
        """Extract BART station abbreviations from message"""
        stations = []
        message_lower = message.lower()
        
        # Sort keywords by length (longest first) to match more specific names first
        sorted_keywords = sorted(self.STATION_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
        
        # Check for station keywords
        for keyword, abbr in sorted_keywords:
            if keyword in message_lower:
                if abbr not in stations:  # Avoid duplicates
                    stations.append(abbr)
                    # Remove matched keyword to avoid partial matches
                    message_lower = message_lower.replace(keyword, '')
        
        return stations
    
    def extract_station_from_text(self, text: str) -> Optional[str]:
        """
        Extract a single station abbreviation from text
        
        Args:
            text: Text that might contain a station name
            
        Returns:
            Station abbreviation or None
        """
        text_lower = text.lower()
        
        for keyword, abbr in self.STATION_KEYWORDS.items():
            if keyword in text_lower:
                return abbr
        
        return None
    
    def is_affirmative(self, message: str) -> bool:
        """Check if message is affirmative (yes, sure, etc.)"""
        affirmative_patterns = [
            r'^(yes|yeah|yep|yup|sure|ok|okay|alright|fine)',
            r'^y$',
            r'sounds good',
            r'let\'s do it'
        ]
        
        message_lower = message.lower().strip()
        
        for pattern in affirmative_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False
    
    def is_negative(self, message: str) -> bool:
        """Check if message is negative (no, nope, etc.)"""
        negative_patterns = [
            r'^(no|nope|nah|not really)',
            r'^n$',
            r'don\'t',
            r'cancel'
        ]
        
        message_lower = message.lower().strip()
        
        for pattern in negative_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False


# Singleton instance
message_parser = MessageParser()
