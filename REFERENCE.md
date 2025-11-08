# 🎯 BARTBot - Quick Reference

## 📂 Project Location
```
C:\Users\ktanm\Documents\BARTBot
```

## ⚡ Quick Commands

### First Time Setup
```bash
cd C:\Users\ktanm\Documents\BARTBot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run Tests
```bash
# Make sure venv is activated first!
python test_bart_api.py
```

### Activate Virtual Environment (Each Time)
```bash
cd C:\Users\ktanm\Documents\BARTBot
venv\Scripts\activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

## 🗂️ Project Structure

```
BARTBot/
├── app/
│   ├── services/
│   │   └── bart_service.py    ← BART API integration
│   ├── models/                ← Database models (TODO)
│   └── utils/                 ← Helper functions (TODO)
├── config.py                  ← Configuration
├── test_bart_api.py          ← Test script
├── setup_and_test.bat        ← Automated setup
└── requirements.txt          ← Dependencies
```

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `bart_service.py` | All BART API functions |
| `test_bart_api.py` | Tests the API |
| `config.py` | API keys and settings |
| `requirements.txt` | Python packages needed |

## 📡 BART API Functions

### Available Now:

```python
from app.services.bart_service import bart_service

# Get all stations
stations = bart_service.get_all_stations()

# Get station details
info = bart_service.get_station_info('EMBR')

# Real-time departures
departures = bart_service.get_real_time_departures('EMBR')

# Route schedule
trips = bart_service.get_route_schedule('EMBR', 'DBRK')

# Service advisories
advisories = bart_service.get_advisories()

# Find nearest station
nearest = bart_service.find_nearest_station(37.7849, -122.4094)
```

## 📍 Common BART Station Codes

| Station | Code |
|---------|------|
| Embarcadero | EMBR |
| Montgomery St | MONT |
| Powell St | POWL |
| 16th St Mission | 16TH |
| Downtown Berkeley | DBRK |
| Oakland 12th St | 12TH |
| MacArthur | MCAR |
| Rockridge | ROCK |
| Walnut Creek | WCRK |
| Dublin/Pleasanton | DUBL |
| Fremont | FRMT |
| Millbrae | MLBR |
| SFO Airport | SFIA |

[Full list in test output]

## 🐍 Python Quick Commands

### Start Python Interactive Mode
```bash
python
```

### Test Individual Functions
```python
from app.services.bart_service import bart_service

# Example: Get departures from Montgomery
deps = bart_service.get_real_time_departures('MONT')
for d in deps[:3]:
    print(f"{d['minutes']} min → {d['destination']}")
```

## ✅ Testing Checklist

Run `python test_bart_api.py` and verify:

- [ ] Gets 50+ stations ✓
- [ ] Shows Embarcadero info ✓
- [ ] Real-time departures with minutes ✓
- [ ] Route schedule with fare ✓
- [ ] Service advisories ✓
- [ ] Nearest station calculation ✓

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| `python not found` | Use `py` instead or check PATH |
| `No module named 'requests'` | Activate venv and run `pip install -r requirements.txt` |
| `ModuleNotFoundError: app` | Make sure you're in BARTBot directory |
| Empty API responses | Check internet, BART API might be down |

## 📚 Documentation Files

- `README.md` - Full project documentation
- `QUICKSTART.md` - Setup guide
- `TESTING.md` - Detailed testing instructions
- `REFERENCE.md` - This file!

## 🎯 Next Steps After Testing

1. ✅ Test BART API (you're here!)
2. 📊 Build database models
3. 💬 Set up WhatsApp integration
4. 📍 Add location services
5. 🧠 Implement pattern recognition

## 🔗 Useful Links

- [BART API Docs](https://api.bart.gov/docs/overview/index.aspx)
- [Notion Project Page](https://www.notion.so/2a5ce9175bd481ffa6ccc0032fa0d025)

---

**Current Status:** Ready to test! 🚀
**Last Updated:** November 8, 2025
