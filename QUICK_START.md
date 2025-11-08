# 🚀 BartBot Quick Start

Get up and running in 5 minutes!

---

## For VS Code Users

### Step 1: Clone Repository
```bash
# In VS Code Terminal (Ctrl+`)
git clone https://github.com/TanmayKallakuri/BartBot.git
cd BartBot
```

### Step 2: Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python init_database.py
```

### Step 4: Test It
```bash
# Quick automated test
python test_bot_features.py

# Or chat with the bot
python interactive_test.py
```

### Step 5: Run Server
```bash
python server.py
```

✅ **Done!** Your bot is running at http://localhost:5000

---

## Quick Commands Reference

| Action | Command |
|--------|---------|
| Test bot features | `python test_bot_features.py` |
| Chat with bot | `python interactive_test.py` |
| Run server | `python server.py` |
| Initialize database | `python init_database.py` |
| Activate virtual env (Mac/Linux) | `source venv/bin/activate` |
| Activate virtual env (Windows) | `venv\Scripts\activate` |

---

## Test the Bot Quickly

```bash
python interactive_test.py
```

Try these messages:
```
You: Hi
You: I need to go to Berkeley
You: Show me directions
You: Find a bus stop
You: Help
You: quit
```

---

## File Structure (What to Open)

```
BartBot/
├── server.py                   ← Main entry point (run this!)
├── interactive_test.py         ← Chat testing
├── test_bot_features.py        ← Automated tests
├── .env                        ← Your API keys
│
├── app/
│   ├── bot.py                 ← Bot logic
│   ├── services/
│   │   └── location_service.py ← Google Maps
│   └── utils/
│       ├── message_parser.py   ← Conversation AI
│       └── response_builder.py ← Responses
```

---

## Common Issues

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "No such file or directory: .env"
```bash
cp .env.example .env
```
Your Google Maps API key is already configured!

### "googlemaps module not found"
```bash
pip install googlemaps
```
Or continue without it - bot works in fallback mode!

### Virtual environment not activating
```bash
# Try this on Windows:
venv\Scripts\activate.bat

# Or this on Mac/Linux:
source venv/bin/activate
```

---

## What's Been Improved?

✅ **Natural Conversation**
- "I need to go to Berkeley" ✓
- "Can you help me get to the airport?" ✓
- "Show me directions" ✓

✅ **Smart Responses**
- Contextual suggestions when confused
- Helpful error messages

✅ **Location Features** (with Google Maps API)
- Turn-by-turn walking directions
- Find nearby bus stops
- Discover transit hubs

---

## Testing Checklist

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Initialize database
- [ ] Run `python test_bot_features.py` (should show 17/17 passed)
- [ ] Run `python interactive_test.py` (chat with bot)
- [ ] Run `python server.py` (start server)
- [ ] Test endpoint: `curl http://localhost:5000/`

---

## Next Steps

1. ✅ **Basic Testing** - You're here!
2. 📖 **Read Full Docs**:
   - `VS_CODE_SETUP.md` - Complete VS Code guide
   - `TESTING_GUIDE.md` - Detailed testing
   - `GOOGLE_MAPS_SETUP.md` - Enable full location features

3. 🚀 **Deploy**:
   - Connect to WhatsApp (Twilio)
   - Deploy to Heroku/Railway
   - Configure webhooks

---

## Get Help

**Documentation:**
- `VS_CODE_SETUP.md` - Full VS Code setup
- `TESTING_GUIDE.md` - Testing guide
- `GOOGLE_MAPS_SETUP.md` - Google Maps setup

**Quick Test:**
```bash
python test_bot_features.py
```

**Interactive Test:**
```bash
python interactive_test.py
```

---

## 🎉 You're Ready!

Your improved BartBot is ready with:
- 🗣️ Natural conversation understanding
- 📍 Location-based features
- 🗺️ Google Maps integration
- 🚌 Transit discovery

Start chatting:
```bash
python interactive_test.py
```
