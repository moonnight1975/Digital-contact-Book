import customtkinter as ctk
from config import conn, cur, app
from add import add_contact

def dashboard():
    dash_win = ctk.CTkToplevel(app)
    dash_win.geometry("700x500")
    dash_win.title("Dashboard")

    # Left frame: buttons
    button_frame = ctk.CTkFrame(dash_win, width=200)
    button_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Right frame: contact list
    contact_frame = ctk.CTkScrollableFrame(dash_win)
    contact_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Hover animations
    def hover_in(widget):
        widget.configure(fg_color="green")
    def hover_out(widget):
        widget.configure(fg_color="grey")

    # Refresh contact list
    def refresh_contacts(selected_group="All"):
        for widget in contact_frame.winfo_children():
            widget.destroy()

        if selected_group == "All":
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM contacts")
        else:
            cur.execute(
                "SELECT id, name, phone, email, address, contact_group FROM contacts WHERE contact_group=%s",
                (selected_group,)
            )
        rows = cur.fetchall()

        if not rows:
            ctk.CTkLabel(contact_frame, text="No contacts found").pack(pady=10)
            return

        for row in rows:
            row_frame = ctk.CTkFrame(contact_frame)
            row_frame.pack(fill="x", pady=5, padx=5)

            contact_text = f"{row[1]} ({row[2]}) | {row[3] or ''} | {row[4] or ''} | Group: {row[5]}"
            label = ctk.CTkLabel(row_frame, text=contact_text, anchor="w")
            label.pack(side="left", padx=5)

            # Delete contact
            def delete_contact(contact_id=row[0]):
                cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
                conn.commit()
                refresh_contacts(selected_group)

            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60, command=delete_contact, fg_color="grey")
            delete_btn.pack(side="right", padx=5)
            delete_btn.bind("<Enter>", lambda e, b=delete_btn: hover_in(b))
            delete_btn.bind("<Leave>", lambda e, b=delete_btn: hover_out(b))

    # Group filter dropdown
    group_var = ctk.StringVar(value="All")
    group_dropdown = ctk.CTkOptionMenu(
        button_frame,
        values=["All", "Family", "Work", "Friends", "Other"],
        variable=group_var,
        command=refresh_contacts
    )
    group_dropdown.pack(pady=10, padx=10, fill="x")

    # Add contact button
    add_btn = ctk.CTkButton(button_frame, text="Add Contact", command=add_contact, fg_color="grey")
    add_btn.pack(pady=10, padx=10, fill="x")
    add_btn.bind("<Enter>", lambda e: hover_in(add_btn))
    add_btn.bind("<Leave>", lambda e: hover_out(add_btn))

    # Initial load
    refresh_contacts()
