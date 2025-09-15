import customtkinter as ctk

from events import events
from setting import setting
from config import app   # main app instance
from add import add_contact
from view import view_contact
from dashboard import dashboard

# Main label
label = ctk.CTkLabel(app, text="Hello There", font=("Arial", 30), text_color="white")
label.pack(pady=20)

# --- Functions ---
def delete_contact_placeholder():
    label.configure(text="Deleting contact (placeholder)")
    # Future DB delete logic goes here


# --- Buttons ---
add_btn = ctk.CTkButton(
    app,
    text="Add Contact",
    command=add_contact,
    fg_color="blue",
    hover_color="green",
    text_color="white"
)
add_btn.pack(pady=20)

view_btn = ctk.CTkButton(
    app,
    text="View Contacts",
    command=view_contact,
    fg_color="blue",
    hover_color="green",
    text_color="white"
)
view_btn.pack(pady=20)

dashboard_btn = ctk.CTkButton(
    app,
    text="Dashboard",
    command=dashboard,
    fg_color="blue",
    hover_color="green",
    text_color="white"
)
dashboard_btn.pack(pady=20)

setting_btn = ctk.CTkButton(
    app,
    text="Settings",
    command=setting,
    fg_color="blue",
    hover_color="green",
    text_color="white"
)
setting_btn.pack(pady=20)

group_btn = ctk.CTkButton(
    app,
    text="Events ",
    command=events,
    fg_color="blue",
    hover_color="green",
    text_color="white"
)
group_btn.pack(pady=20)

# --- Run app ---
app.mainloop()
