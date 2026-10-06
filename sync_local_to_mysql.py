import os
import json
import db

FALLBACK_FILE = os.path.join(os.path.dirname(__file__), 'local_bookings.json')

def sync_pending():
    test = db.test_connection()
    if not test['success']:
        print("[Error] Cannot connect to MySQL:", test.get('error'))
        print("[Hint] Please update 'password' in 'db_config.json'.")
        return False

    if not os.path.exists(FALLBACK_FILE):
        print("No pending bookings found.")
        return True

    try:
        with open(FALLBACK_FILE, 'r', encoding='utf-8') as f:
            pending = json.load(f)
    except Exception as e:
        print("Could not read local_bookings.json:", e)
        return False

    print(f"Found {len(pending)} pending bookings to sync to MySQL...")
    success_count = 0

    for item in pending:
        try:
            res = db.save_booking(
                name=item.get('name', 'Customer'),
                mobile=item.get('mobile', ''),
                locality=item.get('locality', 'Vijayawada'),
                pref_date=item.get('pref_date', ''),
                pref_time=item.get('pref_time', ''),
                garments=item.get('garments') or item.get('garnments') or 'Bespoke Order',
                shirt_size=item.get('shirt_size'),
                pant_size=item.get('pant_size')
            )
            print(f" Synced: User '{item.get('name')}' (#{res['user_id']}), Booking #{res['booking_id']}")
            success_count += 1
        except Exception as e:
            print(f" Failed to sync item {item.get('name')}: {e}")

    print(f" Successfully inserted {success_count}/{len(pending)} records into MySQL customers database!")
    return True

if __name__ == '__main__':
    sync_pending()
