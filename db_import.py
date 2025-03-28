import pandas as pd
import sqlite3

# Load CSV data
df = pd.read_csv('./assets/manifest.csv')

# Create SQLite database connection
conn = sqlite3.connect('capsules_database.db')
cursor = conn.cursor()

# Create table schema with `id`, `title`, and `information`
cursor.execute("""
CREATE TABLE IF NOT EXISTS capsules (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    information TEXT NOT NULL
)
""")

# Save data to SQLite
df.to_sql('capsules', conn, if_exists='replace', index=False)
conn.close()

print("Data imported into SQLite database successfully!")
