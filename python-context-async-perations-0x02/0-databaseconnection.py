class DatabaseConnection :
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def __enter__(self):
        
        print(f"Connecting to database at {self.db_url}...")
        self.connection = f"Connection to {self.db_url}"
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            print(f"Closing connection to {self.db_url}...")
            self.connection = None
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True

with self.connection as conn:
    conn.execute("SELECT * FROM users")
    results = conn.fetchall()
    for row in results:
        print(row)