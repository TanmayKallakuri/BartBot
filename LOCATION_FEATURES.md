# 📍 Location Features Guide

## How Users Share Location on WhatsApp

### **Step 1: Open WhatsApp Chat**
User opens the chat with the BARTBot

### **Step 2: Tap the + Button**
At the bottom of the chat, tap the **+** (attach) button

### **Step 3: Select Location**
Choose **Location** from the menu

### **Step 4: Share Current Location**
- **Live Location** - Shares real-time location for duration
- **Current Location** - Shares location once

---

## What the Bot Can Do With Location

### ✅ **Find Nearest Stations**
```
User: "nearest station"
Bot: [uses location]
     📍 Nearest BART Stations:
     
     1. Powell St
        📏 0.45 km away (~5 min walk)
        📮 899 Market Street
```

### ✅ **Plan Routes Automatically**
```
User: "get me to Berkeley"
[shares location]
Bot: Cool! Using your location 📍
     
     Starting from: Embarcadero
     Going to: Downtown Berkeley
     
     [route info]
```

### ✅ **Track Trips**
```
User: "start trip"
Bot: Trip started!
     [tracks location]
     [sends alerts when approaching destination]
```

---

## Location in the Code

### **Receiving Location**

In `whatsapp_client.py`:
```python
def parse_incoming_message(self, request_data: dict) -> dict:
    # Twilio sends location as Latitude/Longitude
    latitude = request_data.get('Latitude')
    longitude = request_data.get('Longitude')
    
    location = None
    if latitude and longitude:
        location = (float(latitude), float(longitude))
    
    return {
        'location': location  # (lat, lng) or None
    }
```

### **Using Location**

In `bot.py`:
```python
def process_message(
    self,
    user_id: str,
    message: str,
    location: Optional[Tuple[float, float]] = None
) -> str:
    # Location is available throughout processing
    if location:
        # Find nearest stations
        nearest = station_location_service.find_nearest_stations(location)
        
        # Use for route planning
        # Use for trip tracking
```

---

## Testing Location Features

### **Console Test Mode**
```bash
python test_bot.py

# In the console:
You: location
📍 Location enabled

You: nearest station
Bot: [uses test location - Downtown SF]
```

### **WhatsApp Test**
1. Message the bot: "nearest station"
2. Bot will ask for location
3. Share location via WhatsApp
4. Bot responds with nearest stations

---

## Location Permissions

### **User Database**
```python
user.grant_location_permission()  # User allowed location
user.location_permission  # True/False
```

### **First Time Request**
When user first shares location, bot can ask:
```
Bot: 📍 Cool! Can I use your location for:
     - Finding nearest stations
     - Planning routes
     - Tracking trips
     
     Your location stays private! 🔒
```

---

## Privacy & Security

✅ **Location Data Storage:**
- Stored only in active Trip records
- Not shared with third parties
- User can revoke permission anytime

✅ **In Database:**
- `Trip.current_latitude`
- `Trip.current_longitude`
- `Trip.location_history` (array of checkpoints)

✅ **User Control:**
- "forget my location"
- "stop tracking"
- Trip ends = location cleared

---

## Common Location-Based Commands

| User Says | Bot Does |
|-----------|----------|
| "nearest station" | Asks for location, shows 3 nearest |
| "where am I?" | Tells user nearest station |
| "get me to X" | Uses location as origin |
| "start trip" | Begins location tracking |
| "stop trip" | Ends location tracking |
| [shares location] | Acknowledges and uses it |

---

## Implementation Status

✅ **Working Now:**
- Location parsing from WhatsApp
- Find nearest stations with location
- Use location for route origin
- Distance calculations

🔜 **Coming Soon:**
- Live location tracking during trips
- "Get off" alerts based on GPS
- Auto-detect when user arrives at station
- Location history analysis

---

**Current Implementation: Fully functional!** 📍✨

Users can share location anytime and bot will use it intelligently!
