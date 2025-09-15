import customtkinter as ctk
from config import conn, cur, app

def view_contact():
    # Create a popup window
    view_win = ctk.CTkToplevel(app)
    view_win.geometry("500x400")
    view_win.title("All Contacts")

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
    group_dropdown = ctk.CTkOptionMenu(view_win, values=["All", "Family", "Work", "Friends", "Other"], command=refresh_view)
    group_dropdown.set("All")
    group_dropdown.pack(pady=10)

    # Add a scrollable frame to show contacts
    scroll_frame = ctk.CTkScrollableFrame(view_win, width=480, height=300)
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Initial load
    refresh_view("All")
