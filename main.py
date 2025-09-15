import customtkinter as ctk

from setting import setting
from config import app   # main app instance
from add import add_contact
from view import view_contact
from dashboard import dashboard

# Main label
label = ctk.CTkLabel(app, text="Hello There", font=("Arial", 30), text_color="blue")
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
    fg_color="grey",
    hover_color="green",
    text_color="black"
)
add_btn.pack(pady=20)

view_btn = ctk.CTkButton(
    app,
    text="View Contacts",
    command=view_contact,
    fg_color="grey",
    hover_color="green",
    text_color="black"
)
view_btn.pack(pady=20)

dashboard_btn = ctk.CTkButton(
    app,
    text="Dashboard",
    command=dashboard,
    fg_color="grey",
    hover_color="green",
    text_color="black"
)
dashboard_btn.pack(pady=20)

setting_btn = ctk.CTkButton(
    app,
    text="Settings",
    command=setting,
    fg_color="grey",
    hover_color="green",
    text_color="black"
)
setting_btn.pack(pady=20)

group_btn = ctk.CTkButton(
    app,
    text="Groups ",
    command=lambda: label.configure(text="Groups feature coming soon!"),
    fg_color="grey",
    hover_color="green",
    text_color="black"
)
group_btn.pack(pady=20)

# --- Run app ---
app.mainloop()
