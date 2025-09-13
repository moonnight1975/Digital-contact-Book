import customtkinter as ctk
from config import conn, cur, app

# Create table if it doesn't exist
cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                                                    id SERIAL PRIMARY KEY,
                                                    name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                address TEXT
                )
            """)
conn.commit()

def add_contact():
    new_win = ctk.CTkToplevel(app)   # new window for adding contacts
    new_win.geometry("400x400")
    new_win.title("Add Contact")

    ctk.CTkLabel(new_win, text="Add Contact Details", font=("Arial", 20)).pack(pady=20)

    name_entry = ctk.CTkEntry(new_win, placeholder_text="Enter name")
    name_entry.pack(pady=10)

    phone_entry = ctk.CTkEntry(new_win, placeholder_text="Enter phone number")
    phone_entry.pack(pady=10)

    address_entry = ctk.CTkEntry(new_win, placeholder_text="Enter address")
    address_entry.pack(pady=10)

    email_entry = ctk.CTkEntry(new_win, placeholder_text="Enter email")
    email_entry.pack(pady=10)

    def submit_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        email = email_entry.get()

        if name and phone:
            try:
                cur.execute(
                    "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)",
                    (name, phone, email, address)
                )
                conn.commit()
                ctk.CTkLabel(new_win, text=f"{name} added successfully!", text_color="green").pack(pady=5)

                # Clear entries
                name_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                address_entry.delete(0, 'end')
                email_entry.delete(0, 'end')

            except Exception as err:
                ctk.CTkLabel(new_win, text=f"Error: {err}", text_color="red").pack(pady=5)
        else:
            ctk.CTkLabel(new_win, text="Name and Phone are required.", text_color="red").pack(pady=5)

    submit_btn = ctk.CTkButton(new_win, text="Submit", command=submit_contact)
    submit_btn.pack(pady=20)
