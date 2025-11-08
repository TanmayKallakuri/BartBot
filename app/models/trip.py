"""
Trip Model
Tracks active and completed trips for real-time monitoring and "get off" alerts
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class TripStatus(enum.Enum):
    """Trip status enumeration"""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    """Trip model for tracking journeys"""
    
    __tablename__ = 'trips'
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_whatsapp = Column(String(20), ForeignKey('users.whatsapp_number'), nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=True)  # Optional if using saved profile
    
    # Trip Details
    start_station_abbr = Column(String(10), nullable=False)
    start_station_name = Column(String(100), nullable=False)
    end_station_abbr = Column(String(10), nullable=False)
    end_station_name = Column(String(100), nullable=False)
    
    # Status
    status = Column(Enum(TripStatus), default=TripStatus.PLANNED, nullable=False)
    
    # Location Tracking
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    last_location_update = Column(DateTime, nullable=True)
    
    # Location checkpoints (for "get off" alerts)
    location_history = Column(JSON, default=[])  # List of {lat, lng, timestamp, station_nearby}
    
    # Trip Timing
    planned_departure = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    estimated_arrival = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)
    
    # Trip Details from BART API
    expected_duration_minutes = Column(Integer, nullable=True)
    fare = Column(String(10), nullable=True)  # e.g., "$4.70"
    
    # Alerts
    alerts_sent = Column(JSON, default=[])  # List of {type, message, timestamp}
    quiet_mode_active = Column(Boolean, default=False)
    get_off_alert_sent = Column(Boolean, default=False)
    
    # Delays/Issues
    delays_encountered = Column(JSON, default=[])  # List of {type, duration, timestamp}
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='trips')
    profile = relationship('Profile', back_populates='trips')
    
    def __repr__(self):
        return f"<Trip(id={self.id}, route='{self.start_station_abbr}→{self.end_station_abbr}', status='{self.status.value}')>"
    
    def to_dict(self):
        """Convert trip to dictionary"""
        return {
            'id': self.id,
            'start_station': {
                'abbr': self.start_station_abbr,
                'name': self.start_station_name
            },
            'end_station': {
                'abbr': self.end_station_abbr,
                'name': self.end_station_name
            },
            'status': self.status.value,
            'current_location': {
                'latitude': self.current_latitude,
                'longitude': self.current_longitude,
                'last_update': self.last_location_update.isoformat() if self.last_location_update else None
            },
            'planned_departure': self.planned_departure.isoformat() if self.planned_departure else None,
            'actual_departure': self.actual_departure.isoformat() if self.actual_departure else None,
            'estimated_arrival': self.estimated_arrival.isoformat() if self.estimated_arrival else None,
            'expected_duration_minutes': self.expected_duration_minutes,
            'fare': self.fare,
            'quiet_mode_active': self.quiet_mode_active,
            'alerts_sent': self.alerts_sent,
            'delays_encountered': self.delays_encountered,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def start_trip(self):
        """Start the trip"""
        self.status = TripStatus.ACTIVE
        self.actual_departure = datetime.utcnow()
    
    def complete_trip(self):
        """Complete the trip"""
        self.status = TripStatus.COMPLETED
        self.actual_arrival = datetime.utcnow()
        self.completed_at = datetime.utcnow()
    
    def cancel_trip(self):
        """Cancel the trip"""
        self.status = TripStatus.CANCELLED
        self.completed_at = datetime.utcnow()
    
    def update_location(self, latitude: float, longitude: float):
        """Update current location"""
        self.current_latitude = latitude
        self.current_longitude = longitude
        self.last_location_update = datetime.utcnow()
        
        # Add to location history
        if self.location_history is None:
            self.location_history = []
        
        self.location_history.append({
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def add_alert(self, alert_type: str, message: str):
        """Add alert to history"""
        if self.alerts_sent is None:
            self.alerts_sent = []
        
        self.alerts_sent.append({
            'type': alert_type,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def add_delay(self, delay_type: str, duration_minutes: int):
        """Record a delay"""
        if self.delays_encountered is None:
            self.delays_encountered = []
        
        self.delays_encountered.append({
            'type': delay_type,
            'duration_minutes': duration_minutes,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def enable_quiet_mode(self):
        """Enable quiet mode"""
        self.quiet_mode_active = True
    
    def disable_quiet_mode(self):
        """Disable quiet mode"""
        self.quiet_mode_active = False
    
    def mark_get_off_alert_sent(self):
        """Mark that get off alert has been sent"""
        self.get_off_alert_sent = True
    
    def is_active(self) -> bool:
        """Check if trip is currently active"""
        return self.status == TripStatus.ACTIVE
    
    def get_route_key(self):
        """Get unique route identifier"""
        return f"{self.start_station_abbr}→{self.end_station_abbr}"
