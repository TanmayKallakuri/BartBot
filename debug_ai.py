#!/usr/bin/env python3
"""
Debug AI initialization
"""
import os
from dotenv import load_dotenv

print("=" * 70)
print("AI Initialization Diagnostics")
print("=" * 70)

# Test 1: Check .env loading
print("\n1. Checking .env file...")
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✓ API key found: {api_key[:20]}...")
    print(f"  Length: {len(api_key)} characters")
else:
    print("✗ No API key found in environment")

# Test 2: Check openai package
print("\n2. Checking openai package...")
try:
    import openai
    print(f"✓ openai package installed: version {openai.__version__}")
except ImportError as e:
    print(f"✗ openai package not found: {e}")
    exit(1)

# Test 3: Try to initialize OpenAI client
print("\n3. Trying to initialize OpenAI client...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    print("✓ OpenAI client created successfully")
except Exception as e:
    print(f"✗ Error creating OpenAI client: {e}")
    print(f"  Error type: {type(e).__name__}")

# Test 4: Check Config loading
print("\n4. Checking Config class...")
try:
    from config import Config
    print(f"✓ Config loaded")
    print(f"  Config.OPENAI_API_KEY: {Config.OPENAI_API_KEY[:20] if Config.OPENAI_API_KEY else 'None'}...")
except Exception as e:
    print(f"✗ Error loading Config: {e}")

# Test 5: Test actual parser initialization
print("\n5. Testing MessageParser initialization...")
try:
    from app.utils.message_parser import MessageParser
    parser = MessageParser()
    print(f"  AI enabled: {parser.use_ai}")
    print(f"  OpenAI client: {parser.openai_client is not None}")
    if not parser.use_ai:
        print("  ⚠️  AI is NOT enabled!")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Diagnostics complete!")
print("=" * 70)
