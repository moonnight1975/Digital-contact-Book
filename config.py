import customtkinter as ctk
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="mydb",
    user="postgres",
    password="litto",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Ensure contacts table exists with contact_group
cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                                                    id SERIAL PRIMARY KEY,
                                                    name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                address TEXT,
                contact_group VARCHAR(50) DEFAULT 'Other'
                )
            """)
conn.commit()

# Tkinter app setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x500")
app.title("Digital Contact Book")
