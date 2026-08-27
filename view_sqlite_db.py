import sqlite3

db_path = "summer_camp.db"
print("==========================================")
print(f"READING SQLITE DATABASE: {db_path}")
print("==========================================")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables in SQLite Database: {tables}\n")

if "sports" in tables:
    print("--- SPORTS TABLE ---")
    cursor.execute("SELECT id, title, category, min_age, max_age, instructor, fee, max_capacity, enrolled_count FROM sports;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID {row[0]}: {row[1]} | Category: {row[2]} | Ages: {row[3]}-{row[4]} | Coach: {row[5]} | Fee: ${row[6]} | Enrolled: {row[8]}/{row[7]}")
    print()

if "enrollments" in tables:
    print("--- ENROLLMENTS TABLE ---")
    cursor.execute("SELECT id, enrollment_code, participant_name, participant_age, parent_name, parent_email, amount_paid, status FROM enrollments;")
    rows = cursor.fetchall()
    if not rows:
        print("No enrollment records in SQLite yet.")
    for row in rows:
        print(f"ID {row[0]}: Code [{row[1]}] | Camper: {row[2]} ({row[3]} yrs) | Parent: {row[4]} ({row[5]}) | Paid: ${row[6]} | Status: {row[7]}")

conn.close()
print("==========================================")
