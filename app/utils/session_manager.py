"""
Session Manager
Tracks conversation state for each user
"""
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum


class ConversationState(Enum):
    """Conversation states"""
    IDLE = "idle"
    AWAITING_DESTINATION = "awaiting_destination"
    AWAITING_ORIGIN = "awaiting_origin"
    AWAITING_PROFILE_NAME = "awaiting_profile_name"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    IN_TRIP = "in_trip"


class UserSession:
    """Represents a user's conversation session"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.state = ConversationState.IDLE
        self.context = {}
        self.last_activity = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
    
    def set_state(self, state: ConversationState, context: Optional[Dict] = None):
        """
        Set conversation state
        
        Args:
            state: New state
            context: Additional context data
        """
        self.state = state
        if context:
            self.context.update(context)
        self.update_activity()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value"""
        return self.context.get(key, default)
    
    def set_context(self, key: str, value: Any):
        """Set context value"""
        self.context[key] = value
        self.update_activity()
    
    def clear_context(self):
        """Clear all context"""
        self.context = {}
    
    def reset(self):
        """Reset session to idle state"""
        self.state = ConversationState.IDLE
        self.context = {}
        self.update_activity()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired"""
        expiry_time = self.last_activity + timedelta(minutes=timeout_minutes)
        return datetime.utcnow() > expiry_time
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary"""
        return {
            'user_id': self.user_id,
            'state': self.state.value,
            'context': self.context,
            'last_activity': self.last_activity.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class SessionManager:
    """Manages user sessions in memory"""
    
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
    
    def get_session(self, user_id: str) -> UserSession:
        """
        Get or create session for user
        
        Args:
            user_id: User identifier (WhatsApp number)
            
        Returns:
            UserSession
        """
        # Clean up expired sessions first
        self._cleanup_expired_sessions()
        
        # Get or create session
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id)
        
        session = self.sessions[user_id]
        session.update_activity()
        return session
    
    def end_session(self, user_id: str):
        """End and remove a user's session"""
        if user_id in self.sessions:
            del self.sessions[user_id]
    
    def _cleanup_expired_sessions(self, timeout_minutes: int = 30):
        """Remove expired sessions"""
        expired_users = [
            user_id for user_id, session in self.sessions.items()
            if session.is_expired(timeout_minutes)
        ]
        
        for user_id in expired_users:
            del self.sessions[user_id]
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        self._cleanup_expired_sessions()
        return len(self.sessions)
    
    def get_all_sessions(self) -> Dict[str, UserSession]:
        """Get all active sessions"""
        self._cleanup_expired_sessions()
        return self.sessions.copy()


# Singleton instance
session_manager = SessionManager()
