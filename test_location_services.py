"""
Test script for Location Services
Tests GPS calculations, nearest stations, and walking directions
"""
from app.services.location_service import location_service
from app.services.station_location_service import station_location_service


def test_location_services():
    print("🗺️  Testing Location Services\n")
    print("=" * 50)
    
    # Test locations
    # Downtown SF (near Powell St station)
    downtown_sf = (37.7849, -122.4094)
    
    # Embarcadero Station
    embarcadero = (37.7955, -122.3933)
    
    # Downtown Berkeley
    downtown_berkeley = (37.8700, -122.2680)
    
    # Test 1: Calculate distance between two points
    print("\nTEST 1: Calculate distance")
    print("-" * 50)
    distance = location_service.calculate_distance(downtown_sf, embarcadero)
    print(f"✅ Distance from Downtown SF to Embarcadero:")
    print(f"   {distance['distance_km']} km")
    print(f"   {distance['distance_meters']} meters")
    print(f"   {distance['distance_miles']} miles")
    
    # Test 2: Check if near location
    print("\nTEST 2: Check proximity")
    print("-" * 50)
    is_near = location_service.is_near_location(
        downtown_sf,
        embarcadero,
        threshold_meters=1000
    )
    print(f"✅ Is Downtown SF near Embarcadero (within 1km)? {is_near}")
    
    # Test 3: Estimate walking time
    print("\nTEST 3: Estimate walking time")
    print("-" * 50)
    walk_time = location_service.estimate_walking_time(distance['distance_km'])
    print(f"✅ Estimated walking time: {walk_time} minutes")
    
    # Test 4: Find nearest BART stations
    print("\nTEST 4: Find nearest BART stations")
    print("-" * 50)
    print(f"Finding stations near Downtown SF...")
    nearest_stations = station_location_service.find_nearest_stations(
        downtown_sf,
        limit=5
    )
    
    if nearest_stations:
        print(f"✅ Found {len(nearest_stations)} nearest stations:\n")
        for i, station in enumerate(nearest_stations, 1):
            dist = location_service.format_distance_message(station['distance'])
            walk = station['walking_time_minutes']
            print(f"{i}. {station['name']}")
            print(f"   Distance: {dist} (~{walk} min walk)")
            print(f"   Address: {station['address']}\n")
    
    # Test 5: Format message for user
    print("=" * 50)
    print("TEST 5: Formatted message for user")
    print("=" * 50)
    message = station_location_service.format_nearest_stations_message(
        downtown_sf,
        limit=3
    )
    print(message)
    
    # Test 6: Check if at station
    print("=" * 50)
    print("TEST 6: Check if user is at station")
    print("=" * 50)
    
    # Test with exact Embarcadero coordinates
    at_embarcadero = station_location_service.is_user_at_station(
        embarcadero,
        'EMBR',
        threshold_meters=200
    )
    print(f"✅ Is user at Embarcadero? {at_embarcadero}")
    
    # Test with downtown SF (should be at Powell)
    at_powell = station_location_service.is_user_at_station(
        downtown_sf,
        'POWL',
        threshold_meters=200
    )
    print(f"✅ Is user at Powell St? {at_powell}")
    
    # Test 7: Calculate trip progress
    print("\n" + "=" * 50)
    print("TEST 7: Calculate trip progress")
    print("=" * 50)
    print("Simulating trip from Embarcadero to Downtown Berkeley...")
    
    # Simulate user at different points
    test_points = [
        (embarcadero, "At Embarcadero (start)"),
        ((37.8044, -122.2712), "Mid-journey (Oakland)"),
        (downtown_berkeley, "At Downtown Berkeley (end)")
    ]
    
    for location, description in test_points:
        progress = station_location_service.calculate_trip_progress(
            location,
            'EMBR',
            'DBRK'
        )
        
        print(f"\n{description}:")
        print(f"  Progress: {progress.get('progress_percent', 0)}%")
        print(f"  Distance to end: {progress.get('distance_to_end_km', 0)} km")
        print(f"  At start: {progress.get('at_start', False)}")
        print(f"  At end: {progress.get('at_end', False)}")
        print(f"  Almost there: {progress.get('almost_there', False)}")
    
    # Test 8: Get station with directions
    print("\n" + "=" * 50)
    print("TEST 8: Get station with walking directions")
    print("=" * 50)
    print("Getting directions from Downtown SF to Powell St...")
    
    station_with_dirs = station_location_service.get_station_with_directions(
        downtown_sf,
        'POWL'
    )
    
    if station_with_dirs:
        station = station_with_dirs['station']
        distance = station_with_dirs['distance']
        directions = station_with_dirs['directions']
        
        print(f"✅ Station: {station['name']}")
        print(f"   Address: {station['address']}")
        dist_str = location_service.format_distance_message(distance)
        print(f"   Distance: {dist_str}")
        
        if directions:
            print(f"   Walking time: {directions['duration_minutes']} minutes")
            if 'note' in directions:
                print(f"   Note: {directions['note']}")
    
    print("\n" + "=" * 50)
    print("🎉 All location tests completed!")
    print("=" * 50)
    
    print("\n💡 Note: For full walking directions with turn-by-turn,")
    print("   add a Google Maps API key to your .env file")


if __name__ == "__main__":
    test_location_services()
