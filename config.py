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

# Tkinter app setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.geometry("600x500")
app.title("Digital Contact Book")
