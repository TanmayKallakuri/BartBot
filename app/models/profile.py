"""
Profile Model
Stores saved routes/commute profiles like "Work Commute", "Weekend Trip"
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Profile(Base):
    """Profile model for saved routes"""
    
    __tablename__ = 'profiles'
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_whatsapp = Column(String(20), ForeignKey('users.whatsapp_number'), nullable=False)
    
    # Profile Info
    name = Column(String(100), nullable=False)  # e.g., "Work Commute", "Weekend SF Trip"
    description = Column(String(255), nullable=True)
    
    # Route Details
    start_station_abbr = Column(String(10), nullable=False)  # e.g., "EMBR"
    start_station_name = Column(String(100), nullable=False)  # e.g., "Embarcadero"
    end_station_abbr = Column(String(10), nullable=False)
    end_station_name = Column(String(100), nullable=False)
    
    # Alert Settings (can override user defaults)
    alert_settings = Column(JSON, default={
        'frequency': 'real-time',  # 'real-time', 'major-only', 'scheduled', 'off'
        'start_time': None,  # e.g., "09:00" for scheduled alerts
        'end_time': None,    # e.g., "18:00"
        'days_active': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],  # Days this profile is active
        'quiet_mode': True
    })
    
    # Usage Stats
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_favorite = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='profiles')
    trips = relationship('Trip', back_populates='profile')
    
    def __repr__(self):
        return f"<Profile(name='{self.name}', route='{self.start_station_abbr}→{self.end_station_abbr}')>"
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_station': {
                'abbr': self.start_station_abbr,
                'name': self.start_station_name
            },
            'end_station': {
                'abbr': self.end_station_abbr,
                'name': self.end_station_name
            },
            'alert_settings': self.alert_settings,
            'usage_count': self.usage_count,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'is_active': self.is_active,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def increment_usage(self):
        """Increment usage count and update last used"""
        self.usage_count += 1
        self.last_used = datetime.utcnow()
    
    def set_favorite(self):
        """Mark as favorite"""
        self.is_favorite = True
    
    def unset_favorite(self):
        """Unmark as favorite"""
        self.is_favorite = False
    
    def deactivate(self):
        """Deactivate profile"""
        self.is_active = False
    
    def activate(self):
        """Activate profile"""
        self.is_active = True
    
    def update_alert_settings(self, settings: dict):
        """Update alert settings"""
        if self.alert_settings is None:
            self.alert_settings = {}
        self.alert_settings.update(settings)
    
    def get_route_key(self):
        """Get unique route identifier for pattern matching"""
        return f"{self.start_station_abbr}→{self.end_station_abbr}"
