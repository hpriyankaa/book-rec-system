import sqlite3

# Connect to the database (it will create a new one if it doesn't exist)
conn = sqlite3.connect('your_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'challenges' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        challenge_description TEXT,
        target_books INTEGER,
        start_date DATE,
        end_date DATE
    );
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")
