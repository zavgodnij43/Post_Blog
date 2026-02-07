import sqlite3


DB_NAME = "blog.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row

conn.executemany("""
    INSERT OR IGNORE INTO sections (name, slug) 
    VALUES (?, ?)
""", [
    ("Ігри з відкритим світом", "Open world games"),
    ("Піксельні ігри", "Pixel games"),
    ("Майнкрафт", "Minecraft"),
    ("Хогвартс спадщина", "Hogwarts legacy")
])
conn.commit()
conn.close()
