import json
import os
import sys
from dateutil import parser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.models import SessionLocal, Ticket, User, init_db

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic_tickets.jsonl")

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"Data file not found at {DATA_FILE}. Please run generate_tickets.py first.")
        return

    init_db()
    db = SessionLocal()
    
    try:
        # Clear existing data for a clean slate
        db.query(Ticket).delete()
        db.query(User).delete()
        db.commit()
        
        users_cache = {}
        
        print("Loading tickets into the database...")
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                
                username = data.pop("username")
                user_dept = data.pop("user_department")
                
                if username not in users_cache:
                    user = User(username=username, department=user_dept)
                    db.add(user)
                    db.flush() # get ID
                    users_cache[username] = user.id
                
                # Convert ISO string to datetime
                data["created_at"] = parser.parse(data["created_at"]).replace(tzinfo=None)
                data["user_id"] = users_cache[username]
                
                ticket = Ticket(**data)
                db.add(ticket)
                
        db.commit()
        print("Successfully loaded all data into the database!")
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_data()
