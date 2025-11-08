"""
Bot Response Builder
Creates conversational, friendly responses
"""
from typing import Dict, List, Optional
from datetime import datetime


class ResponseBuilder:
    """Build conversational bot responses"""
    
    def greeting(self, user_name: Optional[str] = None) -> str:
        """Greeting message"""
        name_part = f" {user_name}" if user_name else ""
        
        greetings = [
            f"Hey{name_part}! 🤙 What's up?",
            f"Yo{name_part}! Where you headed?",
            f"Hey{name_part}! Need help with BART?",
            f"What's good{name_part}? 🚇"
        ]
        
        import random
        return random.choice(greetings)
    
    def help_message(self) -> str:
        """Help message with commands"""
        return """**Hey! I'm BARTBot, your transit buddy 🚇**

Here's what I can do:

📍 **Find Stations**
"Where's the nearest station?"
"Find a bus stop near me"
"Nearest transit hub"

🚶 **Get Directions**
"How do I get there?"
"Show me directions"
"Guide me to the station"

🚆 **Get Train Times**
"Next train from Embarcadero"
"When's the next train?"

🗺️ **Plan Routes**
"Get me to Berkeley"
"Embarcadero to Montgomery"

🚦 **Trip Mode**
"Start trip" - I'll track you and send alerts
"Stop trip" - End your journey

💾 **Save Routes**
"Save this route"
"My profiles"

⚠️ **Check Status**
"Any delays?"
"BART status"

Just talk to me naturally - I'll figure it out! 😎

💡 Tip: Share your location for personalized directions!"""
    
    def unknown_command(self, message: str = "") -> str:
        """Response when don't understand, with smart suggestions based on keywords"""
        message_lower = message.lower()

        # Provide contextual suggestions based on keywords in message
        suggestions = []

        # Check for station-related keywords
        if any(word in message_lower for word in ['station', 'where', 'location', 'find', 'near']):
            suggestions.append("- 'Where's the nearest station?'")
            suggestions.append("- 'Find a station near me'")

        # Check for route/travel keywords
        if any(word in message_lower for word in ['travel', 'commute', 'journey', 'ride', 'transport']):
            suggestions.append("- 'Get me to [station name]'")
            suggestions.append("- 'How do I get to Berkeley?'")

        # Check for time/schedule keywords
        if any(word in message_lower for word in ['time', 'schedule', 'when', 'departure', 'arrival']):
            suggestions.append("- 'Next train from Embarcadero'")
            suggestions.append("- 'When do trains leave?'")

        # Check for delay/status keywords
        if any(word in message_lower for word in ['late', 'delay', 'slow', 'problem', 'issue', 'wrong']):
            suggestions.append("- 'Any delays?'")
            suggestions.append("- 'BART status'")

        # If no specific keywords, provide general suggestions
        if not suggestions:
            suggestions = [
                "- 'Where's the nearest station?'",
                "- 'Get me to [station name]'",
                "- 'Next train from [station]'",
                "- 'Any delays?'"
            ]

        suggestions_text = "\n".join(suggestions[:4])  # Limit to 4 suggestions

        return f"""Hmm, not sure what you mean 🤔

Try asking like:
{suggestions_text}

Or just say "help" for all commands!"""
    
    def nearest_stations(self, stations: List[Dict]) -> str:
        """Format nearest stations message"""
        if not stations:
            return "❌ No BART stations found nearby"
        
        message = "📍 **Nearest BART Stations:**\n\n"
        
        for i, station in enumerate(stations[:3], 1):
            distance = station['distance']
            dist_str = f"{distance['distance_km']} km" if distance['distance_km'] >= 1 else f"{int(distance['distance_meters'])} meters"
            walk_time = station['walking_time_minutes']
            
            message += f"**{i}. {station['name']}**\n"
            message += f"   📏 {dist_str} away (~{walk_time} min walk)\n"
            message += f"   📮 {station['address']}\n\n"
        
        return message
    
    def departures(self, station_name: str, trains: List[Dict]) -> str:
        """Format departure times"""
        if not trains:
            return f"No trains scheduled from {station_name} right now 😕"
        
        message = f"🚇 **Next trains from {station_name}:**\n\n"
        
        for train in trains[:5]:
            minutes = train['minutes']
            if minutes == 'Leaving':
                time_str = "🔥 **LEAVING NOW**"
            else:
                time_str = f"⏱️ {minutes} min"
            
            bike_flag = " 🚴" if train.get('bikeflag') else ""
            
            message += f"{time_str} → **{train['destination']}**{bike_flag}\n"
            message += f"   Platform {train['platform']} | {train['length']} cars\n\n"
        
        return message
    
    def route_info(self, trips: List[Dict]) -> str:
        """Format route information"""
        if not trips:
            return "Couldn't find a route for that 😕"
        
        trip = trips[0]  # Show first option
        
        message = "🗺️ **Route Info:**\n\n"
        message += f"🚇 {trip['origin']} → {trip['destination']}\n"
        message += f"⏱️ **{trip['trip_time']} minutes**\n"
        message += f"💵 Fare: **${trip['fare']}**\n"
        message += f"🕐 Departs: {trip['orig_time']}\n"
        message += f"🕐 Arrives: {trip['dest_time']}\n\n"
        message += "Wanna start trip mode? I'll keep you posted! 🤙"
        
        return message
    
    def trip_started(self, destination: str) -> str:
        """Trip start confirmation"""
        return f"""✅ **Trip started!**

📍 Heading to: **{destination}**

I got you covered. I'll chill now unless something important comes up 🤙

I'll let you know when you're almost there!"""
    
    def trip_stopped(self) -> str:
        """Trip stop confirmation"""
        return "✅ Trip ended. Made it! Need anything else? 🎉"
    
    def approaching_destination(self, station_name: str) -> str:
        """Alert when approaching destination"""
        return f"""🔔 **Heads up!**

Your stop ({station_name}) is next!

Get ready! 🚇"""
    
    def get_off_alert(self, station_name: str) -> str:
        """Urgent get off alert"""
        return f"""🚨 **THIS IS YOUR STOP!**

Get off now at **{station_name}**! 🚇"""
    
    def delay_alert(self, delay_minutes: int) -> str:
        """Delay notification"""
        return f"""⚠️ **Heads up!**

There's a **{delay_minutes} min delay** on your route.

Want me to find you another way?"""
    
    def profile_saved(self, profile_name: str, route: str) -> str:
        """Profile creation confirmation"""
        return f"""✅ **Profile saved!**

**"{profile_name}"**
Route: {route}

I'll remember this for next time! 💾"""
    
    def profile_suggestion(self, route: str, frequency: int) -> str:
        """Suggest creating a profile"""
        return f"""💡 **Yo!**

I've noticed you take **{route}** like {frequency} times now.

Want to save this as a profile? Makes life easier 😎

Just say "save this route" or give it a name!"""
    
    def profiles_list(self, profiles: List[Dict]) -> str:
        """List user's saved profiles"""
        if not profiles:
            return "You don't have any saved routes yet!\n\nTake a route a few times and I'll suggest saving it 💡"
        
        message = "💾 **Your Saved Routes:**\n\n"
        
        for i, profile in enumerate(profiles, 1):
            fav = " ⭐" if profile.get('is_favorite') else ""
            usage = profile.get('usage_count', 0)
            
            message += f"**{i}. {profile['name']}{fav}**\n"
            message += f"   {profile['start_station']['name']} → {profile['end_station']['name']}\n"
            message += f"   Used {usage} times\n\n"
        
        return message
    
    def service_advisories(self, advisories: List[Dict]) -> str:
        """Format service advisories"""
        if not advisories:
            return "✅ No delays or issues! Smooth sailing 🚇✨"
        
        message = "⚠️ **Service Advisories:**\n\n"
        
        for adv in advisories[:3]:
            station = adv.get('station', 'System-wide')
            adv_type = adv.get('type', 'INFO')
            description = adv.get('description', '')
            
            message += f"**{station}** - {adv_type}\n"
            if description:
                # Truncate long descriptions
                desc_short = description[:100] + "..." if len(description) > 100 else description
                message += f"{desc_short}\n\n"
        
        return message
    
    def location_permission_request(self) -> str:
        """Request location permission"""
        return """📍 **Quick heads up!**

I need location access to:
- Find nearest stations
- Track your trip
- Send "get off" alerts

Your location stays private - I don't share it with anyone.

Cool? 🤙"""
    
    def error_message(self, error_type: str = "general") -> str:
        """Error messages"""
        errors = {
            "general": "Oops, something went wrong 😕\n\nTry again or say 'help' for commands",
            "no_location": """📍 **I need your location for that!**

Tap the **+** button in WhatsApp and select **Location** to share where you are.

Or just tell me which station you're at!""",
            "no_station": "Couldn't find that station 🤔\n\nTry: 'Embarcadero', 'Berkeley', 'Montgomery', 'Civic Center'",
            "api_error": "BART API is acting up 😕\n\nGive it a sec and try again"
        }

        return errors.get(error_type, errors["general"])

    def walking_directions(self, destination_name: str, directions: Dict) -> str:
        """Format walking directions"""
        import re

        if not directions:
            return "Couldn't get directions 😕"

        message = f"🚶 **Walking to {destination_name}**\n\n"

        # Add summary
        duration = directions.get('duration_minutes', 0)
        distance_info = directions.get('distance', {})
        distance_km = distance_info.get('distance_km', 0)

        if distance_km >= 1:
            dist_str = f"{distance_km} km"
        else:
            dist_str = f"{int(distance_info.get('distance_meters', 0))} meters"

        message += f"⏱️ {duration} min ({dist_str})\n\n"

        # Add turn-by-turn steps
        steps = directions.get('steps', [])
        if steps:
            message += "**Directions:**\n"
            for i, step in enumerate(steps[:8], 1):  # Limit to 8 steps to avoid huge messages
                # Clean HTML tags from instructions
                instruction = re.sub(r'<[^>]+>', '', step.get('instruction', ''))
                message += f"{i}. {instruction} ({step.get('distance', '')})\n"

            if len(steps) > 8:
                message += f"\n...and {len(steps) - 8} more steps\n"

        # Note if using estimation
        if directions.get('note'):
            message += f"\n💡 {directions['note']}"

        return message

    def transit_directions(self, destination_name: str, directions: Dict) -> str:
        """Format transit directions with bus/train info"""
        import re

        if not directions:
            return "Couldn't get transit directions 😕"

        message = f"🚇 **Transit to {destination_name}**\n\n"

        # Add summary
        duration = directions.get('duration_minutes', 0)
        distance_info = directions.get('distance', {})
        distance_km = distance_info.get('distance_km', 0)

        if distance_km >= 1:
            dist_str = f"{distance_km} km"
        else:
            dist_str = f"{int(distance_info.get('distance_meters', 0))} meters"

        message += f"⏱️ {duration} min ({dist_str})\n"

        # Add departure/arrival times if available
        if directions.get('departure_time'):
            message += f"🕐 Leave: {directions['departure_time']}\n"
        if directions.get('arrival_time'):
            message += f"🕐 Arrive: {directions['arrival_time']}\n"

        message += "\n**Route:**\n"

        # Add transit details
        transit_details = directions.get('transit_details', [])
        if transit_details:
            for i, transit in enumerate(transit_details, 1):
                transit_type = transit.get('type', 'Transit')
                line_name = transit.get('line_short_name', '') or transit.get('line_name', '')

                # Use emoji based on type
                emoji = "🚌" if transit_type == "BUS" else "🚇"

                message += f"\n{emoji} **{line_name}** - {transit.get('headsign', '')}\n"
                message += f"   Board: {transit.get('departure_stop', '')}\n"
                message += f"   Exit: {transit.get('arrival_stop', '')} ({transit.get('num_stops', 0)} stops)\n"
        else:
            # Show steps without transit details
            steps = directions.get('steps', [])
            for i, step in enumerate(steps[:6], 1):
                instruction = re.sub(r'<[^>]+>', '', step.get('instruction', ''))
                travel_mode = step.get('travel_mode', '')

                # Add emoji based on travel mode
                if travel_mode == 'WALKING':
                    emoji = "🚶"
                elif travel_mode == 'TRANSIT':
                    emoji = "🚇"
                else:
                    emoji = "➡️"

                message += f"{i}. {emoji} {instruction}\n"

        # Note if using estimation
        if directions.get('note'):
            message += f"\n💡 {directions['note']}"

        return message

    def nearby_bus_stops(self, stops: List[Dict]) -> str:
        """Format nearby bus stops"""
        if not stops:
            return "❌ No bus stops found nearby"

        message = "🚌 **Nearby Bus Stops:**\n\n"

        for i, stop in enumerate(stops[:5], 1):  # Show top 5
            distance = stop['distance']
            if distance['distance_km'] >= 1:
                dist_str = f"{distance['distance_km']} km"
            else:
                dist_str = f"{int(distance['distance_meters'])} meters"

            message += f"**{i}. {stop['name']}**\n"
            message += f"   📏 {dist_str} away\n"
            if stop.get('address'):
                message += f"   📮 {stop['address']}\n"
            message += "\n"

        return message

    def nearby_transit_hubs(self, hubs: List[Dict]) -> str:
        """Format nearby transit hubs"""
        if not hubs:
            return "❌ No transit hubs found nearby"

        message = "🚇 **Nearby Transit Hubs:**\n\n"

        for i, hub in enumerate(hubs[:5], 1):  # Show top 5
            distance = hub['distance']
            if distance['distance_km'] >= 1:
                dist_str = f"{distance['distance_km']} km"
            else:
                dist_str = f"{int(distance['distance_meters'])} meters"

            # Choose emoji based on type
            hub_type = hub.get('type', '').lower()
            if 'bus' in hub_type:
                emoji = "🚌"
            elif 'subway' in hub_type or 'train' in hub_type:
                emoji = "🚇"
            else:
                emoji = "🚏"

            message += f"**{i}. {emoji} {hub['name']}**\n"
            message += f"   Type: {hub.get('type', 'Transit Hub')}\n"
            message += f"   📏 {dist_str} away\n"
            if hub.get('address'):
                message += f"   📮 {hub['address']}\n"
            message += "\n"

        return message


# Singleton instance
response_builder = ResponseBuilder()
