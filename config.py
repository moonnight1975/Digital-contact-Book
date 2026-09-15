import os
import sqlite3
import customtkinter as ctk

DB_ENGINE = "sqlite"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.db")

# Attempt PostgreSQL, fallback to SQLite
conn = None
cur = None

try:
    import psycopg2
    # Attempt quick connection to PostgreSQL
    conn = psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="litto",
        host="localhost",
        port="5432",
        connect_timeout=1
    )
    cur = conn.cursor()
    DB_ENGINE = "postgresql"
    print("Database: Connected to PostgreSQL (mydb)")
except Exception as e:
    # Gracefully fallback to SQLite
    DB_ENGINE = "sqlite"
    print(f"Database: PostgreSQL unavailable ({e}). Seamlessly using SQLite ({DB_PATH})")
    
    class SQLiteCursorWrapper:
        """Wraps sqlite3 cursor to transparently handle %s placeholders used in psycopg2 queries."""
        def __init__(self, raw_cursor):
            self.raw_cursor = raw_cursor

        def execute(self, sql, params=None):
            # Convert %s placeholder to ? for sqlite3
            if params is not None:
                # Replace %s with ? safely
                sql = sql.replace("%s", "?")
                return self.raw_cursor.execute(sql, params)
            return self.raw_cursor.execute(sql)

        def executemany(self, sql, params_list):
            sql = sql.replace("%s", "?")
            return self.raw_cursor.executemany(sql, params_list)

        def fetchone(self):
            return self.raw_cursor.fetchone()

        def fetchall(self):
            return self.raw_cursor.fetchall()

        def fetchmany(self, size=None):
            return self.raw_cursor.fetchmany(size) if size else self.raw_cursor.fetchmany()

        @property
        def description(self):
            return self.raw_cursor.description

        @property
        def rowcount(self):
            return self.raw_cursor.rowcount

        @property
        def lastrowid(self):
            return self.raw_cursor.lastrowid

        def close(self):
            self.raw_cursor.close()

    class SQLiteConnWrapper:
        """Wraps sqlite3 connection to return the wrapped cursor and handle commits."""
        def __init__(self, raw_conn):
            self.raw_conn = raw_conn

        def cursor(self):
            return SQLiteCursorWrapper(self.raw_conn.cursor())

        def commit(self):
            return self.raw_conn.commit()

        def rollback(self):
            return self.raw_conn.rollback()

        def close(self):
            return self.raw_conn.close()

    raw_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn = SQLiteConnWrapper(raw_conn)
    cur = conn.cursor()

# Ensure tables and columns exist in either database
if DB_ENGINE == "postgresql":
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            address TEXT,
            contact_group VARCHAR(50) DEFAULT 'Other',
            birthday DATE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deleted_contacts (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            address TEXT,
            contact_group VARCHAR(50) DEFAULT 'Other',
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            birthday DATE
        )
    """)
    conn.commit()
else:
    # SQLite schema setup & migration
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            contact_group TEXT DEFAULT 'Other',
            birthday TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deleted_contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            contact_group TEXT DEFAULT 'Other',
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            birthday TEXT
        )
    """)
    conn.commit()

    # Check for missing columns in existing SQLite tables and migrate
    cur.execute("PRAGMA table_info(contacts)")
    existing_cols = [col[1] for col in cur.fetchall()]
    if "contact_group" not in existing_cols:
        cur.execute("ALTER TABLE contacts ADD COLUMN contact_group TEXT DEFAULT 'Other'")
    if "birthday" not in existing_cols:
        cur.execute("ALTER TABLE contacts ADD COLUMN birthday TEXT")
    conn.commit()

# --- Helper Database Operations ---
class DBHelper:
    @staticmethod
    def get_contacts(search="", group="All"):
        """Fetch contacts filtered by search term and group."""
        query = "SELECT id, name, phone, email, address, contact_group, birthday FROM contacts"
        conditions = []
        params = []

        if group and group != "All":
            conditions.append("contact_group = %s")
            params.append(group)

        if search and search.strip():
            search_pat = f"%{search.strip()}%"
            conditions.append("(name LIKE %s OR phone LIKE %s OR email LIKE %s)")
            params.extend([search_pat, search_pat, search_pat])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY name COLLATE NOCASE ASC" if DB_ENGINE == "sqlite" else " ORDER BY name ASC"
        cur.execute(query, tuple(params) if params else None)
        return cur.fetchall()

    @staticmethod
    def get_stats():
        """Retrieve count statistics for dashboard."""
        cur.execute("SELECT COUNT(*) FROM contacts")
        total = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM contacts WHERE contact_group = 'Family'")
        family = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM contacts WHERE contact_group = 'Work'")
        work = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM contacts WHERE contact_group = 'Friends'")
        friends = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM deleted_contacts")
        trash = cur.fetchone()[0]

        return {
            "total": total,
            "family": family,
            "work": work,
            "friends": friends,
            "other": total - (family + work + friends),
            "trash": trash
        }

    @staticmethod
    def add_contact(name, phone, email, address, group, birthday=None):
        cur.execute("""
            INSERT INTO contacts (name, phone, email, address, contact_group, birthday)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, phone, email, address, group, birthday))
        conn.commit()

    @staticmethod
    def update_contact(contact_id, name, phone, email, address, group, birthday=None):
        cur.execute("""
            UPDATE contacts
            SET name = %s, phone = %s, email = %s, address = %s, contact_group = %s, birthday = %s
            WHERE id = %s
        """, (name, phone, email, address, group, birthday, contact_id))
        conn.commit()

    @staticmethod
    def soft_delete_contact(contact_id):
        cur.execute("SELECT id, name, phone, email, address, contact_group, birthday FROM contacts WHERE id = %s", (contact_id,))
        row = cur.fetchone()
        if row:
            cur.execute("""
                INSERT OR REPLACE INTO deleted_contacts (id, name, phone, email, address, contact_group, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """ if DB_ENGINE == "sqlite" else """
                INSERT INTO deleted_contacts (id, name, phone, email, address, contact_group, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    phone = EXCLUDED.phone,
                    email = EXCLUDED.email,
                    address = EXCLUDED.address,
                    contact_group = EXCLUDED.contact_group,
                    birthday = EXCLUDED.birthday
            """, row)
            cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()

    @staticmethod
    def restore_contact(contact_id):
        cur.execute("SELECT id, name, phone, email, address, contact_group, birthday FROM deleted_contacts WHERE id = %s", (contact_id,))
        row = cur.fetchone()
        if row:
            cur.execute("""
                INSERT OR REPLACE INTO contacts (id, name, phone, email, address, contact_group, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """ if DB_ENGINE == "sqlite" else """
                INSERT INTO contacts (id, name, phone, email, address, contact_group, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, row)
            cur.execute("DELETE FROM deleted_contacts WHERE id = %s", (contact_id,))
            conn.commit()

    @staticmethod
    def permanent_delete(contact_id):
        cur.execute("DELETE FROM deleted_contacts WHERE id = %s", (contact_id,))
        conn.commit()

    @staticmethod
    def empty_trash():
        cur.execute("DELETE FROM deleted_contacts")
        conn.commit()

    @staticmethod
    def get_deleted_contacts():
        cur.execute("SELECT id, name, phone, email, address, contact_group, deleted_at FROM deleted_contacts ORDER BY id DESC")
        return cur.fetchall()

# UI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1020x680")
app.minsize(880, 580)
app.title("Digital Contact Book")