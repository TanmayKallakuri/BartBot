"""
Initialize the database
Creates all tables based on models
"""
from app.database import init_db, drop_all
import sys


def main():
    print("🔧 BARTBot Database Initialization\n")
    print("=" * 50)
    
    # Ask for confirmation
    response = input("This will create all database tables. Continue? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Cancelled.")
        return
    
    # Ask if want to drop existing tables
    drop = input("\n⚠️  Drop existing tables first? (y/n): ")
    
    if drop.lower() == 'y':
        print("\n🗑️  Dropping all tables...")
        drop_all()
    
    # Initialize database
    print("\n📦 Creating tables...")
    init_db()
    
    print("\n" + "=" * 50)
    print("✅ Database initialization complete!")
    print("\nTables created:")
    print("  • users")
    print("  • profiles")
    print("  • trips")
    print("  • patterns")
    print("\n💡 Ready to start storing data!")


if __name__ == "__main__":
    main()
