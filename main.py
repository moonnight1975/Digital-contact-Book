import customtkinter as ctk
from config import app, DB_ENGINE, DBHelper
from theme import COLORS
from dashboard import render_dashboard_view
from view import render_view_contacts, render_trash_view
from add import render_add_view
from setting import render_setting_view
from events import render_events_view

# Configure root window appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app.geometry("1060x680")
app.minsize(920, 600)
app.title("Digital Contact Book")

# Main horizontal layout: Sidebar (left) + Viewport (right)
sidebar = ctk.CTkFrame(
    app,
    width=240,
    corner_radius=0,
    fg_color=("#F1F5F9", "#161922")
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content_viewport = ctk.CTkFrame(
    app,
    corner_radius=0,
    fg_color=("#F8FAFC", "#0F1117")
)
content_viewport.pack(side="right", fill="both", expand=True)

# --- Sidebar Header / Branding ---
brand_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
brand_frame.pack(fill="x", padx=18, pady=(24, 18))

icon_box = ctk.CTkButton(
    brand_frame,
    text="📇",
    width=44,
    height=44,
    corner_radius=12,
    fg_color=COLORS["primary"],
    font=ctk.CTkFont(size=20),
    state="disabled"
)
icon_box.pack(side="left")

brand_text_box = ctk.CTkFrame(brand_frame, fg_color="transparent")
brand_text_box.pack(side="left", padx=(10, 0))

ctk.CTkLabel(
    brand_text_box,
    text="Contact Book",
    font=ctk.CTkFont(size=16, weight="bold"),
    anchor="w"
).pack(anchor="w")

ctk.CTkLabel(
    brand_text_box,
    text="v2.0 Modern Edition",
    font=ctk.CTkFont(size=11),
    text_color="gray",
    anchor="w"
).pack(anchor="w")

# Divider
ctk.CTkFrame(sidebar, height=1, fg_color=("#E2E8F0", "#262C3D")).pack(fill="x", padx=16, pady=(0, 16))

# --- Navigation Menu ---
nav_buttons = {}
current_view = {"name": None}


def set_active_button(target_key):
    for key, btn in nav_buttons.items():
        if key == target_key:
            btn.configure(
                fg_color=COLORS["primary"],
                text_color="#FFFFFF",
                hover_color=COLORS["primary_hover"]
            )
        else:
            btn.configure(
                fg_color="transparent",
                text_color=("#1E293B", "#CBD5E1"),
                hover_color=("#E2E8F0", "#222736")
            )


def navigate_to(view_key, edit_data=None):
    current_view["name"] = view_key
    set_active_button(view_key)

    if view_key == "dashboard":
        render_dashboard_view(
            content_viewport,
            on_navigate_contacts=lambda: navigate_to("contacts"),
            on_navigate_add=lambda: navigate_to("add"),
            on_navigate_trash=lambda: navigate_to("trash")
        )
    elif view_key == "contacts":
        render_view_contacts(
            content_viewport,
            on_navigate_add=lambda: navigate_to("add"),
            on_edit_contact=lambda data: navigate_to("add", edit_data=data)
        )
    elif view_key == "add":
        render_add_view(
            content_viewport,
            on_saved=lambda: navigate_to("contacts"),
            edit_data=edit_data
        )
    elif view_key == "events":
        render_events_view(content_viewport)
    elif view_key == "trash":
        render_trash_view(
            content_viewport,
            on_restored=update_sidebar_stats
        )
    elif view_key == "settings":
        render_setting_view(content_viewport)

    update_sidebar_stats()


# Build Menu Buttons
menu_items = [
    ("dashboard", "📊  Dashboard"),
    ("contacts", "👥  All Contacts"),
    ("add", "➕  Add Contact"),
    ("events", "📅  Events & Dates"),
    ("trash", "🗑️  Recycle Bin"),
    ("settings", "⚙️  Settings"),
]

for key, text in menu_items:
    btn = ctk.CTkButton(
        sidebar,
        text=text,
        anchor="w",
        height=40,
        corner_radius=8,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="transparent",
        command=lambda k=key: navigate_to(k)
    )
    btn.pack(fill="x", padx=12, pady=3)
    nav_buttons[key] = btn

# Spacer to push footer to bottom
spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
spacer.pack(fill="both", expand=True)

# --- Sidebar Footer ---
footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
footer_frame.pack(fill="x", padx=16, pady=(0, 16))

# Divider
ctk.CTkFrame(sidebar, height=1, fg_color=("#E2E8F0", "#262C3D")).pack(in_=footer_frame, fill="x", pady=(0, 12))

# DB status indicator
db_status_line = ctk.CTkFrame(footer_frame, fg_color="transparent")
db_status_line.pack(fill="x", pady=(0, 6))

status_dot = "🟢"
engine_label = "PostgreSQL" if DB_ENGINE == "postgresql" else "SQLite"

ctk.CTkLabel(
    db_status_line,
    text=f"{status_dot} {engine_label}",
    font=ctk.CTkFont(size=12, weight="bold"),
    text_color=COLORS["success"],
    anchor="w"
).pack(side="left")

contact_count_badge = ctk.CTkLabel(
    db_status_line,
    text="0",
    font=ctk.CTkFont(size=11, weight="bold"),
    fg_color=("#E2E8F0", "#252B3B"),
    corner_radius=6,
    width=32
)
contact_count_badge.pack(side="right")


def update_sidebar_stats():
    try:
        stats = DBHelper.get_stats()
        contact_count_badge.configure(text=str(stats["total"]))
        # Also update trash button text with count if trash > 0
        trash_cnt = stats.get("trash", 0)
        trash_text = f"🗑️  Recycle Bin ({trash_cnt})" if trash_cnt > 0 else "🗑️  Recycle Bin"
        nav_buttons["trash"].configure(text=trash_text)
    except Exception:
        pass


# Quit App Button
quit_btn = ctk.CTkButton(
    footer_frame,
    text="✕  Quit Application",
    height=34,
    corner_radius=6,
    fg_color=("#FEE2E2", "#2B1D22"),
    text_color=COLORS["danger"],
    hover_color=("#FECACA", "#3E252D"),
    font=ctk.CTkFont(size=12),
    command=app.quit
)
quit_btn.pack(fill="x", pady=(6, 0))

# Creator credits
ctk.CTkLabel(
    footer_frame,
    text="Created by Sahil, Litto & Anant",
    font=ctk.CTkFont(size=10),
    text_color="gray"
).pack(pady=(8, 2))

# Center window on screen
app.update_idletasks()
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()
x = (screen_w - 1060) // 2
y = (screen_h - 680) // 2
app.geometry(f"1060x680+{max(0, x)}+{max(0, y)}")

# Initial Navigation
navigate_to("dashboard")

if __name__ == "__main__":
    app.mainloop()
