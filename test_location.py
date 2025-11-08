"""
Test script for location services
Tests Google Maps integration and location helpers
"""
from app.services.maps_service import maps_service
from app.utils.location_helper import location_helper


def test_location_services():
    print("📍 Testing Location Services\n")
    print("=" * 50)
    
    # Test coordinates (Downtown SF, near Powell St)
    test_lat = 37.7849
    test_lng = -122.4094
    
    print(f"\n🧪 Test Location: {test_lat}, {test_lng}")
    print("(Downtown San Francisco, near Powell St)")
    print()
    
    # Test 1: Find nearest BART station
    print("=" * 50)
    print("TEST 1: Finding nearest BART station")
    print("=" * 50)
    
    nearest = location_helper.find_nearest_bart_station(test_lat, test_lng)
    
    if nearest:
        station = nearest['station']
        distance = nearest['distance']
        
        print(f"✅ Nearest station: {station['name']}")
        print(f"   Station code: {station['abbr']}")
        print(f"   Address: {station.get('address', 'N/A')}")
        print(f"   Distance: {distance['distance_text']}")
        print(f"   Walking time: {distance['duration_text']}")
    else:
        print("❌ Could not find nearest station")
    
    # Test 2: Calculate distance
    print("\n" + "=" * 50)
    print("TEST 2: Calculate distance between stations")
    print("=" * 50)
    
    # Embarcadero to Montgomery coordinates
    embr_coords = (37.7955, -122.3971)
    mont_coords = (37.7894, -122.4013)
    
    distance = maps_service.calculate_distance(embr_coords, mont_coords)
    
    print(f"✅ Distance from Embarcadero to Montgomery:")
    print(f"   {distance['km']} km")
    print(f"   {distance['miles']} miles")
    print(f"   {distance['meters']} meters")
    
    # Test 3: Check if near station
    print("\n" + "=" * 50)
    print("TEST 3: Check if location is near Powell St")
    print("=" * 50)
    
    is_near = location_helper.is_user_near_station(
        test_lat, test_lng, 
        'POWL',  # Powell St station
        threshold_meters=200
    )
    
    print(f"✅ Near Powell St (within 200m)? {is_near}")
    
    # Test 4: Route progress
    print("\n" + "=" * 50)
    print("TEST 4: Calculate route progress")
    print("=" * 50)
    
    # Simulate being between Embarcadero and Downtown Berkeley
    # Location: Somewhere in the middle (let's use Oakland)
    mid_lat = 37.8044
    mid_lng = -122.2712
    
    progress = location_helper.calculate_route_progress(
        mid_lat, mid_lng,
        'EMBR',  # Start: Embarcadero
        'DBRK'   # End: Downtown Berkeley
    )
    
    if progress:
        print(f"✅ Route progress:")
        print(f"   Distance from start: {progress['distance_from_start_km']} km")
        print(f"   Distance to end: {progress['distance_to_end_km']} km")
        print(f"   Progress: {progress['progress_percentage']}%")
        print(f"   Near destination? {progress['is_near_destination']}")
    
    # Test 5: Should send "get off" alert
    print("\n" + "=" * 50)
    print("TEST 5: Get off alert detection")
    print("=" * 50)
    
    # Test at different distances
    test_cases = [
        (37.7849, -122.4094, "POWL", "At station"),  # Very close to Powell
        (37.7900, -122.4050, "MONT", "Approaching"),  # Near Montgomery
        (37.8044, -122.2712, "LAKE", "Far away")     # Far from Lake Merritt
    ]
    
    for lat, lng, station, description in test_cases:
        alert_info = location_helper.should_send_get_off_alert(lat, lng, station)
        
        print(f"\n   {description} ({station}):")
        print(f"   Should alert? {alert_info['should_alert']}")
        if 'distance_to_station' in alert_info:
            print(f"   Distance: {alert_info['distance_to_station']:.0f} meters")
            print(f"   Alert type: {alert_info.get('alert_type', 'N/A')}")
    
    # Test 6: Format friendly messages
    print("\n" + "=" * 50)
    print("TEST 6: Location description formatting")
    print("=" * 50)
    
    message = location_helper.format_location_message(
        test_lat, test_lng,
        include_nearby_station=True
    )
    
    print(f"✅ Friendly location message:")
    print(f"   {message}")
    
    # Test 7: Distance formatting
    print("\n" + "=" * 50)
    print("TEST 7: Friendly distance formatting")
    print("=" * 50)
    
    test_distances = [0.05, 0.3, 1.2, 5.8]
    
    for dist in test_distances:
        formatted = maps_service.format_distance_friendly(dist)
        print(f"   {dist} km → {formatted}")
    
    # Test 8: ETA messages
    print("\n" + "=" * 50)
    print("TEST 8: ETA message generation")
    print("=" * 50)
    
    test_distances_eta = [0.1, 0.5, 2.0, 5.0]
    
    for dist in test_distances_eta:
        walking = maps_service.get_eta_message(dist, 'walking')
        biking = maps_service.get_eta_message(dist, 'biking')
        print(f"   {dist} km:")
        print(f"      Walking: {walking}")
        print(f"      Biking: {biking}")
    
    # Test 9: Google Maps API status
    print("\n" + "=" * 50)
    print("TEST 9: Google Maps API Status")
    print("=" * 50)
    
    if maps_service.client:
        print("✅ Google Maps API: Connected")
        print("   Note: Some features require valid API key")
    else:
        print("⚠️  Google Maps API: Not configured")
        print("   Using fallback calculations")
        print("   Set GOOGLE_MAPS_API_KEY in .env for full features")
    
    print("\n" + "=" * 50)
    print("🎉 All location tests completed!")
    print("=" * 50)
    
    print("\n💡 Key Features Tested:")
    print("   ✅ Find nearest BART station")
    print("   ✅ Calculate distances")
    print("   ✅ Check proximity to stations")
    print("   ✅ Track route progress")
    print("   ✅ Get off alert detection")
    print("   ✅ Friendly message formatting")
    print("   ✅ ETA calculations")


if __name__ == "__main__":
    test_location_services()
