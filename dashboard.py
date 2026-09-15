import customtkinter as ctk
from config import app, DBHelper
from theme import COLORS, get_avatar_color, get_initials, get_group_style, open_whatsapp


def render_dashboard_view(parent, on_navigate_contacts=None, on_navigate_add=None, on_navigate_trash=None):
    """Renders the modern Dashboard overview with metrics, quick actions, and recent contacts."""
    for widget in parent.winfo_children():
        widget.destroy()

    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=25, pady=20)

    # 1. Header & Welcome
    header_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    welcome_title = ctk.CTkLabel(
        header_frame,
        text="👋 Welcome to Digital Contact Book",
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w"
    )
    welcome_title.pack(anchor="w")

    welcome_sub = ctk.CTkLabel(
        header_frame,
        text="Manage, organize, and quickly reach out to your connections. • Created by Sahil, Litto and Anant",
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    )
    welcome_sub.pack(anchor="w", pady=(3, 0))

    # Fetch stats
    stats = DBHelper.get_stats()

    # 2. Metric Cards Row
    metrics_row = ctk.CTkFrame(scroll, fg_color="transparent")
    metrics_row.pack(fill="x", pady=(0, 20))

    # Configure grid columns
    for i in range(4):
        metrics_row.columnconfigure(i, weight=1)

    cards_data = [
        {"icon": "📇", "title": "Total Contacts", "value": str(stats["total"]), "color": COLORS["primary"], "col": 0},
        {"icon": "👨‍👩‍👧", "title": "Family", "value": str(stats["family"]), "color": "#8B5CF6", "col": 1},
        {"icon": "💼", "title": "Work", "value": str(stats["work"]), "color": "#3B82F6", "col": 2},
        {"icon": "🤝", "title": "Friends", "value": str(stats["friends"]), "color": "#10B981", "col": 3},
    ]

    for item in cards_data:
        m_card = ctk.CTkFrame(
            metrics_row,
            corner_radius=12,
            fg_color=("#FFFFFF", "#1C202C")
        )
        m_card.grid(row=0, column=item["col"], padx=6, sticky="nsew")

        top_line = ctk.CTkFrame(m_card, fg_color="transparent")
        top_line.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(
            top_line,
            text=item["icon"],
            font=ctk.CTkFont(size=22)
        ).pack(side="left")

        ctk.CTkLabel(
            top_line,
            text=item["title"],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            m_card,
            text=item["value"],
            font=ctk.CTkFont(size=30, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=16, pady=(0, 16))

    # 3. Quick Actions Bar
    actions_card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    actions_card.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        actions_card,
        text="⚡ Quick Actions",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(fill="x", padx=18, pady=(14, 10))

    btn_bar = ctk.CTkFrame(actions_card, fg_color="transparent")
    btn_bar.pack(fill="x", padx=18, pady=(0, 16))

    if on_navigate_add:
        ctk.CTkButton(
            btn_bar,
            text="➕ Add New Contact",
            height=38,
            corner_radius=8,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=on_navigate_add
        ).pack(side="left", padx=(0, 10))

    if on_navigate_contacts:
        ctk.CTkButton(
            btn_bar,
            text="👥 View All Contacts",
            height=38,
            corner_radius=8,
            fg_color=("#F1F5F9", "#282E3E"),
            text_color=("#0F172A", "#E2E8F0"),
            hover_color=("#E2E8F0", "#384157"),
            font=ctk.CTkFont(size=13),
            command=on_navigate_contacts
        ).pack(side="left", padx=(0, 10))

    if on_navigate_trash:
        trash_count = stats.get("trash", 0)
        ctk.CTkButton(
            btn_bar,
            text=f"🗑️ Recycle Bin ({trash_count})",
            height=38,
            corner_radius=8,
            fg_color=("#F1F5F9", "#282E3E"),
            text_color=("#0F172A", "#E2E8F0"),
            hover_color=("#E2E8F0", "#384157"),
            font=ctk.CTkFont(size=13),
            command=on_navigate_trash
        ).pack(side="left")

    # 4. Recent Contacts Section
    recent_section = ctk.CTkFrame(scroll, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    recent_section.pack(fill="both", expand=True)

    sec_header = ctk.CTkFrame(recent_section, fg_color="transparent")
    sec_header.pack(fill="x", padx=18, pady=(16, 12))

    ctk.CTkLabel(
        sec_header,
        text="⏱️ Recently Added Contacts",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(side="left")

    if on_navigate_contacts:
        ctk.CTkButton(
            sec_header,
            text="See all →",
            height=28,
            width=70,
            fg_color="transparent",
            text_color=COLORS["primary"],
            hover_color=("#F1F5F9", "#282E3E"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=on_navigate_contacts
        ).pack(side="right")

    contacts = DBHelper.get_contacts()[:6]

    if not contacts:
        ctk.CTkLabel(
            recent_section,
            text="No contacts yet. Click 'Add New Contact' above to get started!",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=30)
    else:
        for row in contacts:
            cid, name, phone, email, address, grp, bday = row
            grp_name = grp or "Other"
            grp_style = get_group_style(grp_name)

            row_frame = ctk.CTkFrame(
                recent_section,
                fg_color=("#F8FAFC", "#161922"),
                corner_radius=8
            )
            row_frame.pack(fill="x", padx=18, pady=4)

            # Mini avatar
            avatar_btn = ctk.CTkButton(
                row_frame,
                text=get_initials(name),
                width=38,
                height=38,
                corner_radius=19,
                fg_color=get_avatar_color(name),
                font=ctk.CTkFont(size=13, weight="bold"),
                state="disabled"
            )
            avatar_btn.pack(side="left", padx=(10, 12), pady=8)

            # Name & Group
            info_f = ctk.CTkFrame(row_frame, fg_color="transparent")
            info_f.pack(side="left", fill="both", expand=True)

            line1 = ctk.CTkFrame(info_f, fg_color="transparent")
            line1.pack(fill="x", anchor="w")

            ctk.CTkLabel(
                line1,
                text=name,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(side="left")

            badge = ctk.CTkLabel(
                line1,
                text=f" {grp_name} ",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=grp_style["bg"],
                text_color=grp_style["fg"],
                corner_radius=4
            )
            badge.pack(side="left", padx=8)

            ctk.CTkLabel(
                info_f,
                text=f"📞 {phone}   ✉️ {email or 'No email'}",
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(anchor="w", pady=(1, 0))

            # Copy button
            def copy_num(p=phone, n=name):
                app.clipboard_clear()
                app.clipboard_append(p)

            # WhatsApp button
            wa_btn = ctk.CTkButton(
                row_frame,
                text="💬",
                width=34,
                height=30,
                corner_radius=6,
                fg_color=COLORS["whatsapp"],
                hover_color=COLORS["whatsapp_hover"],
                text_color="#FFFFFF",
                command=lambda p=phone: open_whatsapp(p)
            )
            wa_btn.pack(side="right", padx=(4, 12), pady=8)

            copy_btn = ctk.CTkButton(
                row_frame,
                text="📋",
                width=34,
                height=30,
                corner_radius=6,
                fg_color=("#FFFFFF", "#282E3E"),
                text_color=("#0F172A", "#E2E8F0"),
                hover_color=("#E2E8F0", "#384157"),
                command=copy_num
            )
            copy_btn.pack(side="right", padx=(4, 0), pady=8)

    ctk.CTkFrame(recent_section, height=12, fg_color="transparent").pack()


def dashboard():
    """Fallback standalone window for dashboard."""
    modal = ctk.CTkToplevel(app)
    modal.geometry("750x600")
    modal.title("Dashboard")
    modal.transient(app)
    render_dashboard_view(modal)