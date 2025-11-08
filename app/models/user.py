"""
User Model
Stores user information and preferences
"""
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """User model for WhatsApp bot users"""
    
    __tablename__ = 'users'
    
    # Primary Key
    whatsapp_number = Column(String(20), primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Permissions
    location_permission = Column(Boolean, default=False)
    
    # Preferences (stored as JSON)
    alert_preferences = Column(JSON, default={
        'frequency': 'real-time',  # Options: 'real-time', 'major-only', 'scheduled', 'off'
        'quiet_mode': True,
        'weather_alerts': True,
        'delay_threshold_minutes': 10
    })
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    profiles = relationship('Profile', back_populates='user', cascade='all, delete-orphan')
    trips = relationship('Trip', back_populates='user', cascade='all, delete-orphan')
    patterns = relationship('Pattern', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(whatsapp_number='{self.whatsapp_number}', name='{self.name}')>"
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'whatsapp_number': self.whatsapp_number,
            'name': self.name,
            'location_permission': self.location_permission,
            'alert_preferences': self.alert_preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'is_active': self.is_active
        }
    
    def update_last_active(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
    
    def grant_location_permission(self):
        """Grant location tracking permission"""
        self.location_permission = True
    
    def revoke_location_permission(self):
        """Revoke location tracking permission"""
        self.location_permission = False
    
    def update_alert_preferences(self, preferences: dict):
        """Update alert preferences"""
        if self.alert_preferences is None:
            self.alert_preferences = {}
        self.alert_preferences.update(preferences)
