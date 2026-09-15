import customtkinter as ctk
from config import app, DB_ENGINE, DB_PATH, DBHelper
from theme import COLORS


def render_setting_view(parent):
    """Renders the modern Settings & Preferences view inside parent."""
    for widget in parent.winfo_children():
        widget.destroy()

    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=25, pady=20)

    # Header
    header_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    title_label = ctk.CTkLabel(
        header_frame,
        text="⚙️ Preferences & Settings",
        font=ctk.CTkFont(size=22, weight="bold"),
        anchor="w"
    )
    title_label.pack(anchor="w")

    sub_label = ctk.CTkLabel(
        header_frame,
        text="Customize appearance, check database status, and view application info.",
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    )
    sub_label.pack(anchor="w", pady=(2, 0))

    # --- Section 1: Appearance ---
    app_card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    app_card.pack(fill="x", pady=(0, 16))

    ctk.CTkLabel(
        app_card,
        text="🎨 Appearance Mode",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(fill="x", padx=20, pady=(16, 4))

    ctk.CTkLabel(
        app_card,
        text="Select your preferred UI color scheme (Dark, Light, or System default).",
        font=ctk.CTkFont(size=12),
        text_color="gray",
        anchor="w"
    ).pack(fill="x", padx=20, pady=(0, 12))

    def on_mode_change(mode):
        ctk.set_appearance_mode(mode.lower())

    mode_seg = ctk.CTkSegmentedButton(
        app_card,
        values=["Dark", "Light", "System"],
        command=on_mode_change,
        height=36,
        selected_color=COLORS["primary"],
        selected_hover_color=COLORS["primary_hover"]
    )
    current_mode = ctk.get_appearance_mode().capitalize()
    mode_seg.set(current_mode if current_mode in ["Dark", "Light", "System"] else "Dark")
    mode_seg.pack(padx=20, pady=(0, 20), anchor="w")

    # --- Section 2: Database Status & Diagnostic ---
    db_card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    db_card.pack(fill="x", pady=(0, 16))

    ctk.CTkLabel(
        db_card,
        text="🗄️ Database Information",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(fill="x", padx=20, pady=(16, 4))

    stats = DBHelper.get_stats()

    info_grid = ctk.CTkFrame(db_card, fg_color="transparent")
    info_grid.pack(fill="x", padx=20, pady=(4, 20))

    def add_info_row(f, label, val, is_badge=False):
        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(fill="x", pady=4)
        ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="gray", width=140, anchor="w").pack(side="left")
        if is_badge:
            ctk.CTkLabel(
                row,
                text=f" {val} ",
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=COLORS["success"],
                text_color="#FFFFFF",
                corner_radius=4
            ).pack(side="left")
        else:
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=12), anchor="w").pack(side="left")

    engine_name = "SQLite Database (Local Embedded)" if DB_ENGINE == "sqlite" else "PostgreSQL Database (Network)"
    add_info_row(info_grid, "Engine:", engine_name, is_badge=True)
    add_info_row(info_grid, "Storage Location:", DB_PATH if DB_ENGINE == "sqlite" else "localhost:5432 / mydb")
    add_info_row(info_grid, "Active Contacts:", str(stats["total"]))
    add_info_row(info_grid, "Recycle Bin Items:", str(stats["trash"]))

    # --- Section 3: About ---
    about_card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    about_card.pack(fill="x", pady=(0, 16))

    ctk.CTkLabel(
        about_card,
        text="ℹ️ About Digital Contact Book",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(fill="x", padx=20, pady=(16, 4))

    about_text = (
        "Digital Contact Book — Modern Desktop Edition\n"
        "Version: 2.0.0\n"
        "Created by Sahil, Litto and Anant\n\n"
        "Features: Unified single-window dashboard, live contact search, contact categorization, "
        "smart avatars, soft delete & trash recovery, and seamless dual-engine database resilience."
    )

    ctk.CTkLabel(
        about_card,
        text=about_text,
        font=ctk.CTkFont(size=12),
        text_color="gray",
        justify="left",
        anchor="w"
    ).pack(fill="x", padx=20, pady=(4, 20))


def setting():
    """Fallback standalone window for settings."""
    modal = ctk.CTkToplevel(app)
    modal.geometry("600x550")
    modal.title("Preferences & Settings")
    modal.transient(app)
    render_setting_view(modal)