"""
Test script for database models
Tests creating, reading, updating, and deleting data
"""
from app.database import SessionLocal, init_db
from app.models import User, Profile, Trip, TripStatus, Pattern
from datetime import datetime, timedelta


def test_database():
    print("🧪 Testing Database Models\n")
    print("=" * 50)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Test 1: Create a User
        print("\nTEST 1: Creating a user")
        print("-" * 50)
        
        user = User(
            whatsapp_number="+14155551234",
            name="Phoenix Test User",
            location_permission=True
        )
        db.add(user)
        db.commit()
        print(f"✅ Created user: {user}")
        print(f"   User dict: {user.to_dict()}")
        
        # Test 2: Create a Profile for the User
        print("\nTEST 2: Creating a saved route profile")
        print("-" * 50)
        
        profile = Profile(
            user_whatsapp=user.whatsapp_number,
            name="Work Commute",
            description="Daily commute to work",
            start_station_abbr="EMBR",
            start_station_name="Embarcadero",
            end_station_abbr="DBRK",
            end_station_name="Downtown Berkeley"
        )
        db.add(profile)
        db.commit()
        print(f"✅ Created profile: {profile}")
        print(f"   Profile dict: {profile.to_dict()}")
        
        # Test 3: Create a Trip
        print("\nTEST 3: Creating an active trip")
        print("-" * 50)
        
        trip = Trip(
            user_whatsapp=user.whatsapp_number,
            profile_id=profile.id,
            start_station_abbr="EMBR",
            start_station_name="Embarcadero",
            end_station_abbr="DBRK",
            end_station_name="Downtown Berkeley",
            expected_duration_minutes=25,
            fare="$4.70"
        )
        trip.start_trip()
        trip.update_location(37.7955, -122.3933)  # Embarcadero coords
        db.add(trip)
        db.commit()
        print(f"✅ Created trip: {trip}")
        print(f"   Trip status: {trip.status.value}")
        print(f"   Trip dict: {trip.to_dict()}")
        
        # Test 4: Create a Pattern
        print("\nTEST 4: Creating a usage pattern")
        print("-" * 50)
        
        pattern = Pattern(
            user_whatsapp=user.whatsapp_number,
            route_key="EMBR→DBRK",
            start_station_abbr="EMBR",
            start_station_name="Embarcadero",
            end_station_abbr="DBRK",
            end_station_name="Downtown Berkeley",
            frequency_count=1
        )
        pattern.add_time_pattern("Mon", "09:15")
        db.add(pattern)
        db.commit()
        print(f"✅ Created pattern: {pattern}")
        print(f"   Pattern dict: {pattern.to_dict()}")
        
        # Test 5: Update Pattern (simulate repeated usage)
        print("\nTEST 5: Simulating repeated route usage")
        print("-" * 50)
        
        for i in range(3):
            pattern.increment_frequency()
            pattern.add_time_pattern("Tue", "09:20")
        
        db.commit()
        print(f"✅ Updated pattern frequency: {pattern.frequency_count} times")
        print(f"   Should suggest profile? {pattern.should_suggest_profile()}")
        print(f"   Pattern summary: {pattern.get_pattern_summary()}")
        
        # Test 6: Query Data
        print("\nTEST 6: Querying data")
        print("-" * 50)
        
        # Get all users
        all_users = db.query(User).all()
        print(f"✅ Found {len(all_users)} users")
        
        # Get user's profiles
        user_profiles = db.query(Profile).filter_by(user_whatsapp=user.whatsapp_number).all()
        print(f"✅ User has {len(user_profiles)} saved profiles")
        
        # Get active trips
        active_trips = db.query(Trip).filter_by(status=TripStatus.ACTIVE).all()
        print(f"✅ Found {len(active_trips)} active trips")
        
        # Get patterns for suggestion
        patterns_to_suggest = db.query(Pattern).filter(
            Pattern.frequency_count >= 4,
            Pattern.profile_suggested == False
        ).all()
        print(f"✅ Found {len(patterns_to_suggest)} patterns ready for profile suggestion")
        
        # Test 7: Update Operations
        print("\nTEST 7: Update operations")
        print("-" * 50)
        
        # Mark profile as favorite
        profile.set_favorite()
        profile.increment_usage()
        db.commit()
        print(f"✅ Profile marked as favorite, usage count: {profile.usage_count}")
        
        # Complete the trip
        trip.add_alert("approaching_station", "Downtown Berkeley is next!")
        trip.mark_get_off_alert_sent()
        trip.complete_trip()
        db.commit()
        print(f"✅ Trip completed, status: {trip.status.value}")
        print(f"   Alerts sent: {len(trip.alerts_sent)}")
        
        # Test 8: Relationships
        print("\nTEST 8: Testing relationships")
        print("-" * 50)
        
        # Access user's profiles through relationship
        user_from_db = db.query(User).filter_by(whatsapp_number=user.whatsapp_number).first()
        print(f"✅ User has {len(user_from_db.profiles)} profiles")
        print(f"✅ User has {len(user_from_db.trips)} trips")
        print(f"✅ User has {len(user_from_db.patterns)} patterns")
        
        # Test 9: Cleanup (optional)
        print("\nTEST 9: Cleanup test data")
        print("-" * 50)
        
        cleanup = input("Delete test data? (y/n): ")
        if cleanup.lower() == 'y':
            db.delete(trip)
            db.delete(pattern)
            db.delete(profile)
            db.delete(user)
            db.commit()
            print("✅ Test data deleted")
        else:
            print("✅ Test data kept in database")
        
        print("\n" + "=" * 50)
        print("🎉 All database tests passed!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Make sure database is initialized
    print("Initializing database if needed...")
    init_db()
    print()
    
    # Run tests
    test_database()
