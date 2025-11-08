# Running BartBot in VS Code with GitHub

Complete guide to clone, setup, and run your BartBot in VS Code.

---

## 🚀 Step 1: Clone the Repository in VS Code

### Method A: Using VS Code Built-in Git

1. **Open VS Code**

2. **Open Command Palette**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type: `Git: Clone`

3. **Enter your repository URL:**
   ```
   https://github.com/TanmayKallakuri/BartBot.git
   ```

4. **Choose a location** on your computer to save the project

5. **Open the cloned repository** when prompted

### Method B: Using Terminal in VS Code

1. **Open VS Code**

2. **Open Terminal** (`Ctrl+` ` or View → Terminal)

3. **Navigate to where you want the project:**
   ```bash
   cd ~/Documents  # or wherever you want
   ```

4. **Clone the repository:**
   ```bash
   git clone https://github.com/TanmayKallakuri/BartBot.git
   cd BartBot
   ```

5. **Open the folder in VS Code:**
   ```bash
   code .
   ```

---

## 📦 Step 2: Install Dependencies

### 2.1 Create Virtual Environment (Recommended)

In VS Code Terminal:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### 2.2 Install Required Packages

```bash
pip install -r requirements.txt
```

**Note:** If `googlemaps` fails to install, that's okay! The bot will work in fallback mode.

### 2.3 Install Additional Dependencies (if needed)

```bash
pip install python-dotenv geopy flask flask-cors sqlalchemy
```

---

## ⚙️ Step 3: Configure Environment Variables

Your `.env` file is already configured with the Google Maps API key, but make sure it exists:

### Check if .env exists:

In VS Code, look for `.env` in the file explorer (left sidebar).

If it doesn't exist:

1. **Create `.env` file** in the project root
2. **Copy from `.env.example`:**
   - Right-click `.env.example` → Copy
   - Right-click in file explorer → Paste
   - Rename to `.env`

3. **Your `.env` should have:**
   ```env
   GOOGLE_MAPS_API_KEY=AIzaSyAn_txXVaVwa8_uJKshf5lvrjAdzk0gxvo
   BART_API_KEY=MW9S-E7SL-26DU-VV8V

   # Add these if you have Twilio for WhatsApp:
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

---

## 🗄️ Step 4: Initialize Database

In VS Code Terminal:

```bash
python init_database.py
```

This creates `bartbot.db` with all required tables.

---

## 🧪 Step 5: Test the Bot

### Quick Test (Automated)

```bash
python test_bot_features.py
```

**Expected output:**
```
🎉 All conversation tests passed!
✅ Conversation Model: 17/17 tests passed
```

### Interactive Test (Chat with Bot)

```bash
python interactive_test.py
```

**Try these:**
```
You: Hi
You: I need to go to Berkeley
You: show me directions
You: find a bus stop
You: help
You: quit
```

---

## 🏃 Step 6: Run the Bot Server

### Start the Flask Server

In VS Code Terminal:

```bash
python server.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

### Test the Server

Open a **new terminal** (`Ctrl+Shift+` `) and run:

```bash
curl http://localhost:5000/
```

**Expected response:**
```json
{
  "status": "ok",
  "service": "BARTBot WhatsApp Service",
  "version": "1.0.0"
}
```

---

## 🎯 VS Code Pro Tips

### 1. **Select Python Interpreter**

1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose the one from your `venv` folder

### 2. **Run Python Files Easily**

- Click the **Play button** (▶️) in top-right corner of any `.py` file
- Or press `Ctrl+F5` to run without debugging
- Or press `F5` to run with debugging

### 3. **Open Multiple Terminals**

- Click the **+** icon in the Terminal panel
- Terminal 1: Run server (`python server.py`)
- Terminal 2: Run tests (`python interactive_test.py`)

### 4. **Use VS Code Extensions**

Install these helpful extensions:

- **Python** (Microsoft) - Python language support
- **Pylance** - Enhanced Python IntelliSense
- **GitLens** - Enhanced Git features
- **Better Comments** - Highlight TODOs and important comments

### 5. **Quick File Navigation**

- `Ctrl+P` - Quick file search
- `Ctrl+Shift+F` - Search across all files
- `Ctrl+B` - Toggle sidebar

---

## 📂 Project Structure in VS Code

```
BartBot/
├── .env                        # Your API keys (don't commit!)
├── .gitignore                  # Git ignore rules
├── server.py                   # Main server (run this!)
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── bartbot.db                  # SQLite database (created after init)
│
├── app/
│   ├── bot.py                 # Main bot logic
│   ├── services/
│   │   ├── location_service.py    # Google Maps integration
│   │   └── bart_service.py        # BART API
│   └── utils/
│       ├── message_parser.py      # Conversation understanding
│       └── response_builder.py    # Response formatting
│
├── test_bot_features.py       # Automated tests
├── interactive_test.py        # Interactive chat
├── TESTING_GUIDE.md          # Testing documentation
└── GOOGLE_MAPS_SETUP.md      # Google Maps setup
```

---

## 🔄 Working with Git in VS Code

### View Changes

- **Source Control Panel** (Ctrl+Shift+G)
- See all modified files
- Click files to see diff

### Pull Latest Changes

```bash
git pull origin claude/improve-conversation-model-011CUvxC4L3bLP5H8AdDXqXP
```

Or use VS Code:
1. Click Source Control icon
2. Click `...` menu
3. Select "Pull"

### Commit Changes (if you make edits)

In VS Code Terminal:
```bash
git add .
git commit -m "Your commit message"
git push
```

Or use VS Code Source Control panel:
1. Stage changes (click `+` next to files)
2. Enter commit message
3. Click ✓ to commit
4. Click `...` → Push

---

## 🐛 Troubleshooting in VS Code

### "Python not found"

1. Install Python: https://www.python.org/downloads/
2. Restart VS Code
3. Select Python interpreter (`Ctrl+Shift+P` → Python: Select Interpreter)

### "Module not found" errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Terminal not working

- Try: `Ctrl+Shift+P` → "Terminal: Select Default Profile"
- Choose: Command Prompt (Windows) or bash (Mac/Linux)

### Can't see .env file

- It's hidden by default
- Look for it in the file explorer
- Or create it manually: Right-click → New File → `.env`

---

## 🚀 Quick Start Commands

**Full setup from scratch:**

```bash
# 1. Clone repo
git clone https://github.com/TanmayKallakuri/BartBot.git
cd BartBot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python init_database.py

# 5. Test it
python test_bot_features.py

# 6. Run interactive test
python interactive_test.py

# 7. Run server
python server.py
```

---

## 📱 Next Steps (Optional)

### Connect to WhatsApp

1. Sign up for Twilio: https://www.twilio.com/
2. Get WhatsApp sandbox credentials
3. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```
4. Set webhook URL to your server

### Deploy to Production

Options:
- **Heroku** - Easy deployment
- **Railway** - Modern platform
- **AWS/Google Cloud** - More control
- **Replit** - Quick testing

---

## 🎉 You're Ready!

Your BartBot is now set up in VS Code!

**Quick test:**
```bash
python interactive_test.py
```

**Run server:**
```bash
python server.py
```

**Have questions?** Check:
- `TESTING_GUIDE.md` - Testing instructions
- `GOOGLE_MAPS_SETUP.md` - Google Maps setup

Happy coding! 🤖🚇
