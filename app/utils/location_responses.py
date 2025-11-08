"""
Location-aware response additions for ResponseBuilder
"""

def location_request() -> str:
    \"\"\"Request user to share location\"\"\"
    return \"\"\"📍 **Share your location for better help!**

Tap the **+** button in WhatsApp and select **Location** to share where you are.

This helps me:
- Find nearest stations
- Plan your route
- Track your trip

Or just tell me which station you're at! 😊\"\"\"

def using_location(station_name: str) -> str:
    \"\"\"Confirm using their location\"\"\"
    return f\"Cool! I see you're near **{station_name}** 📍\"

def route_with_location(origin_name: str, dest_name: str, route_info: str) -> str:
    \"\"\"Route info with location confirmation\"\"\"
    return f\"\"\"✅ **Using your location!**

From: **{origin_name}** 📍
To: **{dest_name}**

{route_info}\"\"\"
