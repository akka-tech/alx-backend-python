class DatabaseConnection :
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def __enter__(self):
        
        print(f"Connecting to database at {self.db_url}...")
        self.connection = f"Connection to {self.db_url}"
        return self.connection

with self.connection as conn:
    conn.execute("SELECT * FROM users")
    results = conn.fetchall()
    for row in results:
        print(row)