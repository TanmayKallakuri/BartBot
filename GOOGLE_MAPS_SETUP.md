# Google Maps API Setup Guide

## ✅ Status: API Key Configured!

Your Google Maps API key has been successfully added to `.env`

## 📦 Required Package Installation

To enable full Google Maps functionality, install the `googlemaps` package:

```bash
pip install googlemaps
```

**Note:** If installation fails, the bot will still work! It will use distance-based estimates instead of real Google Maps directions.

## 🔑 Enable Required APIs

For all features to work, enable these APIs in your [Google Cloud Console](https://console.cloud.google.com/apis/library):

### Required APIs:
1. **Directions API** - For turn-by-turn navigation
2. **Places API** - For finding bus stops and transit hubs
3. **Geocoding API** - For address to coordinates conversion

### How to Enable:
1. Go to https://console.cloud.google.com/apis/library
2. Search for each API above
3. Click "Enable"
4. Repeat for all three APIs

## 🚀 Available Features

Once setup is complete, users can:

### 🚶 Get Walking Directions
```
User: "Show me directions"
User: "How do I get to the station?"
User: "Navigate me"
```

The bot will provide:
- Turn-by-turn walking directions
- Distance and estimated time
- Step-by-step instructions

### 🚌 Find Bus Stops
```
User: "Find a bus stop"
User: "Nearest bus"
User: "Where can I catch a bus?"
```

The bot will show:
- 5 nearest bus stops
- Distance from user's location
- Full addresses

### 🚇 Find Transit Hubs
```
User: "Nearest transit hub"
User: "Find transit"
User: "Public transport near me"
```

The bot will display:
- Nearby subway/train/bus stations
- Station types
- Distances and addresses

### 🗺️ Transit Routing
The bot can provide public transportation directions with:
- Bus/train line names and numbers
- Boarding and exit stops
- Departure/arrival times
- Number of stops per leg

## 🔒 Security Notes

- Your `.env` file is already added to `.gitignore` to protect your API key
- Never commit your API key to version control
- Keep your `.env` file secure

## 🧪 Testing the Setup

Run this command to test your configuration:

```python
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if api_key and api_key != 'your_google_maps_api_key_here':
    print('✓ API Key configured correctly!')
    print(f'  Key starts with: {api_key[:20]}...')
else:
    print('✗ API Key not configured')
"
```

## 💡 Fallback Behavior

If the Google Maps API is unavailable, the bot will:
- Calculate straight-line distances using geopy
- Estimate walking times (5 km/h average speed)
- Add a note: "Estimated - Google Maps API key not configured"

This ensures the bot remains functional even without the API!

## 📊 API Usage & Costs

Google Maps APIs have a free tier:
- **Directions API**: $5.00 per 1000 requests (up to 40,000 free/month)
- **Places API**: $17.00 per 1000 requests (Monthly $200 credit)
- **Geocoding API**: $5.00 per 1000 requests (up to 40,000 free/month)

Most personal usage will stay within the free tier.

Monitor usage: https://console.cloud.google.com/apis/dashboard

## 🆘 Troubleshooting

### "Module not found: googlemaps"
```bash
pip install googlemaps
```

### "API key not valid"
- Check the key in `.env` matches your Google Cloud Console key
- Ensure the key has no extra spaces
- Verify the APIs are enabled in Google Cloud Console

### "No results returned"
- Check that Places API is enabled
- Verify your API key has permission to use the APIs
- Ensure you're searching in a valid location

## 📚 Documentation

- [Google Maps Directions API](https://developers.google.com/maps/documentation/directions)
- [Google Maps Places API](https://developers.google.com/maps/documentation/places/web-service)
- [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding)
