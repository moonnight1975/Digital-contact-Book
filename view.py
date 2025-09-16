import customtkinter as ctk
# Make sure your config file provides these correctly
from config import conn, cur, app

def view_contact():
    # --- Main Popup Window Setup ---
    view_win = ctk.CTkToplevel(app)
    view_win.geometry("600x450") # Increased size for better layout
    view_win.title("All Contacts")
    view_win.transient(app) # Keeps the popup on top of the main app

    # --- Top frame for controls (filter and buttons) ---
    controls_frame = ctk.CTkFrame(view_win)
    controls_frame.pack(fill="x", padx=10, pady=5)

    # --- Scrollable frame for displaying the contact list ---
    scroll_frame = ctk.CTkScrollableFrame(view_win)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Function to refresh the main contact list ---
    def refresh_view(selected_group="All"):
        # Clear any existing widgets in the scroll frame to prevent duplicates
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        # Fetch contacts from the database based on the selected group
        if selected_group == "All":
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM contacts ORDER BY name")
        else:
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM contacts WHERE contact_group = %s ORDER BY name", (selected_group,))

        rows = cur.fetchall()

        # Display a message if no contacts are found
        if not rows:
            ctk.CTkLabel(scroll_frame, text="No contacts found in this group.", font=ctk.CTkFont(size=14)).pack(pady=20)
            return

        # Create and display a row for each contact
        for row in rows:
            # A frame for each contact row to hold the label and buttons
            contact_row_frame = ctk.CTkFrame(scroll_frame)
            contact_row_frame.pack(fill="x", pady=4, padx=5)

            contact_text = f"👤 {row[1]}  |  📞 {row[2]}  |  🏠 Group: {row[5]}"
            ctk.CTkLabel(contact_row_frame, text=contact_text, anchor="w").pack(side="left", padx=10, pady=10)

    # --- Hover effects for buttons ---
    def hover_in(btn):
        btn.configure(fg_color="#5A5A5A") # A slightly lighter grey for hover

    def hover_out(btn):
        btn.configure(fg_color="#3A3A3A") # A standard dark grey

    # --- Function to show the "Recently Deleted" window ---
    def show_recently_deleted():
        deleted_win = ctk.CTkToplevel(view_win)
        deleted_win.geometry("550x400")
        deleted_win.title("Recently Deleted")
        deleted_win.transient(view_win) # Keep this window on top of the contacts view

        deleted_scroll_frame = ctk.CTkScrollableFrame(deleted_win)
        deleted_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Action to restore a contact (defined once)
        def restore_contact_action(contact_id):
            # Find the contact in the deleted table
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM deleted_contacts WHERE id = %s", (contact_id,))
            contact_data = cur.fetchone()

            if contact_data:
                # Insert it back into the main contacts table
                cur.execute("""
                            INSERT INTO contacts (id, name, phone, email, address, contact_group)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """, contact_data)
                # Remove it from the deleted table
                cur.execute("DELETE FROM deleted_contacts WHERE id = %s", (contact_id,))
                conn.commit()
                refresh_deleted_contacts() # Refresh the deleted list
                refresh_view(group_dropdown.get()) # Refresh the main contact list

        # Function to populate the deleted contacts list
        def refresh_deleted_contacts():
            for widget in deleted_scroll_frame.winfo_children():
                widget.destroy()

            cur.execute("SELECT id, name, phone, contact_group FROM deleted_contacts ORDER BY name")
            rows = cur.fetchall()

            if not rows:
                ctk.CTkLabel(deleted_scroll_frame, text="No recently deleted contacts.").pack(pady=20)
                return

            for row in rows:
                row_frame = ctk.CTkFrame(deleted_scroll_frame)
                row_frame.pack(fill="x", pady=4, padx=5)

                contact_text = f"👤 {row[1]}  |  📞 {row[2]}  |  🏠 Group: {row[3]}"
                ctk.CTkLabel(row_frame, text=contact_text, anchor="w").pack(side="left", padx=10, pady=10)

                # **FIXED**: Used a lambda function to correctly pass the contact_id for this specific row
                restore_btn = ctk.CTkButton(
                    row_frame, text="Restore",
                    command=lambda cid=row[0]: restore_contact_action(cid),
                    fg_color="#3A3A3A"
                )
                restore_btn.pack(side="right", padx=10, pady=5)
                restore_btn.bind("<Enter>", lambda e, b=restore_btn: hover_in(b))
                restore_btn.bind("<Leave>", lambda e, b=restore_btn: hover_out(b))

        refresh_deleted_contacts()

    # --- Widgets for the top controls frame ---

    # Filter dropdown menu
    group_dropdown = ctk.CTkOptionMenu(
        controls_frame,
        values=["All", "Family", "Work", "Friends", "Other"],
        command=refresh_view
    )
    group_dropdown.set("All")
    group_dropdown.pack(side="left", padx=10, pady=10)

    # "Recently Deleted" button
    re_btn = ctk.CTkButton(controls_frame, text="Recently Deleted", command=show_recently_deleted, fg_color="#3A3A3A")
    re_btn.pack(side="right", padx=10, pady=10)
    re_btn.bind("<Enter>", lambda e: hover_in(re_btn))
    re_btn.bind("<Leave>", lambda e: hover_out(re_btn))

    # --- Initial Load of Contacts ---
    refresh_view("All")