# 🧪 Testing Instructions

## Option 1: Automated Setup (EASIEST) 🚀

**Just double-click this file:**
```
setup_and_test.bat
```

This will automatically:
1. Create virtual environment
2. Activate it
3. Install all dependencies
4. Run the BART API tests

---

## Option 2: Manual Setup (Step by Step) 📝

### Step 1: Open Command Prompt

```bash
# Press Windows Key + R
# Type: cmd
# Press Enter
```

### Step 2: Navigate to Project

```bash
cd C:\Users\ktanm\Documents\BARTBot
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` at the start of your command prompt line.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- requests (for API calls)
- python-dotenv (for config)
- geopy (for distance calculations)
- And other dependencies

### Step 6: Run the Test

```bash
python test_bart_api.py
```

---

## 📊 Expected Output

If everything works, you should see:

```
🚇 Testing BART API Integration...

==================================================
TEST 1: Getting all BART stations
==================================================
✅ Found 50+ stations
First 3 stations: ['12th St. Oakland City Center', '16th St. Mission', '19th St. Oakland']

==================================================
TEST 2: Getting info for Embarcadero Station
==================================================
✅ Station: Embarcadero
   Address: 298 Market Street
   City: San Francisco

==================================================
TEST 3: Real-time departures from Embarcadero
==================================================
✅ Found 10+ upcoming trains
🚇 **Next Trains:**

⏱️ 3 min → **Antioch** 
   Platform 1 | 10 cars

⏱️ 5 min → **Dublin/Pleasanton** 🚴
   Platform 2 | 10 cars

... (more trains)

==================================================
TEST 4: Route from Embarcadero to Downtown Berkeley
==================================================
✅ Next trip:
   Departs: 2:30 PM
   Arrives: 2:55 PM
   Duration: 25 minutes
   Fare: $4.70

==================================================
TEST 5: Current service advisories
==================================================
✅ No service advisories - smooth sailing!
(or)
⚠️ Found 2 advisories:
   - System-wide: DELAY
   - Richmond: MAINTENANCE

==================================================
TEST 6: Finding nearest station to SF coordinates
==================================================
✅ Nearest station: Powell St.
   Distance: 0.45 km
   Address: 899 Market Street

==================================================
🎉 All tests completed!
==================================================
```

---

## 🐛 Troubleshooting

### Problem: "python is not recognized"

**Solution:**
- Make sure Python is installed
- Try `py` instead of `python`
- Add Python to your PATH

### Problem: "No module named 'requests'"

**Solution:**
- Make sure virtual environment is activated (you should see `(venv)`)
- Run `pip install -r requirements.txt` again

### Problem: "ModuleNotFoundError: No module named 'app'"

**Solution:**
- Make sure you're in the BARTBot directory
- Check that the `app` folder exists
- Verify `app\__init__.py` exists

### Problem: API returns empty data

**Solution:**
- Check your internet connection
- BART API might be temporarily down
- Try again in a few minutes

### Problem: "geopy" import error

**Solution:**
```bash
pip install geopy
```

---

## ✅ Success Checklist

After running the test, you should have seen:

- [ ] List of 50+ BART stations
- [ ] Details for Embarcadero station
- [ ] Real-time train departures (with times)
- [ ] Route schedule with fare and duration
- [ ] Service advisories (or confirmation of no issues)
- [ ] Nearest station calculation

If you saw all of these, **CONGRATULATIONS! 🎉**
Your BART API integration is working perfectly!

---

## 🚀 Next Steps

Once testing is successful:

1. **Explore the data** - Try different stations
2. **Build database models** - Store user preferences
3. **Set up WhatsApp bot** - Connect to Twilio
4. **Add location tracking** - Integrate Google Maps

---

## 💡 Quick Test Commands

Test specific stations:
```python
# In Python interpreter after activating venv
from app.services.bart_service import bart_service

# Get departures from any station
bart_service.get_real_time_departures('MONT')  # Montgomery
bart_service.get_real_time_departures('POWL')  # Powell St
bart_service.get_real_time_departures('DBRK')  # Downtown Berkeley

# Get route between any two stations
bart_service.get_route_schedule('MONT', 'EMBR')

# Find nearest station
bart_service.find_nearest_station(37.7749, -122.4194)  # San Francisco coords
```

---

**Ready? Let's test! 🚇✨**
