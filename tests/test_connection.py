"""
Supabase Connection Test Script
Tests database connection and basic operations
"""

import os
import sys
from datetime import datetime, timezone

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Supabase client not installed!")
    print("Run: pip install supabase")
    sys.exit(1)

# Load credentials from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing environment variables!")
    print("Please set:")
    print("  SUPABASE_URL=your_project_url")
    print("  SUPABASE_SERVICE_KEY=your_service_key")
    sys.exit(1)

print("🔌 Testing Supabase connection...")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}...")

try:
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Client created successfully")
    
    # Test 1: Query signals table
    print("\n📊 Test 1: Query signals table...")
    response = supabase.table('signals').select('*').limit(5).execute()
    print(f"✅ Found {len(response.data)} signal(s)")
    
    if response.data:
        print("\nSample signal:")
        signal = response.data[0]
        print(f"  Asset: {signal.get('asset')}")
        print(f"  Direction: {signal.get('direction')}")
        print(f"  Confidence: {signal.get('confidence')}%")
        print(f"  Posted: {signal.get('posted_at_utc')}")
    
    # Test 2: Insert a test signal
    print("\n📝 Test 2: Insert test signal...")
    test_signal = {
        'asset': 'EUR/USD',
        'direction': 'BUY',
        'direction_icon': '🟢',
        'timeframe': 'M15',
        'session': 'Test Session',
        'price_levels': {
            'entry_zone': ['1.16710', '1.16750'],
            'take_profit': '1.17080',
            'stop_loss': '1.16480'
        },
        'trade_details': {
            'target_pips': 35,
            'risk_reward': '1 : 1.40',
            'suggested_risk': '0.5% – 1%'
        },
        'trade_type': 'Intraday',
        'confidence': 96,
        'posted_at_utc': datetime.now(timezone.utc).isoformat(),
        'expiry_rules': {
            'session_only': True,
            'expires_at': 'NY_CLOSE',
            'invalidate_if_missed_entry': True
        }
    }
    
    insert_response = supabase.table('signals').insert(test_signal).execute()
    print(f"✅ Signal inserted with ID: {insert_response.data[0]['id']}")
    
    # Test 3: Query active signals view
    print("\n🔍 Test 3: Query active signals view...")
    active_response = supabase.table('active_signals').select('*').limit(3).execute()
    print(f"✅ Found {len(active_response.data)} active signal(s)")
    
    # Test 4: Check tables exist
    print("\n📋 Test 4: Verify tables...")
    tables = [
        'signals',
        'signal_history',
        'telegram_subscribers',
        'signal_deliveries',
        'analytics',
        'api_logs'
    ]
    
    for table in tables:
        try:
            supabase.table(table).select('id').limit(1).execute()
            print(f"  ✅ {table}")
        except Exception as e:
            print(f"  ❌ {table}: {e}")
    
    print("\n" + "="*50)
    print("🎉 All tests passed!")
    print("="*50)
    print("\nDatabase is ready to use!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check SUPABASE_URL is correct")
    print("2. Check SUPABASE_SERVICE_KEY is correct (not anon key)")
    print("3. Verify database schema has been executed")
    print("4. Check network connection")
    sys.exit(1)
