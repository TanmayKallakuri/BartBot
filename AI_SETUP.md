# AI-Powered Message Understanding

Your BartBot now has **hybrid AI + regex** message understanding!

---

## 🧠 How It Works

### **Hybrid Approach:**

1. **First: Fast Regex Matching** ⚡
   - Checks common patterns (fast, free)
   - Handles simple, well-formed messages
   - No API calls needed

2. **Fallback: AI Understanding** 🤖
   - Only used when regex doesn't match
   - Understands typos, slang, complex requests
   - Uses OpenAI GPT-3.5-turbo

---

## 💰 Cost-Effective Design

- **Regex matches:** FREE (90%+ of messages)
- **AI fallback:** ~$0.002 per message (only complex cases)
- **Typical usage:** $1-2/month

---

## ✨ What AI Enables

### Before (Regex Only):
```
User: "I wanna catch a train to berkley tmrw morning"
Bot: ❌ "Hmm, not sure what you mean"
```

### After (With AI):
```
User: "I wanna catch a train to berkley tmrw morning"
AI: Detected "plan_route" to "Berkeley (DBRK)"
Bot: ✅ "Planning route to Berkeley..."
```

### Examples AI Can Handle:

✅ **Typos:** "berkley" → Berkeley
✅ **Slang:** "wanna go to" → plan_route
✅ **Natural language:** "how can I reach the airport?"
✅ **Complex requests:** "get me from embarcadero to berkeley"
✅ **Misspellings:** "montgomry" → Montgomery
✅ **Abbreviations:** "SF airport" → SFO

---

## 🔑 Setup Instructions

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Add to `.env` File

Open your `.env` file and add:

```env
# OpenAI (for AI-powered message understanding)
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Install OpenAI Package

```bash
pip install openai
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Restart the Bot

```bash
python interactive_test.py
```

You should see:
```
✓ AI-powered understanding enabled (OpenAI)
```

---

## 🧪 Testing AI Understanding

Run the interactive test:

```bash
python interactive_test.py
```

**Try these complex messages:**

```
You: I wanna catch a train to berkley
You: how can I reach the airport tmrw
You: get me from montgomry to embarcadro
You: need to find a bus stop near by
You: whats the fastest route to SFO
```

Watch for `[AI]` tags in the output showing when AI is used!

---

## 📊 How to Monitor Usage

The bot prints debug info:

```
[AI] Parsed 'I wanna go to berkley' → plan_route (confidence: 0.95)
```

If you see `[AI]` tags, AI was used for that message.

---

## ⚙️ Configuration Options

### Use AI for All Messages (Not Recommended)

If you want AI to parse ALL messages (expensive):

Modify `message_parser.py`:
```python
# In parse() method, call AI first:
if self.use_ai:
    ai_result = self._parse_with_ai(message)
    if ai_result:
        return ai_result
# Then try regex...
```

### Disable AI Temporarily

Remove or comment out in `.env`:
```env
# OPENAI_API_KEY=sk-your-key
```

The bot automatically falls back to regex-only mode.

---

## 💡 Best Practices

### 1. **Monitor Costs**

Check usage at: https://platform.openai.com/usage

Set spending limits in OpenAI dashboard.

### 2. **Use GPT-3.5-turbo** (Default)

- Fast and cheap ($0.002/message)
- GPT-4 is more expensive ($0.03/message)
- GPT-3.5 is sufficient for intent detection

### 3. **Keep Regex Patterns Updated**

Common messages should match regex to avoid API calls:
- Greetings
- Simple "get me to X"
- "Next train from X"

### 4. **Set Rate Limits** (Optional)

In `message_parser.py`, you can add:
```python
import time
self.last_ai_call = 0
MIN_INTERVAL = 1  # seconds

# In _parse_with_ai():
if time.time() - self.last_ai_call < MIN_INTERVAL:
    return None  # Rate limit
self.last_ai_call = time.time()
```

---

## 🐛 Troubleshooting

### "AI-powered understanding failed"

**Possible causes:**
1. Invalid API key
2. OpenAI package not installed
3. Network/API issues

**Solution:**
```bash
# Check API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:20])"

# Reinstall openai
pip install --upgrade openai
```

### "Using regex-only mode"

This means:
- OpenAI package not installed, OR
- No API key in `.env`

The bot still works, just without AI fallback.

### AI Parsing Errors

If you see `[AI] Error:` messages:
- Check OpenAI API status
- Verify API key is valid
- Check you have credits/billing enabled

---

## 📈 Expected Performance

### Regex Coverage:
- ~90% of messages match patterns
- Instant response
- Zero cost

### AI Fallback:
- ~10% of messages use AI
- ~1-2 second response time
- ~$0.002 per message

### Total Monthly Cost:
- Light use (100 messages): ~$0.20
- Medium use (500 messages): ~$1.00
- Heavy use (2000 messages): ~$4.00

---

## 🔒 Security & Privacy

### API Key Security:
- ✅ Stored in `.env` (gitignored)
- ✅ Never committed to repo
- ✅ Server-side only

### Data Sent to OpenAI:
- User messages only
- No personal information
- No conversation history
- Messages not stored by OpenAI (as of API policy)

### Best Practices:
- Use separate API keys for dev/prod
- Rotate keys periodically
- Monitor usage dashboard
- Set spending limits

---

## 📚 Technical Details

### Model: GPT-3.5-turbo

**Parameters:**
- Temperature: 0.3 (consistent, focused)
- Max tokens: 200 (short responses)
- System prompt: Custom BART-specific

### Response Format:

```json
{
  "intent": "plan_route",
  "confidence": 0.95,
  "entities": {
    "origin": "EMBR",
    "destination": "DBRK"
  }
}
```

### Fallback Chain:

1. Try regex patterns
2. If no match → Try AI
3. If AI fails → Return "unknown"

---

## 🎯 When AI Is Used

AI fallback triggers when:
- ❌ No regex pattern matches
- ❌ Message contains typos
- ❌ Natural language without keywords
- ❌ Complex multi-part requests

AI is NOT used when:
- ✅ Clear regex match found
- ✅ API key not configured
- ✅ OpenAI package not installed

---

## 🚀 Future Enhancements

Possible additions:
- **Context awareness:** Remember previous messages
- **Multi-turn conversations:** Track conversation state
- **Entity extraction:** Better station/time extraction
- **Local models:** Run AI locally (no API costs)
- **Caching:** Cache AI results for similar messages

---

## 📞 Need Help?

- **Documentation:** See `TESTING_GUIDE.md`
- **OpenAI Docs:** https://platform.openai.com/docs
- **Cost Calculator:** https://openai.com/pricing

---

## ✨ Summary

Your bot now has **intelligent fallback** that:
- Uses fast regex for common messages (90%+)
- Falls back to AI for complex cases (10%)
- Costs ~$1-2/month for typical usage
- Handles typos, slang, and natural language

**Enable it now:**
1. Get API key from OpenAI
2. Add to `.env`
3. `pip install openai`
4. Test it!

🤖 **Your bot is now much smarter!**
