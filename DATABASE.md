# 📊 Database Setup Guide

## What We Just Built

✅ **Complete Database Layer** with 4 models:

1. **User Model** - Store user info and preferences
2. **Profile Model** - Saved routes like "Work Commute"
3. **Trip Model** - Active journey tracking with location
4. **Pattern Model** - Learn user behavior and suggest profiles

---

## 🚀 Quick Start

### Step 1: Install SQLAlchemy (if you haven't)

```bash
# Make sure venv is activated
pip install sqlalchemy
```

### Step 2: Initialize Database

```bash
python init_database.py
```

This creates a SQLite database file: `bartbot.db`

### Step 3: Test the Database

```bash
python test_database.py
```

This will:
- Create a test user
- Create a saved profile
- Start a trip
- Track a usage pattern
- Test all CRUD operations
- Show relationships between models

---

## 📋 Database Schema

### Users Table
```
- whatsapp_number (PK)
- name
- location_permission
- alert_preferences (JSON)
- created_at
- last_active
```

### Profiles Table
```
- id (PK)
- user_whatsapp (FK)
- name ("Work Commute")
- start_station_abbr, start_station_name
- end_station_abbr, end_station_name
- alert_settings (JSON)
- usage_count
- is_favorite
```

### Trips Table
```
- id (PK)
- user_whatsapp (FK)
- profile_id (FK, optional)
- start/end stations
- status (PLANNED, ACTIVE, COMPLETED, CANCELLED)
- current_latitude, current_longitude
- location_history (JSON)
- alerts_sent (JSON)
- quiet_mode_active
```

### Patterns Table
```
- id (PK)
- user_whatsapp (FK)
- route_key ("EMBR→DBRK")
- frequency_count
- time_patterns (JSON)
- profile_suggested
```

---

## 💡 Key Features

### User Model
```python
user = User(whatsapp_number="+1234567890", name="Phoenix")
user.grant_location_permission()
user.update_alert_preferences({'frequency': 'major-only'})
```

### Profile Model
```python
profile = Profile(
    user_whatsapp=user.whatsapp_number,
    name="Work Commute",
    start_station_abbr="EMBR",
    end_station_abbr="DBRK"
)
profile.set_favorite()
profile.increment_usage()
```

### Trip Model
```python
trip = Trip(...)
trip.start_trip()
trip.update_location(37.7955, -122.3933)
trip.add_alert("get_off", "Your stop is next!")
trip.enable_quiet_mode()
trip.complete_trip()
```

### Pattern Model
```python
pattern = Pattern(route_key="EMBR→DBRK", ...)
pattern.add_time_pattern("Mon", "09:15")
pattern.increment_frequency()

if pattern.should_suggest_profile():
    # Suggest creating a saved profile!
    print(pattern.get_pattern_summary())
```

---

## 🔍 Common Queries

### Get User with All Data
```python
user = db.query(User).filter_by(whatsapp_number="+1234567890").first()
print(f"Profiles: {len(user.profiles)}")
print(f"Trips: {len(user.trips)}")
print(f"Patterns: {len(user.patterns)}")
```

### Get Active Trips
```python
active_trips = db.query(Trip).filter_by(status=TripStatus.ACTIVE).all()
```

### Find Patterns Ready for Suggestion
```python
patterns = db.query(Pattern).filter(
    Pattern.frequency_count >= 4,
    Pattern.profile_suggested == False
).all()
```

### Get User's Favorite Profiles
```python
favorites = db.query(Profile).filter_by(
    user_whatsapp=user.whatsapp_number,
    is_favorite=True
).all()
```

---

## 📝 Database File Location

```
C:\Users\ktanm\Documents\BARTBot\bartbot.db
```

You can view/edit this with:
- [DB Browser for SQLite](https://sqlitebrowser.org/) (free tool)
- VS Code SQLite extension
- Python scripts

---

## 🎯 Next Steps After Testing

Once database tests pass:

1. ✅ Database models working
2. 🔜 Build Location Services (Google Maps)
3. 🔜 Create WhatsApp Bot Core
4. 🔜 Implement Trip Management
5. 🔜 Add Smart Features (patterns, alerts)

---

## 🐛 Troubleshooting

### "No module named 'sqlalchemy'"
```bash
pip install sqlalchemy
```

### "Unable to open database file"
- Make sure you're in the BARTBot directory
- Check write permissions

### "Table already exists"
- Run `init_database.py` and choose "y" to drop existing tables

---

**Ready to test?**

```bash
python init_database.py
python test_database.py
```

Let's see that database in action! 🚀
