# 🚀 Quick Start Guide

## Step 1: Set Up Virtual Environment

```bash
# Navigate to project
cd C:\Users\ktanm\Documents\BARTBot

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Test BART API

The BART API has a public key we can use for testing!

```bash
python test_bart_api.py
```

This will test all the BART API functions and show you real-time data.

## Step 4: Set Up Environment Variables

```bash
# Copy the example file
copy .env.example .env

# The BART API key is already set in config.py for testing
# You'll need to add other API keys later:
# - Twilio (for WhatsApp)
# - Google Maps
# - OpenWeatherMap
# etc.
```

## Next Steps

Once the BART API test works, we'll build:

1. **Database models** - Store user profiles and routes
2. **WhatsApp bot** - Connect to Twilio
3. **Location tracking** - Use Google Maps API
4. **Smart alerts** - Pattern detection and notifications
5. **Multi-modal integration** - Muni, Bay Wheels, etc.

## Current Status

✅ Project structure created
✅ BART API service implemented
⏳ Ready to test!

## Testing BART API

Run the test script to see real-time BART data:

```bash
python test_bart_api.py
```

You should see:
- List of all BART stations
- Real-time departures from Embarcadero
- Route schedules
- Service advisories
- Nearest station finder

## Troubleshooting

**Import errors?**
- Make sure you're in the virtual environment
- Make sure you're in the BARTBot directory
- Run `pip install -r requirements.txt` again

**API errors?**
- Check your internet connection
- BART API might be down (rare)
- Check if the API key in config.py is still valid

---

**Ready to test? Run:**
```bash
python test_bart_api.py
```

Let's see that beautiful real-time BART data! 🚇✨
