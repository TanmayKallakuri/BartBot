"""
BARTBot Main Handler
Core bot logic that processes messages and generates responses
"""
from typing import Dict, Optional, Tuple
from app.utils.message_parser import message_parser
from app.utils.response_builder import response_builder
from app.utils.session_manager import session_manager, ConversationState
from app.services.bart_service import bart_service
from app.services.station_location_service import station_location_service
from app.database import SessionLocal
from app.models import User, Profile, Trip, TripStatus, Pattern
from datetime import datetime


class BARTBot:
    """Main bot handler"""
    
    def __init__(self):
        self.parser = message_parser
        self.responses = response_builder
        self.sessions = session_manager
    
    def process_message(
        self,
        user_id: str,
        message: str,
        location: Optional[Tuple[float, float]] = None
    ) -> str:
        """
        Process incoming message and generate response
        
        Args:
            user_id: User's WhatsApp number
            message: User's message text
            location: Optional (latitude, longitude) tuple
            
        Returns:
            Bot's response message
        """
        # Get or create session
        session = self.sessions.get_session(user_id)
        
        # Get or create user in database
        user = self._get_or_create_user(user_id)
        
        # Handle location-only message (no text)
        if location and not message.strip():
            # User just shared location
            nearest = station_location_service.find_nearest_stations(location, limit=3)
            if nearest:
                return self.responses.nearest_stations(nearest)
            else:
                return "Got your location! \ud83d\udccd What can I help you with?"
        
        # Parse message
        parsed = self.parser.parse(message)
        intent = parsed['intent']
        entities = parsed.get('entities', {})
        
        # Debug logging
        print(f"\n[PARSE] Intent: {intent}")
        print(f"[PARSE] Entities: {entities}")
        print(f"[PARSE] Original: {message}")
        print(f"[PARSE] Location: {location}")
        
        # Handle based on current state and intent
        if session.state == ConversationState.AWAITING_DESTINATION:
            return self._handle_awaiting_destination(session, message, entities)
        
        elif session.state == ConversationState.AWAITING_PROFILE_NAME:
            return self._handle_awaiting_profile_name(session, message, user)
        
        elif session.state == ConversationState.AWAITING_CONFIRMATION:
            return self._handle_awaiting_confirmation(session, message)
        
        # Handle intents in idle state
        if intent == 'greeting':
            return self._handle_greeting(user)
        
        elif intent == 'help':
            return self.responses.help_message()
        
        elif intent == 'find_station':
            return self._handle_find_station(location)
        
        elif intent == 'get_departures':
            return self._handle_get_departures(entities, location)
        
        elif intent == 'plan_route':
            return self._handle_plan_route(session, entities, location)
        
        elif intent == 'start_trip':
            return self._handle_start_trip(session, user, location)
        
        elif intent == 'stop_trip':
            return self._handle_stop_trip(user)
        
        elif intent == 'create_profile':
            return self._handle_create_profile(session, user)
        
        elif intent == 'list_profiles':
            return self._handle_list_profiles(user)
        
        elif intent == 'status':
            return self._handle_status()
        
        else:
            return self.responses.unknown_command()
    
    def _get_or_create_user(self, whatsapp_number: str) -> User:
        """Get or create user in database"""
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(whatsapp_number=whatsapp_number).first()
            
            if not user:
                user = User(whatsapp_number=whatsapp_number)
                db.add(user)
                db.commit()
                db.refresh(user)
            else:
                user.update_last_active()
                db.commit()
            
            return user
        finally:
            db.close()
    
    def _handle_greeting(self, user: User) -> str:
        """Handle greeting"""
        return self.responses.greeting(user.name)
    
    def _handle_find_station(self, location: Optional[Tuple[float, float]]) -> str:
        """Handle find nearest station"""
        if not location:
            return self.responses.error_message("no_location")
        
        stations = station_location_service.find_nearest_stations(location, limit=3)
        return self.responses.nearest_stations(stations)
    
    def _handle_get_departures(
        self,
        entities: Dict,
        location: Optional[Tuple[float, float]]
    ) -> str:
        """Handle get departures request"""
        # Try to get station from entities
        station_abbr = entities.get('origin')
        
        if not station_abbr:
            # If no station specified, use nearest
            if not location:
                return self.responses.error_message("no_location")
            
            nearest = station_location_service.find_nearest_stations(location, limit=1)
            if not nearest:
                return self.responses.error_message("no_station")
            
            station_abbr = nearest[0]['abbr']
        
        # Get departures
        departures = bart_service.get_real_time_departures(station_abbr)
        station_info = bart_service.get_station_info(station_abbr)
        station_name = station_info.get('name', station_abbr) if station_info else station_abbr
        
        return self.responses.departures(station_name, departures)
    
    def _handle_plan_route(
        self,
        session,
        entities: Dict,
        location: Optional[Tuple[float, float]]
    ) -> str:
        """Handle route planning"""
        origin = entities.get('origin')
        destination = entities.get('destination')
        
        # If we have both, get route
        if origin and destination:
            try:
                trips = bart_service.get_route_schedule(origin, destination)
                if trips:
                    # Store in session for potential trip start
                    session.set_context('planned_route', {
                        'origin': origin,
                        'destination': destination,
                        'trip_info': trips[0]
                    })
                    return self.responses.route_info(trips)
                else:
                    return self.responses.error_message("no_station")
            except Exception as e:
                print(f"Error planning route: {e}")
                return self.responses.error_message("api_error")
        
        # If we only have destination, ask for origin or use location
        if destination and not origin:
            if location:
                # Use nearest station as origin
                try:
                    nearest = station_location_service.find_nearest_stations(location, limit=1)
                    if nearest:
                        origin = nearest[0]['abbr']
                        trips = bart_service.get_route_schedule(origin, destination)
                        if trips:
                            session.set_context('planned_route', {
                                'origin': origin,
                                'destination': destination,
                                'trip_info': trips[0]
                            })
                            return self.responses.route_info(trips)
                except Exception as e:
                    print(f"Error using location: {e}")
            
            # Ask for origin
            station_info = bart_service.get_station_info(destination)
            dest_name = station_info.get('name', destination) if station_info else destination
            session.set_state(ConversationState.AWAITING_ORIGIN)
            session.set_context('destination', destination)
            return f"Got it, heading to {dest_name}! Where are you starting from?"
        
        # Need destination
        session.set_state(ConversationState.AWAITING_DESTINATION)
        return "Sure! Where do you want to go? 🗺️"
    
    def _handle_awaiting_destination(self, session, message: str, entities: Dict) -> str:
        """Handle when waiting for destination"""
        destination = entities.get('destination') or self.parser.extract_station_from_text(message)
        
        if not destination:
            return "Hmm, couldn't find that station 🤔\n\nTry: 'Embarcadero', 'Berkeley', 'Montgomery'"
        
        # Get route
        origin = session.get_context('origin')
        if origin:
            trips = bart_service.get_route_schedule(origin, destination)
            session.reset()
            return self.responses.route_info(trips)
        
        # This shouldn't happen, but just in case
        session.reset()
        return "Something went wrong 😕 Try again!"
    
    def _handle_start_trip(
        self,
        session,
        user: User,
        location: Optional[Tuple[float, float]]
    ) -> str:
        """Handle start trip"""
        # Check if there's a planned route
        planned_route = session.get_context('planned_route')
        
        if not planned_route:
            return "Plan a route first!\n\nTry: 'Get me to Berkeley' then 'start trip'"
        
        # Create trip in database
        db = SessionLocal()
        try:
            trip_info = planned_route['trip_info']
            
            trip = Trip(
                user_whatsapp=user.whatsapp_number,
                start_station_abbr=planned_route['origin'],
                start_station_name=trip_info['origin'],
                end_station_abbr=planned_route['destination'],
                end_station_name=trip_info['destination'],
                expected_duration_minutes=int(trip_info['trip_time']),
                fare=trip_info['fare']
            )
            
            if location:
                trip.update_location(location[0], location[1])
            
            trip.start_trip()
            trip.enable_quiet_mode()
            
            db.add(trip)
            db.commit()
            
            # Update session
            session.set_state(ConversationState.IN_TRIP)
            session.set_context('active_trip_id', trip.id)
            
            return self.responses.trip_started(trip_info['destination'])
        
        finally:
            db.close()
    
    def _handle_stop_trip(self, user: User) -> str:
        """Handle stop trip"""
        db = SessionLocal()
        try:
            # Find active trip
            active_trip = db.query(Trip).filter_by(
                user_whatsapp=user.whatsapp_number,
                status=TripStatus.ACTIVE
            ).first()
            
            if active_trip:
                active_trip.complete_trip()
                db.commit()
                return self.responses.trip_stopped()
            else:
                return "You don't have an active trip 🤔"
        
        finally:
            db.close()
    
    def _handle_create_profile(self, session, user: User) -> str:
        """Handle create profile"""
        # Check if there's a completed trip or planned route
        planned_route = session.get_context('planned_route')
        
        if not planned_route:
            return "Take a trip first, then I can save it as a profile! 🚇"
        
        # Ask for profile name
        session.set_state(ConversationState.AWAITING_PROFILE_NAME)
        origin = planned_route['trip_info']['origin']
        dest = planned_route['trip_info']['destination']
        return f"Cool! What should I call this route?\n\n{origin} → {dest}\n\n(e.g., 'Work Commute', 'Weekend Trip')"
    
    def _handle_awaiting_profile_name(self, session, message: str, user: User) -> str:
        """Handle when waiting for profile name"""
        profile_name = message.strip()
        
        if len(profile_name) > 50:
            return "That name's too long! Keep it under 50 characters 😅"
        
        planned_route = session.get_context('planned_route')
        
        if not planned_route:
            session.reset()
            return "Something went wrong 😕 Try creating the profile again!"
        
        # Create profile
        db = SessionLocal()
        try:
            trip_info = planned_route['trip_info']
            
            profile = Profile(
                user_whatsapp=user.whatsapp_number,
                name=profile_name,
                start_station_abbr=planned_route['origin'],
                start_station_name=trip_info['origin'],
                end_station_abbr=planned_route['destination'],
                end_station_name=trip_info['destination']
            )
            
            db.add(profile)
            db.commit()
            
            route_str = f"{trip_info['origin']} → {trip_info['destination']}"
            
            session.reset()
            return self.responses.profile_saved(profile_name, route_str)
        
        finally:
            db.close()
    
    def _handle_awaiting_confirmation(self, session, message: str) -> str:
        """Handle when waiting for yes/no confirmation"""
        if self.parser.is_affirmative(message):
            # Handle whatever was being confirmed
            confirmation_type = session.get_context('confirmation_type')
            
            if confirmation_type == 'start_trip':
                # Start trip logic
                pass
            
            session.reset()
            return "✅ Done!"
        
        elif self.parser.is_negative(message):
            session.reset()
            return "No worries! Anything else I can help with?"
        
        else:
            return "Just say 'yes' or 'no' 😊"
    
    def _handle_list_profiles(self, user: User) -> str:
        """Handle list profiles"""
        db = SessionLocal()
        try:
            profiles = db.query(Profile).filter_by(
                user_whatsapp=user.whatsapp_number,
                is_active=True
            ).all()
            
            profiles_data = [p.to_dict() for p in profiles]
            return self.responses.profiles_list(profiles_data)
        
        finally:
            db.close()
    
    def _handle_status(self) -> str:
        """Handle BART status check"""
        advisories = bart_service.get_advisories()
        return self.responses.service_advisories(advisories)


# Singleton instance
bartbot = BARTBot()
