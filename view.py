import customtkinter as ctk
from config import conn, cur, app

def view_contact():
    # Create a popup window
    view_win = ctk.CTkToplevel(app)
    view_win.geometry("500x400")
    view_win.title("All Contacts")

    # Scrollable frame for contacts
    scroll_frame = ctk.CTkScrollableFrame(view_win, width=480, height=350)
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    cur.execute("SELECT id, name, phone, email, address FROM contacts")
    rows = cur.fetchall()

    if not rows:
        ctk.CTkLabel(scroll_frame, text="No contacts found").pack(pady=10)
        return

    # Display each contact
    for row in rows:
        contact_text = f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3] or ''} | {row[4] or ''}"
        ctk.CTkLabel(scroll_frame, text=contact_text, anchor="w", justify="left").pack(pady=5, fill="x")
