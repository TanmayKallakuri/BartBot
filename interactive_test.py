#!/usr/bin/env python3
"""
Interactive BartBot Testing
Simulates conversations with the bot without WhatsApp
"""
import sys

try:
    from app.bot import bartbot
    print("✓ Bot loaded successfully!")
except Exception as e:
    print(f"✗ Error loading bot: {e}")
    print("\nMake sure dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

print("=" * 80)
print("🤖 BartBot Interactive Testing")
print("=" * 80)
print("\nThis simulates a conversation with the bot.")
print("Type your messages and see how the bot responds!")
print("\nCommands:")
print("  'quit' or 'exit' - Exit the test")
print("  'loc' - Simulate sharing location (Downtown SF)")
print("  'help' - Ask the bot for help")
print("\n" + "=" * 80)

# Simulated user ID
user_id = "test_user_12345"

# Downtown San Francisco coordinates (for testing location features)
test_location = (37.7879, -122.4075)

print("\n💬 Start chatting with BartBot! (Type 'quit' to exit)\n")

while True:
    try:
        # Get user input
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Handle special commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break

        # Simulate location sharing
        location = None
        if user_input.lower() == 'loc':
            location = test_location
            print(f"📍 Sharing location: Downtown SF ({location})")
            user_input = ""  # Location-only message

        # Process message with bot
        try:
            response = bartbot.process_message(user_id, user_input, location)
            print(f"\nBot: {response}\n")
        except Exception as e:
            print(f"\n❌ Error processing message: {e}\n")
            import traceback
            traceback.print_exc()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

print("\n" + "=" * 80)
print("Testing session ended.")
print("=" * 80)
