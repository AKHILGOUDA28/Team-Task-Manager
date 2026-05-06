import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Verify URL
db_url = os.environ.get('DATABASE_URL')
if not db_url or 'sqlite' in db_url:
    print("❌ ERROR: DATABASE_URL is not set to your Supabase PostgreSQL URL in your .env file.")
    print("Please update DATABASE_URL in your .env file before running this script.")
    sys.exit(1)

print("Connecting to Supabase PostgreSQL database...")

# Import app context and db
from app import create_app
from models import db

app = create_app()

try:
    with app.app_context():
        db.create_all()
        print("🎉 SUCCESS: All tables have been successfully created in your Supabase database!")
except Exception as e:
    print(f"❌ ERROR: Could not connect to Supabase: {e}")
    print("Please check that your DATABASE_URL in .env has the correct password and credentials.")
