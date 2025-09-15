from config import app, conn, cur
import customtkinter as ctk

def add_contact():
    # New window
    new_win = ctk.CTkToplevel(app)
    new_win.geometry("400x500")
    new_win.title("Add Contact")

    ctk.CTkLabel(new_win, text="Add Contact Details", font=("Arial", 20)).pack(pady=20)

    # Name entry
    name_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter name",
        text_color="black",
        placeholder_text_color="gray"
    )
    name_entry.pack(pady=10)

    # Phone entry with StringVar filter
    phone_var = ctk.StringVar()
    def int_only(*args):
        value = phone_var.get()
        if not value.isdigit():  # allow only digits
            phone_var.set(''.join(filter(str.isdigit, value)))
    phone_var.trace_add("write", int_only)

    phone_entry = ctk.CTkEntry(
        new_win,
        textvariable=phone_var,
        placeholder_text="Enter phone number",
        text_color="black",
        placeholder_text_color="gray"
    )
    phone_entry.pack(pady=10)

    # Address entry
    address_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter address",
        text_color="black",
        placeholder_text_color="gray"
    )
    address_entry.pack(pady=10)

    # Email entry
    email_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter email",
        text_color="black",
        placeholder_text_color="gray"
    )
    email_entry.pack(pady=10)

    # Dropdown for group
    group_dropdown = ctk.CTkOptionMenu(
        new_win,
        values=["Family", "Work", "Friends", "Other"]
    )
    group_dropdown.set("Other")
    group_dropdown.pack(pady=20)

    # Submit function
    def submit_contact():
        name = name_entry.get()
        phone = phone_var.get()
        address = address_entry.get()
        email = email_entry.get()
        group = group_dropdown.get()

        if name and phone:
            try:
                cur.execute(
                    """
                    INSERT INTO contacts (name, phone, email, address, contact_group)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name, phone, email, address, group)
                )
                conn.commit()
                ctk.CTkLabel(
                    new_win,
                    text=f"{name} added successfully to group {group}",
                    text_color="green"
                ).pack(pady=5)

                # Clear fields
                name_entry.delete(0, 'end')
                phone_var.set("")
                address_entry.delete(0, 'end')
                email_entry.delete(0, 'end')
                group_dropdown.set("Other")

            except Exception as err:
                ctk.CTkLabel(new_win, text=f"Error: {err}", text_color="red").pack(pady=5)
        else:
            ctk.CTkLabel(new_win, text="Name and Phone are required.", text_color="red").pack(pady=5)

    # Submit button
    submit_btn = ctk.CTkButton(new_win, text="Submit", command=submit_contact)
    submit_btn.pack(pady=20)
