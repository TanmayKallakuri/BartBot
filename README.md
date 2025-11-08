# 🚇 BARTBot - Your Transit BFF

Your personal Bay Area transit companion on WhatsApp. Real-time BART updates, smart route planning, and multi-modal journey assistance.

## 🎯 What It Does

BARTBot is your homie for navigating the Bay Area. It helps you:

- 🚆 Get real-time BART schedules and delays
- 📍 Find nearest stations based on your location
- 🔔 Smart alerts that learn your commute patterns
- 🚴 Bay Wheels bike share integration
- 🚌 Muni alternatives when BART's acting up
- 🌧️ Weather alerts for your journey
- 🚗 Uber/Lyft cost estimates as backup
- 🧠 AI-powered pattern recognition for your favorite routes

## 🏗️ Project Structure

```
BARTBot/
├── app/
│   ├── services/          # API integrations (BART, Muni, Weather, etc.)
│   ├── models/            # Database models (User, Route, Trip)
│   ├── utils/             # Helper functions
│   └── bot.py             # Main WhatsApp bot logic
├── tests/                 # Unit tests
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (API keys)
```

## 🚀 Features

### Phase 1 (MVP) - In Progress
- [x] Project setup
- [ ] BART API integration
- [ ] WhatsApp bot basic setup
- [ ] Location tracking
- [ ] Start/Stop trip mode
- [ ] "Get off" alerts

### Phase 2 (Smart Features)
- [ ] Pattern recognition
- [ ] Weather integration
- [ ] Twitter delay monitoring
- [ ] Muni integration
- [ ] Scheduled alerts

### Phase 3 (Full Experience)
- [ ] Bay Wheels integration
- [ ] Multi-modal journey planning
- [ ] Uber/Lyft pricing
- [ ] Offline caching

## 🛠️ Tech Stack

- **Backend:** Python (Flask/FastAPI)
- **Database:** PostgreSQL
- **Cache:** Redis
- **APIs:** 
  - Twilio (WhatsApp)
  - BART API
  - 511.org (Bay Area Transit)
  - Bay Wheels
  - Google Maps
  - OpenWeatherMap
  - Twitter API
  - Uber/Lyft APIs

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/BARTBot.git
cd BARTBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🔑 API Keys Needed

- Twilio (WhatsApp Business API)
- BART API (free)
- Google Maps API
- OpenWeatherMap API
- Twitter API
- Uber/Lyft Developer APIs

## 🎨 Conversational Design

BARTBot talks like a friend, not a robot:

```
User: "Get me to Montgomery"
Bot: "Bet! You're at 16th St Mission right? 
     Next train in 4 mins. 
     Wanna start trip mode? I'll keep you posted 🚇"
```

## 📄 License

MIT License - Build cool stuff with it!

## 🙌 Contributing

This started as a personal project but contributions are welcome! Open an issue or PR.

---

Built with ❤️ for Bay Area commuters
