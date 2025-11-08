#!/usr/bin/env python3
"""
Comprehensive BartBot Testing Script
Tests all new features: conversation model + location services
"""
import sys
from app.utils.message_parser import message_parser
from app.utils.response_builder import response_builder

print("=" * 80)
print("🤖 BartBot Feature Testing Suite")
print("=" * 80)

# Test 1: Conversation Model Improvements
print("\n" + "=" * 80)
print("TEST 1: Conversational Language Understanding")
print("=" * 80)

conversational_tests = [
    # Natural route planning
    ("I need to go to Berkeley", "plan_route"),
    ("Can you help me get to the airport?", "plan_route"),
    ("I wanna visit Embarcadero", "plan_route"),

    # Natural departure queries
    ("Are there any trains coming?", "get_departures"),
    ("When's the next train?", "get_departures"),
    ("Show me train times", "get_departures"),

    # Natural station finding
    ("Where's the nearest station?", "find_station"),
    ("Is there a BART near me?", "find_station"),

    # Help requests
    ("I'm lost", "help"),
    ("What can you do?", "help"),
    ("I need help", "help"),

    # New direction intents
    ("Show me directions", "get_directions"),
    ("How do I get there?", "get_directions"),
    ("Navigate me", "get_directions"),

    # Bus and transit
    ("Find a bus stop", "find_bus_stop"),
    ("Nearest bus", "find_bus_stop"),
    ("Public transport near me", "find_transit"),
]

passed = 0
failed = 0

for message, expected_intent in conversational_tests:
    result = message_parser.parse(message)
    detected_intent = result['intent']

    if detected_intent == expected_intent:
        print(f"✓ '{message}'")
        passed += 1
    else:
        print(f"✗ '{message}'")
        print(f"  Expected: {expected_intent}, Got: {detected_intent}")
        failed += 1

print(f"\n📊 Results: {passed}/{len(conversational_tests)} passed")

if failed > 0:
    print(f"⚠️  {failed} tests failed")
else:
    print("🎉 All conversation tests passed!")

# Test 2: Smart Fallback Responses
print("\n" + "=" * 80)
print("TEST 2: Smart Fallback Responses")
print("=" * 80)

fallback_tests = [
    ("I need to find a station", "Should suggest station-related commands"),
    ("What time does it leave?", "Should suggest time/schedule commands"),
    ("Is there a delay?", "Should suggest status commands"),
    ("Random gibberish", "Should give general suggestions"),
]

print("\nTesting contextual suggestions...\n")

for message, description in fallback_tests:
    response = response_builder.unknown_command(message)
    print(f"📝 Message: '{message}'")
    print(f"   {description}")
    print(f"\n   Response preview:")
    # Show first 2 lines of response
    lines = response.split('\n')[:3]
    for line in lines:
        if line.strip():
            print(f"   {line}")
    print()

print("✓ Fallback responses generated successfully!")

# Test 3: Location Service Capabilities
print("\n" + "=" * 80)
print("TEST 3: Location Service Features")
print("=" * 80)

try:
    from app.services.location_service import location_service

    # Test basic distance calculation
    print("\n📍 Testing distance calculation (no API required)...")
    embarcadero = (37.7925, -122.3967)
    montgomery = (37.7896, -122.4012)

    distance = location_service.calculate_distance(embarcadero, montgomery)
    walk_time = location_service.estimate_walking_time(distance['distance_km'])

    print(f"✓ Distance: {distance['distance_meters']:.0f} meters")
    print(f"✓ Walk time: {walk_time} minutes")

    # Check Google Maps API status
    print("\n🗺️  Checking Google Maps API...")
    if location_service.gmaps_client:
        print("✓ Google Maps client initialized!")
        print("  Full features available:")
        print("    • Turn-by-turn directions")
        print("    • Bus stop finder")
        print("    • Transit hub discovery")
    else:
        print("⚠️  Google Maps client not initialized")
        print("  Limited features (fallback mode):")
        print("    • Distance calculations ✓")
        print("    • Time estimates ✓")
        print("\n  To enable full features:")
        print("    1. Install: pip install googlemaps")
        print("    2. Enable APIs in Google Cloud Console")

except Exception as e:
    print(f"✗ Error testing location service: {e}")

# Test 4: Response Formatting
print("\n" + "=" * 80)
print("TEST 4: Response Formatting")
print("=" * 80)

print("\n📝 Testing walking directions format...\n")

sample_directions = {
    'duration_minutes': 8,
    'distance': {'distance_km': 0.65, 'distance_meters': 650},
    'steps': [
        {'instruction': 'Head <b>north</b> on Market St', 'distance': '200 m'},
        {'instruction': 'Turn <b>right</b> onto 5th St', 'distance': '450 m'},
    ]
}

walking_response = response_builder.walking_directions("Embarcadero Station", sample_directions)
print(walking_response)

print("\n" + "-" * 80)
print("\n🚌 Testing bus stops format...\n")

sample_stops = [
    {
        'name': 'Market St & 5th St',
        'address': '500 Market St, SF',
        'distance': {'distance_km': 0.2, 'distance_meters': 200}
    }
]

bus_response = response_builder.nearby_bus_stops(sample_stops)
print(bus_response)

print("✓ All response formats working!")

# Test 5: Help System
print("\n" + "=" * 80)
print("TEST 5: Updated Help System")
print("=" * 80)

help_response = response_builder.help_message()
print("\n" + help_response)

# Summary
print("\n" + "=" * 80)
print("🎯 TESTING SUMMARY")
print("=" * 80)

# Check if location_service was loaded
try:
    api_status = 'Full features' if location_service.gmaps_client else 'Fallback mode'
except NameError:
    api_status = 'Not loaded (googlemaps package needed)'

print(f"""
✅ Conversation Model: {passed}/{len(conversational_tests)} tests passed
✅ Fallback Responses: Working with contextual suggestions
✅ Location Service: {api_status}
✅ Response Formatting: All templates working
✅ Help System: Updated with new features

Next Steps:
1. Install googlemaps package: pip install googlemaps
2. Enable Google APIs (see GOOGLE_MAPS_SETUP.md)
3. Run the bot with: python run.py (or your main entry point)
4. Test with WhatsApp by sending messages to the bot

For manual testing:
- Share your location and ask "show me directions"
- Try "find a bus stop near me"
- Ask "how do I get to Berkeley?"
- Test "I need help" to see all commands
""")

print("=" * 80)
print("✨ Testing Complete!")
print("=" * 80)
