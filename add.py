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
        placeholder_text="Enter name"
    )
    name_entry.pack(pady=10)

    # Phone entry - WITHOUT textvariable initially
    phone_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter phone number"
    )
    phone_entry.pack(pady=10)

    # Add validation to phone entry
    def validate_phone(event):
        current = phone_entry.get()
        # Keep only digits
        filtered = ''.join(filter(str.isdigit, current))
        if current != filtered:
            phone_entry.delete(0, 'end')
            phone_entry.insert(0, filtered)

    phone_entry.bind('<KeyRelease>', validate_phone)

    # Address entry
    address_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter address"
    )
    address_entry.pack(pady=10)

    # Email entry
    email_entry = ctk.CTkEntry(
        new_win,
        placeholder_text="Enter email"
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
        phone = phone_entry.get()
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

                # Create success message
                success_label = ctk.CTkLabel(
                    new_win,
                    text=f"{name} added successfully to group {group}",
                    text_color="green"
                )
                success_label.pack(pady=5)

                # Clear fields properly
                name_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                address_entry.delete(0, 'end')
                email_entry.delete(0, 'end')
                group_dropdown.set("Other")

                # Remove success message after 3 seconds
                new_win.after(3000, success_label.destroy)

            except Exception as err:
                error_label = ctk.CTkLabel(
                    new_win,
                    text=f"Error: {err}",
                    text_color="red"
                )
                error_label.pack(pady=5)
                # Remove error message after 3 seconds
                new_win.after(3000, error_label.destroy)
        else:
            error_label = ctk.CTkLabel(
                new_win,
                text="Name and Phone are required.",
                text_color="red"
            )
            error_label.pack(pady=5)
            # Remove error message after 3 seconds
            new_win.after(3000, error_label.destroy)

    # Submit button
    submit_btn = ctk.CTkButton(new_win, text="Submit", command=submit_contact)
    submit_btn.pack(pady=20)