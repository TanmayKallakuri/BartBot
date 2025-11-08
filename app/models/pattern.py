"""
Pattern Model
Tracks user behavior patterns to suggest saved profiles
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Pattern(Base):
    """Pattern model for tracking repeated routes"""
    
    __tablename__ = 'patterns'
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_whatsapp = Column(String(20), ForeignKey('users.whatsapp_number'), nullable=False)
    
    # Route Information
    route_key = Column(String(50), nullable=False)  # e.g., "EMBR→DBRK"
    start_station_abbr = Column(String(10), nullable=False)
    start_station_name = Column(String(100), nullable=False)
    end_station_abbr = Column(String(10), nullable=False)
    end_station_name = Column(String(100), nullable=False)
    
    # Pattern Stats
    frequency_count = Column(Integer, default=1)  # How many times this route was taken
    first_occurrence = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_occurrence = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Time Patterns (stored as JSON for flexibility)
    time_patterns = Column(JSON, default={
        'weekdays': [],      # ['Mon', 'Tue', 'Wed'] - which days
        'times_of_day': [],  # ['09:00', '09:15', '09:30'] - departure times
        'avg_time': None     # '09:15' - average departure time
    })
    
    # Status
    profile_suggested = Column(Boolean, default=False)
    profile_created = Column(Boolean, default=False)
    profile_id = Column(Integer, nullable=True)  # If user created a profile from this pattern
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='patterns')
    
    def __repr__(self):
        return f"<Pattern(route='{self.route_key}', frequency={self.frequency_count})>"
    
    def to_dict(self):
        """Convert pattern to dictionary"""
        return {
            'id': self.id,
            'route_key': self.route_key,
            'start_station': {
                'abbr': self.start_station_abbr,
                'name': self.start_station_name
            },
            'end_station': {
                'abbr': self.end_station_abbr,
                'name': self.end_station_name
            },
            'frequency_count': self.frequency_count,
            'first_occurrence': self.first_occurrence.isoformat() if self.first_occurrence else None,
            'last_occurrence': self.last_occurrence.isoformat() if self.last_occurrence else None,
            'time_patterns': self.time_patterns,
            'profile_suggested': self.profile_suggested,
            'profile_created': self.profile_created,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def increment_frequency(self, timestamp: datetime = None):
        """Increment frequency and update last occurrence"""
        self.frequency_count += 1
        self.last_occurrence = timestamp or datetime.utcnow()
    
    def add_time_pattern(self, weekday: str, time_of_day: str):
        """Add time pattern data"""
        if self.time_patterns is None:
            self.time_patterns = {
                'weekdays': [],
                'times_of_day': [],
                'avg_time': None
            }
        
        # Add weekday if not already present
        if weekday not in self.time_patterns['weekdays']:
            self.time_patterns['weekdays'].append(weekday)
        
        # Add time of day
        self.time_patterns['times_of_day'].append(time_of_day)
        
        # Calculate average time (simplified - just use most common hour)
        times = self.time_patterns['times_of_day']
        if times:
            # Extract hours and find most common
            hours = [t.split(':')[0] for t in times]
            most_common_hour = max(set(hours), key=hours.count)
            self.time_patterns['avg_time'] = f"{most_common_hour}:00"
    
    def should_suggest_profile(self, threshold: int = 4) -> bool:
        """
        Check if pattern is strong enough to suggest creating a profile
        Default threshold: 4 occurrences
        """
        return (
            self.frequency_count >= threshold and 
            not self.profile_suggested and 
            not self.profile_created
        )
    
    def mark_suggested(self):
        """Mark that profile has been suggested to user"""
        self.profile_suggested = True
    
    def mark_profile_created(self, profile_id: int):
        """Mark that user created a profile from this pattern"""
        self.profile_created = True
        self.profile_id = profile_id
    
    def get_pattern_summary(self) -> str:
        """Get human-readable summary of the pattern"""
        days = ', '.join(self.time_patterns.get('weekdays', []))
        avg_time = self.time_patterns.get('avg_time', 'various times')
        
        return (
            f"You've taken {self.start_station_name} → {self.end_station_name} "
            f"{self.frequency_count} times"
            f"{f' on {days}' if days else ''}"
            f"{f' around {avg_time}' if avg_time != 'various times' else ''}"
        )
