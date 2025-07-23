import aiosqlite
import asyncio

DB_NAME = "async_users.db"

# Setup the database and add sample data
async def setup_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("DELETE FROM users")  # Clear old data
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 25), ("Bob", 45), ("Charlie", 60), ("Diana", 35)]
        )
        await db.commit()

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("All users:")
        for row in rows:
            print(row)

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        print("\nUsers older than 40:")
        for row in rows:
            print(row)
        return rows

# Run both queries concurrently
async def fetch_concurrently():
    await setup_db()
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
