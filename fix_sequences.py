from app import app, db
from sqlalchemy import text

def fix_sequences():
    with app.app_context():
        try:
            # Re-sync sequences to the max id in the tables
            db.session.execute(text("SELECT setval('users_user_id_seq', COALESCE((SELECT MAX(user_id) FROM users) + 1, 1), false);"))
            db.session.execute(text("SELECT setval('bookings_booking_id_seq', COALESCE((SELECT MAX(booking_id) FROM bookings) + 1, 1), false);"))
            db.session.execute(text("SELECT setval('payments_payment_id_seq', COALESCE((SELECT MAX(payment_id) FROM payments) + 1, 1), false);"))
            db.session.commit()
            print("Successfully re-synchronized PostgreSQL sequences!")
        except Exception as e:
            print(f"Error updating sequences: {e}")

if __name__ == "__main__":
    fix_sequences()
