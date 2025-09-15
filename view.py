import customtkinter as ctk
from config import conn, cur, app

def view_contact():
    # Create a popup window
    view_win = ctk.CTkToplevel(app)
    view_win.geometry("500x400")
    view_win.title("All Contacts")
    row_frame = ctk.CTkFrame(view_win)
    row_frame.pack(fill="x", pady=5, padx=5)

    # Dropdown filter for groups
    def refresh_view(selected_group="All"):
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        if selected_group == "All":
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM contacts")
        else:
            cur.execute("SELECT id, name, phone, email, address, contact_group FROM contacts WHERE contact_group = %s", (selected_group,))

        rows = cur.fetchall()

        if not rows:
            ctk.CTkLabel(scroll_frame, text="No contacts found").pack(pady=10)
            return

        for row in rows:
            contact_text = f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3] or ''} | {row[4] or ''} | Group: {row[5]}"
            ctk.CTkLabel(scroll_frame, text=contact_text, anchor="w", justify="left").pack(pady=5, fill="x")

    # Filter dropdown
    group_dropdown = ctk.CTkOptionMenu(row_frame, values=["All", "Family", "Work", "Friends", "Other"], command=refresh_view)
    group_dropdown.set("All")
    group_dropdown.pack(pady=10)

    # Add a scrollable frame to show contacts
    scroll_frame = ctk.CTkScrollableFrame(view_win, width=480, height=300)
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Initial load
    refresh_view("All")

    # Hover effects
    def hover_in(btn):
        btn.configure(fg_color="darkgrey")

    def hover_out(btn):
        btn.configure(fg_color="grey")

    # Recently Deleted
    def show_recently_deleted():
        deleted_win = ctk.CTkToplevel(view_win)
        deleted_win.geometry("500x400")
        deleted_win.title("Recently Deleted")

        deleted_scroll_frame = ctk.CTkScrollableFrame(deleted_win)
        deleted_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_deleted_contacts():
            for widget in deleted_scroll_frame.winfo_children():
                widget.destroy()

            cur.execute("SELECT id, name, phone, email, address, contact_group FROM deleted_contacts")
            rows = cur.fetchall()

            if not rows:
                ctk.CTkLabel(deleted_scroll_frame, text="No recently deleted contacts").pack(pady=10)
                return

            for row in rows:
                row_frame = ctk.CTkFrame(deleted_scroll_frame)
                row_frame.pack(fill="x", pady=5, padx=5)

                contact_text = f"ID: {row[0]} | {row[1]} ({row[2]}) | Group: {row[5]}"
                ctk.CTkLabel(row_frame, text=contact_text, anchor="w").pack(side="left", padx=5)

                def restore_contact(contact_id=row[0]):
                    cur.execute("SELECT id, name, phone, email, address, contact_group FROM deleted_contacts WHERE id = %s", (contact_id,))
                    contact_data = cur.fetchone()

                    if contact_data:
                        cur.execute("""
                                    INSERT INTO contacts (id, name, phone, email, address, contact_group)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    """, contact_data)
                        cur.execute("DELETE FROM deleted_contacts WHERE id = %s", (contact_id,))
                        conn.commit()
                        refresh_deleted_contacts()
                        refresh_view() # Refresh main view

                restore_btn = ctk.CTkButton(row_frame, text="Restore", command=restore_contact, fg_color="grey")
                restore_btn.pack(side="right", padx=5)
                restore_btn.bind("<Enter>", lambda e, b=restore_btn: hover_in(b))
                restore_btn.bind("<Leave>", lambda e, b=restore_btn: hover_out(b))

        refresh_deleted_contacts()

    re_btn = ctk.CTkButton(row_frame, text="Recently deleted", command=show_recently_deleted, fg_color="grey")
    re_btn.pack(side="right",pady=10)
    re_btn.bind("<Enter>", lambda e: hover_in(re_btn))
    re_btn.bind("<Leave>", lambda e: hover_out(re_btn))