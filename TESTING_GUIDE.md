# BartBot Testing Guide

Complete guide to testing your improved BartBot with conversation model enhancements and Google Maps integration.

---

## 🚀 Quick Start Testing

### Option 1: Run Automated Tests (Recommended First)

Test all features automatically:

```bash
python test_bot_features.py
```

**This will test:**
- ✅ 17 conversational message patterns
- ✅ Smart fallback responses
- ✅ Location service capabilities
- ✅ Response formatting
- ✅ Help system

**Expected output:**
```
🎉 All conversation tests passed!
✅ Conversation Model: 17/17 tests passed
✅ Fallback Responses: Working
✅ Response Formatting: All templates working
```

---

### Option 2: Interactive Chat Testing

Simulate a conversation with the bot:

```bash
python interactive_test.py
```

**Try these messages:**

```
You: Hi
You: I need to get to Berkeley
You: When's the next train?
You: Show me directions
You: loc                    # Simulates sharing location
You: Find a bus stop
You: I'm lost
You: quit                   # Exit
```

This lets you test the bot's responses without setting up WhatsApp!

---

## 📋 Testing Checklist

### 1. Conversation Model Tests

Test that the bot understands natural language:

| Message | Expected Intent | Status |
|---------|----------------|--------|
| "I need to go to Berkeley" | plan_route | ✓ |
| "Can you help me get to the airport?" | plan_route | ✓ |
| "Are there any trains coming?" | get_departures | ✓ |
| "Show me directions" | get_directions | ✓ |
| "Find a bus stop" | find_bus_stop | ✓ |
| "What can you do?" | help | ✓ |
| "I'm lost" | help | ✓ |

**Run:** `python test_bot_features.py`

---

### 2. Location Features Tests

#### Without Google Maps API (Basic Mode)

The bot will still work with fallback estimates:

```python
python interactive_test.py

# Test these:
You: loc                    # Share location
You: show me directions     # Should give estimated distance
You: find a bus stop        # Will explain API needed
You: nearest transit hub    # Will explain API needed
```

#### With Google Maps API (Full Features)

After installing `googlemaps` and enabling APIs:

```python
python interactive_test.py

# Test these:
You: loc                          # Share location
You: show me directions           # Turn-by-turn directions!
You: find a bus stop              # Lists 5 nearest bus stops
You: nearest transit hub          # Shows all nearby transit
You: get me to Embarcadero       # Plans route
You: show me directions           # Directions to station
```

---

### 3. Smart Fallback Tests

Test contextual suggestions when bot doesn't understand:

```python
python interactive_test.py

You: I need to find something
# Should suggest station-related commands

You: What time is it?
# Should suggest time/schedule commands

You: Random gibberish
# Should give general help suggestions
```

---

## 🧪 Full Feature Testing

### Test Scenario 1: Route Planning with Directions

```
1. You: "I want to go to Berkeley"
   Bot: Shows route info (Embarcadero → Berkeley)

2. You: "Show me directions"
   Bot: Provides walking directions to Embarcadero station

3. You: "Start trip"
   Bot: Starts trip tracking
```

### Test Scenario 2: Finding Transit Options

```
1. You: "loc"
   Bot: Got your location!

2. You: "Find a bus stop"
   Bot: Lists 5 nearest bus stops with distances

3. You: "Nearest transit hub"
   Bot: Shows all nearby subway/train/bus stations
```

### Test Scenario 3: Natural Conversation

```
You: "Hey"
Bot: Friendly greeting

You: "I'm lost and need help"
Bot: Shows help message with all commands

You: "Can you help me get to the airport?"
Bot: Plans route to SFO

You: "Are there any delays?"
Bot: Checks BART status
```

---

## 🔧 Advanced Testing

### Test with Database

Initialize the database first:

```bash
python init_database.py
```

Then test features that require DB:
- Trip tracking
- Saved profiles
- Pattern recognition

### Test with Real Location Data

Modify `interactive_test.py` to use your actual coordinates:

```python
# In interactive_test.py, change:
test_location = (YOUR_LAT, YOUR_LON)  # Your actual coordinates
```

### Test API Endpoints (for WhatsApp Integration)

Run the server:

```bash
python server.py
```

Test the health endpoint:

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "status": "ok",
  "service": "BARTBot WhatsApp Service",
  "version": "1.0.0"
}
```

---

## 🐛 Troubleshooting Tests

### "ModuleNotFoundError: No module named 'googlemaps'"

**Solution:**
```bash
pip install googlemaps
```

If installation fails, the bot will still work with fallback mode!

### "API key not valid"

**Check:**
1. API key in `.env` is correct
2. No extra spaces in the key
3. Google Maps APIs are enabled in Cloud Console

**Test API key:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GOOGLE_MAPS_API_KEY')[:20] + '...')"
```

### "No stations found"

**Likely causes:**
1. Using location outside San Francisco Bay Area
2. BART API might be down
3. Check `test_location` coordinates in `interactive_test.py`

### Tests fail with database errors

**Solution:**
```bash
python init_database.py
```

This creates the SQLite database with all required tables.

---

## 📊 Expected Test Results

### Automated Tests (`test_bot_features.py`)

```
✅ Conversation Model: 17/17 tests passed
✅ Fallback Responses: Working with contextual suggestions
✅ Location Service: [Full features OR Fallback mode]
✅ Response Formatting: All templates working
✅ Help System: Updated with new features
```

### Interactive Tests (`interactive_test.py`)

**You should see:**
- Natural, conversational responses
- Contextual help when confused
- Proper formatting with emojis
- Location-aware features (if location shared)
- Turn-by-turn directions (if Google Maps API configured)

---

## 🎯 What to Test Before Production

### Critical Features:
- ✅ Natural language understanding (all 17 patterns)
- ✅ Route planning with station recognition
- ✅ Train departure queries
- ✅ Help system responses
- ✅ Error handling (unknown commands)

### Location Features (if Google Maps configured):
- ✅ Walking directions to stations
- ✅ Bus stop finder
- ✅ Transit hub discovery
- ✅ Distance calculations

### Database Features (if enabled):
- ✅ Trip tracking (start/stop)
- ✅ Profile saving
- ✅ User management

### Integration Features:
- ✅ WhatsApp webhook handling
- ✅ Location message parsing
- ✅ Multi-turn conversations
- ✅ Session management

---

## 📝 Test Reporting

Create an issue if you find:
- Messages that should be understood but aren't
- Incorrect intent detection
- Response formatting issues
- API errors
- Database problems

**Include:**
- Exact message you sent
- Expected behavior
- Actual behavior
- Any error messages
- Your test environment (with/without Google Maps API)

---

## 🚀 Next Steps After Testing

Once tests pass:

1. **Local Testing Complete** ✓
2. **Set up Twilio/WhatsApp** (for production)
3. **Deploy to server** (Heroku, AWS, etc.)
4. **Configure webhooks**
5. **Test with real WhatsApp messages**
6. **Monitor and iterate**

---

## 💡 Pro Testing Tips

### Speed Up Testing

Create a test shortcut:
```bash
alias testbot="python interactive_test.py"
```

### Test Multiple Scenarios

Create a test script:
```python
# test_scenarios.py
messages = [
    "Hi",
    "Get me to Berkeley",
    "Show me directions",
    "Any delays?",
]

for msg in messages:
    response = bartbot.process_message("test", msg, None)
    print(f"{msg} → {response[:50]}...")
```

### Compare Before/After

Save responses before improvements:
```bash
python test_bot_features.py > before.txt
```

After improvements:
```bash
python test_bot_features.py > after.txt
diff before.txt after.txt
```

---

## ✨ Happy Testing!

Your BartBot is ready to test with:
- 🗣️ Improved conversation understanding
- 📍 Location-based features
- 🗺️ Google Maps integration
- 🚌 Transit discovery
- 💡 Smart help system

Run `python test_bot_features.py` to get started!
