"""
Test script to verify BART API integration
Run this to test if the BART service is working
"""
from app.services.bart_service import bart_service

def test_bart_api():
    print("🚇 Testing BART API Integration...\n")
    
    # Test 1: Get all stations
    print("=" * 50)
    print("TEST 1: Getting all BART stations")
    print("=" * 50)
    stations = bart_service.get_all_stations()
    print(f"✅ Found {len(stations)} stations")
    print(f"First 3 stations: {[s['name'] for s in stations[:3]]}\n")
    
    # Test 2: Get station info
    print("=" * 50)
    print("TEST 2: Getting info for Embarcadero Station")
    print("=" * 50)
    station_info = bart_service.get_station_info('EMBR')
    print(f"✅ Station: {station_info.get('name', 'N/A')}")
    print(f"   Address: {station_info.get('address', 'N/A')}")
    print(f"   City: {station_info.get('city', 'N/A')}\n")
    
    # Test 3: Get real-time departures
    print("=" * 50)
    print("TEST 3: Real-time departures from Embarcadero")
    print("=" * 50)
    departures = bart_service.get_real_time_departures('EMBR')
    print(f"✅ Found {len(departures)} upcoming trains")
    message = bart_service.format_departure_message(departures, limit=3)
    print(message)
    
    # Test 4: Get route schedule
    print("=" * 50)
    print("TEST 4: Route from Embarcadero to Downtown Berkeley")
    print("=" * 50)
    trips = bart_service.get_route_schedule('EMBR', 'DBRK')
    if trips:
        trip = trips[0]
        print(f"✅ Next trip:")
        print(f"   Departs: {trip['orig_time']}")
        print(f"   Arrives: {trip['dest_time']}")
        print(f"   Duration: {trip['trip_time']} minutes")
        print(f"   Fare: ${trip['fare']}\n")
    
    # Test 5: Get advisories
    print("=" * 50)
    print("TEST 5: Current service advisories")
    print("=" * 50)
    advisories = bart_service.get_advisories()
    if advisories:
        print(f"⚠️ Found {len(advisories)} advisories:")
        for adv in advisories[:3]:
            print(f"   - {adv['station']}: {adv['type']}")
    else:
        print("✅ No service advisories - smooth sailing!")
    
    # Test 6: Find nearest station
    print("\n" + "=" * 50)
    print("TEST 6: Finding nearest station to SF coordinates")
    print("=" * 50)
    # Coordinates for downtown SF (near Powell St)
    nearest = bart_service.find_nearest_station(37.7849, -122.4094)
    if nearest:
        print(f"✅ Nearest station: {nearest['name']}")
        print(f"   Distance: {nearest['distance_km']} km")
        print(f"   Address: {nearest['address']}\n")
    
    print("=" * 50)
    print("🎉 All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_bart_api()
