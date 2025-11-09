"""
Message Parser
Understands user messages and extracts intent and entities
Hybrid approach: Regex patterns + AI fallback for complex messages
"""
import re
import json
from typing import Dict, Optional, List
from datetime import datetime
from config import Config

# Try to import OpenAI, but make it optional
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MessageParser:
    """Parse user messages to understand intent"""

    def __init__(self):
        """Initialize the message parser with optional AI support"""
        self.openai_client = None
        self.use_ai = False

        # Initialize OpenAI client if available and configured
        if OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.use_ai = True
                print("✓ AI-powered understanding enabled (OpenAI)")
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
                self.use_ai = False
        else:
            print("ℹ️  Using regex-only mode (OpenAI not configured)")

    # Command patterns
    PATTERNS = {
        'greeting': [
            r'^(hi|hello|hey|yo|sup|what\'s up|whats up)',
            r'^good (morning|afternoon|evening)',
            r'^(hey|hi) there',
            r'^howdy',
            r'^greetings'
        ],
        'find_station': [
            r'(nearest|closest|near me) (station|bart)',
            r'where.*station',
            r'find.*station',
            r'(is there|where\'s|wheres) a (station|bart)',
            r'station (near|close)',
            r'where can i (catch|get|find) (bart|train)',
            r'bart near me',
            r'closest bart'
        ],
        'get_departures': [
            r'(when|what time).*train',
            r'next train',
            r'train.*time',
            r'departures?.*from',
            r'when.*leaving',
            r'(show|get|give).*train.*schedule',
            r'train schedule',
            r'is there a train',
            r'(any|are there) trains',
            r'how long (until|till) (the )?next train',
            r'when (does|do) trains (leave|depart)',
            r'what trains are coming',
            r'upcoming trains',
            r'train times'
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
            r'need to get to',
            r'i (need|want) to (go|get) to',
            r'can you (help|take) me (to|get to)',
            r'trying to (get|go) to',
            r'(i\'m|im) (headed|heading|going) to',
            r'help me (get|go) to',
            r'directions? to',
            r'how (can i|do i) (reach|get to)',
            r'i (wanna|want to) (visit|go to|get to)',
            r'take.*to',
            r'bring me to'
        ],
        'start_trip': [
            r'start trip',
            r'begin trip',
            r'trip mode',
            r'let\'s go',
            r'im ready',
            r'i\'m ready',
            r'track me',
            r'track my trip',
            r'start tracking'
        ],
        'stop_trip': [
            r'stop trip',
            r'end trip',
            r'cancel trip',
            r'i\'m here',
            r'im here',
            r'arrived',
            r'stop tracking',
            r'end tracking',
            r'made it',
            r'i arrived'
        ],
        'create_profile': [
            r'save (this )?route',
            r'create profile',
            r'save as (\w+)',
            r'make.*profile',
            r'remember this',
            r'save (this|it)'
        ],
        'list_profiles': [
            r'(show|list|my) profile',
            r'saved routes',
            r'my routes',
            r'what (routes|profiles) do i have',
            r'(show|display) my (saved|) routes'
        ],
        'help': [
            r'^help',
            r'what can you do',
            r'commands',
            r'how.*work',
            r'what (do you|can you) do',
            r'(can you )?help me',
            r'i need help',
            r'show.*commands',
            r'how (do i|can i) use',
            r'what are.*options',
            r'i\'m lost',
            r'im lost',
            r'i don\'t know'
        ],
        'status': [
            r'(any )?delays',
            r'service.*status',
            r'bart.*status',
            r'problems',
            r'issues',
            r'is bart (running|working|ok)',
            r'(any|are there) (problems|issues)',
            r'service.*ok',
            r'everything (ok|okay|working)',
            r'status',
            r'is everything (running|working)'
        ],
        'get_directions': [
            r'(how do i|how can i) (get|walk|reach) (to|there)',
            r'(show|give|get)( me)? directions',
            r'navigate( me| to)?',
            r'guide me( there| to the)',
            r'(walking|turn.by.turn) directions',
            r'take me there',
            r'how to (walk|get) there',
            r'(what\'s|whats) the way',
            r'which way',
            r'direct me'
        ],
        'find_bus_stop': [
            r'(bus stop|bus station)',
            r'(nearest|closest|where.*) bus',
            r'find.*bus',
            r'where can i (catch|take|get) (a |the )?bus',
            r'bus near me',
            r'is there a bus'
        ],
        'find_transit': [
            r'(nearest|closest) (transit|public transport)',
            r'transit (hub|station|center)',
            r'public transport',
            r'where.*transit',
            r'find transit'
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
    
    def _parse_with_ai(self, message: str) -> Optional[Dict]:
        """
        Use OpenAI to parse complex messages that don't match regex patterns

        Args:
            message: User's message text

        Returns:
            Parsed result dict or None if AI is unavailable
        """
        if not self.use_ai or not self.openai_client:
            return None

        try:
            # Build the prompt for OpenAI
            system_prompt = """You are a BART (Bay Area Rapid Transit) bot assistant. Parse user messages to extract:
1. intent: One of [greeting, find_station, get_departures, plan_route, start_trip, stop_trip, create_profile, list_profiles, help, status, get_directions, find_bus_stop, find_transit, unknown]
2. entities: Extract station names, preferences, etc.
3. confidence: 0.0 to 1.0

Respond ONLY with valid JSON in this exact format:
{
  "intent": "intent_name",
  "confidence": 0.95,
  "entities": {
    "origin": "EMBR",
    "destination": "DBRK"
  }
}

BART stations include: Embarcadero (EMBR), Montgomery (MONT), Powell (POWL), Berkeley (DBRK), North Berkeley (NBRK), SFO Airport (SFIA), etc.
Handle typos, slang, and natural language. Extract station names even with spelling errors."""

            user_prompt = f"Parse this message: {message}"

            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            # Extract and parse the response
            content = response.choices[0].message.content.strip()

            # Parse JSON response
            result = json.loads(content)

            # Add original message
            result['original_message'] = message
            result['ai_parsed'] = True

            print(f"[AI] Parsed '{message}' → {result['intent']} (confidence: {result['confidence']})")

            return result

        except json.JSONDecodeError as e:
            print(f"[AI] JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"[AI] Error: {e}")
            return None

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
        
        # No pattern matched - try AI parsing if available
        if self.use_ai:
            ai_result = self._parse_with_ai(message)
            if ai_result:
                return ai_result

        # No pattern matched and AI unavailable or failed
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
