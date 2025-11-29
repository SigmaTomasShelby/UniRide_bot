import aiosqlite


async def init_db():
    async with aiosqlite.connect('visits.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                time_of_start TEXT,
                place_of_departure TEXT,
                place_of_arrival TEXT,
                cost TEXT,
                comment TEXT
            )
        ''')
        await db.commit()