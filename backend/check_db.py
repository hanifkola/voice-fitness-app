from database import SessionLocal
import models

db = SessionLocal()

try:
    # Try fetching a table entry to check the connection
    test_entry = db.query(models.Workout).first()
    if test_entry:
        print(f"Connected! First workout: {test_entry.exercise_name}")
    else:
        print("Connected, but no workouts found.")
except Exception as e:
    print(f"Database connection failed: {e}")
finally:
    db.close()
