import sqlite3

DB_NAME = "blog.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL
        )""")

        db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL, 
        image TEXT,
        section_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (section_id) REFERENCES sections(id)
        )
        """)
        db.commit()


def seed_data():
    """Заповнює базу даних тестовими даними"""
    with get_db() as db:
        # Додаємо розділи
        db.executemany("""
            INSERT OR IGNORE INTO sections (name, slug) 
            VALUES (?, ?)
        """, [
            ("Ігри з відкритим світом", "Open world games"),
            ("Піксельні ігри", "Pixel games"),
            ("Майнкрафт", "Minecraft"),
            ("Хогвартс спадщина", "Hogwarts legacy")
        ])
        db.commit()


def get_blog_sections():
    with get_db() as db:
        sections = db.execute("SELECT * FROM sections").fetchall()
        return sections


def get_section_by_slug(section_slug):
    with get_db() as db:
        section = db.execute("SELECT * FROM sections WHERE slug = ?", (section_slug,)).fetchone()
        return section


def get_section_by_id(section_id):
    with get_db() as db:
        section = db.execute("SELECT * FROM sections WHERE id = ?", (section_id,)).fetchone()
        return section


def get_section_posts(section_id):
    with get_db() as db:
        posts = db.execute("""
        SELECT * FROM posts 
        WHERE section_id = ?
        ORDER BY created_at DESC
        """, (section_id,)).fetchall()

    return posts


def create_new_post(text, image, section_id):
    with get_db() as db:
        db.execute("""
        INSERT INTO posts (text, image, section_id)
        VALUES (?, ?, ?)
        """, (text, image, section_id))
        db.commit()


if __name__ == "__main__":
    init_db()
    seed_data()
    print("✅ База даних ініціалізована та заповнена!")
