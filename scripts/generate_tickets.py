import json
import os
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

NUM_TICKETS = 1500
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "synthetic_tickets.jsonl")

CATEGORIES = {
    "Password Reset": ["AD Lockout", "Expired Password", "Application Login Issue"],
    "Email Issues": ["Outlook Disconnected", "Cannot Send Emails", "Spam Filter Overactive"],
    "Software Installation": ["Missing License", "Admin Rights Needed", "Installation Failed"],
    "Network Connectivity": ["VPN Dropping", "Wi-Fi Authentication Failed", "Slow Intranet"],
    "Hardware Failure": ["Blue Screen", "Monitor Not Waking", "Keyboard Keys Sticking"],
    "Access Rights": ["Shared Drive Access Denied", "SharePoint Permission", "GitHub Repo Access"],
    "Application Error": ["SAP GUI Crash", "CRM Timeout", "Internal Tool 500 Error"]
}

PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
DEPARTMENTS = ["Finance", "HR", "Engineering", "Sales", "IT", "Marketing", "Operations"]

def generate_ticket():
    category = random.choice(list(CATEGORIES.keys()))
    subcategory = random.choice(CATEGORIES[category])
    
    status = random.choices(STATUSES, weights=[0.2, 0.1, 0.5, 0.2])[0]
    
    # Priority logic based on category
    if category == "Network Connectivity" or category == "Hardware Failure":
        priority = random.choices(PRIORITIES, weights=[0.1, 0.2, 0.4, 0.3])[0]
    else:
        priority = random.choices(PRIORITIES, weights=[0.4, 0.4, 0.15, 0.05])[0]

    created_at = fake.date_time_between(start_date="-30d", end_date="now")
    
    ticket = {
        "ticket_id": f"INC{str(uuid.uuid4().int)[:8]}",
        "title": f"{subcategory} - {fake.catch_phrase()}",
        "description": f"User reported: {fake.sentence(nb_words=15)} {fake.sentence(nb_words=10)}",
        "category": category,
        "subcategory": subcategory,
        "priority": priority,
        "status": status,
        "created_at": created_at.isoformat(),
        "user_department": random.choice(DEPARTMENTS),
        "username": fake.user_name(),
        "logs_snippet": fake.text(max_nb_chars=200) if random.random() > 0.5 else None,
        "resolution_steps": fake.paragraph(nb_sentences=3) if status in ["Resolved", "Closed"] else None,
        "root_cause": fake.sentence(nb_words=8) if status in ["Resolved", "Closed"] else None
    }
    return ticket

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating {NUM_TICKETS} synthetic tickets...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for _ in range(NUM_TICKETS):
            ticket = generate_ticket()
            f.write(json.dumps(ticket) + "\n")
            
    print(f"Successfully generated tickets at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
