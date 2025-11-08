"""
Test BARTBot in Console Mode
Test the bot logic without needing Twilio/WhatsApp
"""
from app.bot import bartbot
from app.database import init_db


def test_bot_console():
    """Interactive console testing"""
    
    print("\n" + "=" * 50)
    print("🚇 BARTBot - Console Test Mode")
    print("=" * 50)
    
    # Initialize database
    print("\n📦 Initializing database...")
    init_db()
    print("✅ Database ready!")
    
    # Test user
    test_user = "+15555551234"
    
    # Test location (Downtown SF)
    test_location = (37.7849, -122.4094)
    
    print(f"\n🧪 Testing as user: {test_user}")
    print(f"📍 Test location: Downtown SF")
    print("\n" + "=" * 50)
    print("Type messages to test the bot")
    print("Type 'quit' to exit")
    print("Type 'location' to use test location")
    print("=" * 50 + "\n")
    
    use_location = False
    
    while True:
        try:
            # Get user input
            user_message = input("You: ")
            
            if user_message.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            
            if user_message.lower() == 'location':
                use_location = not use_location
                status = "enabled" if use_location else "disabled"
                print(f"\n📍 Location {status}\n")
                continue
            
            if not user_message.strip():
                continue
            
            # Process with bot
            location = test_location if use_location else None
            response = bartbot.process_message(test_user, user_message, location)
            
            # Print bot response
            print(f"\nBot: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def test_bot_automated():
    """Run automated test scenarios"""
    
    print("\n" + "=" * 50)
    print("🧪 Running Automated Bot Tests")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    test_user = "+15555551234"
    test_location = (37.7849, -122.4094)  # Downtown SF
    
    # Test scenarios
    scenarios = [
        ("hi", None, "Greeting"),
        ("help", None, "Help command"),
        ("nearest station", test_location, "Find nearest station"),
        ("next train from embarcadero", None, "Get departures"),
        ("get me to berkeley", test_location, "Plan route"),
        ("any delays?", None, "Check status"),
    ]
    
    for i, (message, location, description) in enumerate(scenarios, 1):
        print(f"\n{'-' * 50}")
        print(f"TEST {i}: {description}")
        print(f"{'-' * 50}")
        print(f"User: {message}")
        if location:
            print(f"Location: {location}")
        
        try:
            response = bartbot.process_message(test_user, message, location)
            print(f"\nBot: {response}\n")
            print("✅ Test passed")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ All automated tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    
    # Check command line argument
    if len(sys.argv) > 1 and sys.argv[1] == 'auto':
        test_bot_automated()
    else:
        test_bot_console()
