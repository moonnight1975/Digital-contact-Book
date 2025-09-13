import customtkinter as ctk
from config import conn, cur, app
from add import add_contact



def dashboard():
    # Dashboard window
    dash_win = ctk.CTkToplevel(app)
    dash_win.geometry("700x500")
    dash_win.title("Dashboard")

    # Left frame: buttons
    button_frame = ctk.CTkFrame(dash_win, width=200)
    button_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Right frame: scrollable contact list
    contact_frame = ctk.CTkScrollableFrame(dash_win)
    contact_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Hover animation helpers
    def hover_in(widget):
        widget.configure(fg_color="green")
    def hover_out(widget):
        widget.configure(fg_color="grey")

    # Refresh contacts
    def refresh_contacts():
        for widget in contact_frame.winfo_children():
            widget.destroy()

        cur.execute("SELECT id, name, phone, email, address FROM contacts")
        rows = cur.fetchall()

        if not rows:
            ctk.CTkLabel(contact_frame, text="No contacts found").pack(pady=10)
            return

        for row in rows:
            row_frame = ctk.CTkFrame(contact_frame)
            row_frame.pack(fill="x", pady=5, padx=5)

            contact_text = f"{row[1]} ({row[2]}) | {row[3] or ''} | {row[4] or ''}"
            ctk.CTkLabel(row_frame, text=contact_text, anchor="w").pack(side="left", padx=5)

            # Delete button with hover
            def delete_contact(contact_id=row[0]):
                cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
                conn.commit()
                refresh_contacts()

            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60, command=delete_contact)
            delete_btn.pack(side="right", padx=5)
            delete_btn.bind("<Enter>", lambda e, b=delete_btn: hover_in(b))
            delete_btn.bind("<Leave>", lambda e, b=delete_btn: hover_out(b))

    # Add and Refresh buttons on left frame
    add_btn = ctk.CTkButton(button_frame, text="Add Contact", command=add_contact, fg_color="grey")
    add_btn.pack(pady=10, fill="x")
    add_btn.bind("<Enter>", lambda e: hover_in(add_btn))
    add_btn.bind("<Leave>", lambda e: hover_out(add_btn))

    refresh_btn = ctk.CTkButton(button_frame, text="Refresh Contacts", command=refresh_contacts, fg_color="grey")
    refresh_btn.pack(pady=10, fill="x")
    refresh_btn.bind("<Enter>", lambda e: hover_in(refresh_btn))
    refresh_btn.bind("<Leave>", lambda e: hover_out(refresh_btn))

    # Slide-in animation for right panel
    def slide_in(widget, start_x=-700, target_x=200, step=20):
        x = start_x
        widget.place(x=x, y=0, relheight=1)
        def animate():
            nonlocal x
            if x < target_x:
                x += step
                widget.place(x=x, y=0, relheight=1)
                widget.after(20, animate)
            else:
                widget.place(x=target_x, y=0, relheight=1)
        animate()

    # Initial load and optional slide-in
    refresh_contacts()
    # Uncomment to see slide-in effect:
    # slide_in(contact_frame)
