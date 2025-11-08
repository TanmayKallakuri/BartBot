# 📍 Location Services Guide

## What We Just Built

✅ **Complete Location Layer** with 2 services:

1. **Location Service** - Core GPS and mapping functions
2. **Station Location Service** - BART + Location integration

---

## 🚀 Quick Test

```bash
# Make sure venv is activated
cd C:\Users\ktanm\Documents\BARTBot
venv\Scripts\activate

# Install googlemaps (if needed)
pip install googlemaps

# Run location tests
python test_location_services.py
```

---

## 📦 What's Included

### Location Service (`location_service.py`)

**Core Functions:**
- `calculate_distance(point1, point2)` - GPS distance calculation
- `is_near_location(current, target, threshold)` - Proximity check
- `find_nearest_point(location, points)` - Find closest from list
- `estimate_walking_time(distance_km)` - Walking time estimate
- `format_distance_message(distance)` - User-friendly formatting

**Google Maps Functions** (require API key):
- `get_walking_directions(origin, dest)` - Turn-by-turn directions
- `geocode_address(address)` - Address → GPS
- `reverse_geocode(location)` - GPS → Address

### Station Location Service (`station_location_service.py`)

**Smart Station Finding:**
- `find_nearest_stations(location, limit)` - Nearest BART stations with distances
- `get_station_with_directions(location, station)` - Station + walking directions
- `is_user_at_station(location, station)` - Check if at station
- `format_nearest_stations_message(location)` - User-friendly message

**Trip Tracking:**
- `calculate_trip_progress(location, start, end)` - Trip progress %
  - Returns: at_start, at_end, distance_to_end, progress_percent, almost_there

---

## 💡 Usage Examples

### Find Nearest Stations

```python
from app.services.station_location_service import station_location_service

# User location (lat, lng)
downtown_sf = (37.7849, -122.4094)

# Find nearest 3 stations
stations = station_location_service.find_nearest_stations(
    downtown_sf,
    limit=3
)

for station in stations:
    print(f"{station['name']}: {station['distance']['distance_km']} km")
```

### Get Formatted Message

```python
message = station_location_service.format_nearest_stations_message(
    downtown_sf,
    limit=3
)
print(message)
# Output:
# 📍 **Nearest BART Stations:**
# 
# **1. Powell St**
#    📏 0.45 km away (~5 min walk)
#    📮 899 Market Street
```

### Check If At Station

```python
user_location = (37.7955, -122.3933)  # Embarcadero coords

at_station = station_location_service.is_user_at_station(
    user_location,
    'EMBR',  # Embarcadero
    threshold_meters=200
)

if at_station:
    print("User is at Embarcadero!")
```

### Calculate Trip Progress

```python
# User somewhere between Embarcadero and Berkeley
user_location = (37.8044, -122.2712)

progress = station_location_service.calculate_trip_progress(
    user_location,
    'EMBR',  # Start
    'DBRK'   # End
)

print(f"Trip progress: {progress['progress_percent']}%")
print(f"Distance to destination: {progress['distance_to_end_km']} km")

if progress['almost_there']:
    print("Almost at your stop!")
```

### Calculate Distance

```python
from app.services.location_service import location_service

point1 = (37.7849, -122.4094)  # Downtown SF
point2 = (37.7955, -122.3933)  # Embarcadero

distance = location_service.calculate_distance(point1, point2)

print(f"Distance: {distance['distance_km']} km")
print(f"Distance: {distance['distance_meters']} meters")
print(f"Walking time: ~{location_service.estimate_walking_time(distance['distance_km'])} minutes")
```

---

## 🎯 What This Powers

### 1. "Find Nearest Station"
```python
# User: "Where's the nearest BART station?"
message = station_location_service.format_nearest_stations_message(
    user_location,
    limit=3
)
# Bot sends formatted message with 3 nearest stations
```

### 2. "Get Off" Alerts
```python
# During active trip, check progress
progress = station_location_service.calculate_trip_progress(
    current_location,
    start_station,
    end_station
)

if progress['almost_there'] and not alert_sent:
    # Send "Get ready, your stop is next!" alert
    send_alert()
```

### 3. Trip Start Detection
```python
# Check if user arrived at starting station
at_start = station_location_service.is_user_at_station(
    user_location,
    trip.start_station_abbr,
    threshold_meters=200
)

if at_start:
    trip.start_trip()
    # Bot: "Trip started! I'll keep you posted 🚇"
```

### 4. Trip End Detection
```python
# Check if user arrived at destination
at_end = station_location_service.is_user_at_station(
    user_location,
    trip.end_station_abbr,
    threshold_meters=200
)

if at_end:
    trip.complete_trip()
    # Bot: "Made it! Trip ended. Need anything else?"
```

---

## 🔑 Google Maps API (Optional)

Most features work WITHOUT an API key (using geodesic calculations).

**With API key, you get:**
- Turn-by-turn walking directions
- Address geocoding
- Real-time traffic data

**To add API key:**
1. Get key from [Google Cloud Console](https://console.cloud.google.com/)
2. Add to `.env`:
   ```
   GOOGLE_MAPS_API_KEY=your_key_here
   ```

**Without API key:**
- Distance calculations still work (geopy)
- Estimated walking times work
- Station finding works
- Trip progress works

---

## 📊 Testing Output

Running `python test_location_services.py` tests:

1. ✅ Distance calculations
2. ✅ Proximity checks
3. ✅ Walking time estimates
4. ✅ Nearest station finding (5 stations)
5. ✅ Formatted messages
6. ✅ "At station" detection
7. ✅ Trip progress calculation (0% → 50% → 100%)
8. ✅ Station with directions

---

## 🎯 Phase 1 Progress

### ✅ COMPLETED:
1. ✅ Project structure
2. ✅ BART API integration
3. ✅ Configuration management
4. ✅ Testing framework
5. ✅ **Database models (all 4)**
6. ✅ **Location services** 📍

### 🔨 STILL TO BUILD:
- WhatsApp Bot Core (Twilio)
- Trip Management System
- Smart Features (alerts, patterns)

---

**Ready to test?**

```bash
python test_location_services.py
```

Let's see those distances and nearest stations! 🗺️✨
