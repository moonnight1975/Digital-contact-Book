import customtkinter as ctk
from config import app, DBHelper
from theme import COLORS, get_avatar_color, get_initials, get_group_style, open_whatsapp


def render_view_contacts(parent, on_navigate_add=None, on_edit_contact=None):
    """
    Renders the modern contact list with live search, group filters,
    and interactive contact cards inside parent.
    """
    for widget in parent.winfo_children():
        widget.destroy()

    # Container
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=25, pady=20)

    # Top Header Row: Title & Action
    top_row = ctk.CTkFrame(container, fg_color="transparent")
    top_row.pack(fill="x", pady=(0, 15))

    title_frame = ctk.CTkFrame(top_row, fg_color="transparent")
    title_frame.pack(side="left")

    title_lbl = ctk.CTkLabel(
        title_frame,
        text="👥 Contacts Directory",
        font=ctk.CTkFont(size=22, weight="bold"),
        anchor="w"
    )
    title_lbl.pack(anchor="w")

    count_lbl = ctk.CTkLabel(
        title_frame,
        text="Loading contacts...",
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    )
    count_lbl.pack(anchor="w", pady=(2, 0))

    if on_navigate_add:
        add_btn = ctk.CTkButton(
            top_row,
            text="➕ New Contact",
            height=36,
            corner_radius=8,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=on_navigate_add
        )
        add_btn.pack(side="right")

    # Search & Filter Row
    filter_row = ctk.CTkFrame(container, fg_color="transparent")
    filter_row.pack(fill="x", pady=(0, 12))

    search_entry = ctk.CTkEntry(
        filter_row,
        placeholder_text="🔍 Search contacts by name, phone, or email...",
        height=38,
        corner_radius=8
    )
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

    current_group_var = ctk.StringVar(value="All")
    group_menu = ctk.CTkOptionMenu(
        filter_row,
        values=["All", "Family", "Work", "Friends", "Other"],
        variable=current_group_var,
        height=38,
        corner_radius=8,
        fg_color=("#E2E8F0", "#2D3446"),
        text_color=("#0F172A", "#F8FAFC"),
        button_color=("#CBD5E1", "#3B445B"),
        command=lambda _: refresh_list()
    )
    group_menu.pack(side="right")

    # Scrollable list frame
    cards_scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
    cards_scroll.pack(fill="both", expand=True)

    # Toast banner inside container for copy/delete actions
    toast_lbl = ctk.CTkLabel(container, text="", font=ctk.CTkFont(size=12))
    toast_lbl.pack(pady=2)

    def show_toast(msg, color=COLORS["success"]):
        toast_lbl.configure(text=msg, text_color=color)
        container.after(3000, lambda: toast_lbl.configure(text=""))

    def copy_to_clipboard(text, label="Text"):
        app.clipboard_clear()
        app.clipboard_append(text)
        show_toast(f"📋 Copied {label} to clipboard!")

    def delete_action(contact_id, contact_name):
        DBHelper.soft_delete_contact(contact_id)
        show_toast(f"🗑️ Moved '{contact_name}' to Recycle Bin", color=COLORS["warning"])
        refresh_list()

    def edit_action(contact_data):
        if on_edit_contact:
            on_edit_contact(contact_data)
        else:
            from add import add_contact
            add_contact(edit_data=contact_data, on_saved=refresh_list)

    def refresh_list(*_):
        search_query = search_entry.get().strip()
        selected_grp = current_group_var.get()
        rows = DBHelper.get_contacts(search=search_query, group=selected_grp)

        # Update count label
        count_lbl.configure(text=f"Showing {len(rows)} {'contact' if len(rows) == 1 else 'contacts'}")

        # Clear existing cards
        for w in cards_scroll.winfo_children():
            w.destroy()

        if not rows:
            empty_frame = ctk.CTkFrame(cards_scroll, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=60)
            ctk.CTkLabel(
                empty_frame,
                text="🔍 No contacts found",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=(0, 6))
            ctk.CTkLabel(
                empty_frame,
                text="Try changing your search query or group filter",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            ).pack()
            return

        for row in rows:
            cid, name, phone, email, address, grp, bday = row
            grp_name = grp or "Other"
            grp_style = get_group_style(grp_name)

            card = ctk.CTkFrame(
                cards_scroll,
                corner_radius=12,
                fg_color=("#FFFFFF", "#1C202C")
            )
            card.pack(fill="x", pady=6, padx=2)

            # Left avatar
            avatar_col = get_avatar_color(name)
            avatar_btn = ctk.CTkButton(
                card,
                text=get_initials(name),
                width=52,
                height=52,
                corner_radius=26,
                fg_color=avatar_col,
                font=ctk.CTkFont(size=18, weight="bold"),
                state="disabled"
            )
            avatar_btn.pack(side="left", padx=16, pady=14)

            # Details column
            details_frame = ctk.CTkFrame(card, fg_color="transparent")
            details_frame.pack(side="left", fill="both", expand=True, pady=12)

            # Name and Group Badge line
            name_badge_line = ctk.CTkFrame(details_frame, fg_color="transparent")
            name_badge_line.pack(fill="x", anchor="w")

            name_label = ctk.CTkLabel(
                name_badge_line,
                text=name,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            name_label.pack(side="left")

            badge = ctk.CTkLabel(
                name_badge_line,
                text=f" {grp_name} ",
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=grp_style["bg"],
                text_color=grp_style["fg"],
                corner_radius=6
            )
            badge.pack(side="left", padx=(10, 0))

            # Info line (Phone, Email, Address)
            info_line = ctk.CTkFrame(details_frame, fg_color="transparent")
            info_line.pack(fill="x", anchor="w", pady=(4, 0))

            # Phone
            phone_lbl = ctk.CTkLabel(
                info_line,
                text=f"📞 {phone}",
                font=ctk.CTkFont(size=13),
                text_color=("#334155", "#CBD5E1")
            )
            phone_lbl.pack(side="left", padx=(0, 14))

            # Email
            if email:
                email_lbl = ctk.CTkLabel(
                    info_line,
                    text=f"✉️ {email}",
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                )
                email_lbl.pack(side="left", padx=(0, 14))

            # Address
            if address:
                addr_lbl = ctk.CTkLabel(
                    info_line,
                    text=f"📍 {address}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                addr_lbl.pack(side="left", padx=(0, 14))

            # Right actions
            actions_frame = ctk.CTkFrame(card, fg_color="transparent")
            actions_frame.pack(side="right", padx=16, pady=12)

            # WhatsApp button
            wa_btn = ctk.CTkButton(
                actions_frame,
                text="💬 WhatsApp",
                width=86,
                height=32,
                corner_radius=6,
                fg_color=COLORS["whatsapp"],
                hover_color=COLORS["whatsapp_hover"],
                text_color="#FFFFFF",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda p=phone, n=name: (
                    open_whatsapp(p),
                    show_toast(f"💬 Opening WhatsApp for {n}...", color=COLORS["whatsapp"])
                )
            )
            wa_btn.pack(side="left", padx=4)

            # Copy button
            copy_btn = ctk.CTkButton(
                actions_frame,
                text="📋 Copy",
                width=65,
                height=32,
                corner_radius=6,
                fg_color=("#F1F5F9", "#282E3E"),
                text_color=("#0F172A", "#E2E8F0"),
                hover_color=("#E2E8F0", "#384157"),
                font=ctk.CTkFont(size=11),
                command=lambda p=phone, n=name: copy_to_clipboard(p, f"phone for {n}")
            )
            copy_btn.pack(side="left", padx=4)

            # Edit button
            row_data = row
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏️ Edit",
                width=65,
                height=32,
                corner_radius=6,
                fg_color=("#F1F5F9", "#282E3E"),
                text_color=("#0F172A", "#E2E8F0"),
                hover_color=("#E2E8F0", "#384157"),
                font=ctk.CTkFont(size=11),
                command=lambda d=row_data: edit_action(d)
            )
            edit_btn.pack(side="left", padx=4)

            # Delete button
            del_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                width=34,
                height=32,
                corner_radius=6,
                fg_color=("#FEE2E2", "#382025"),
                text_color=COLORS["danger"],
                hover_color=("#FECACA", "#4C242A"),
                font=ctk.CTkFont(size=12),
                command=lambda i=cid, n=name: delete_action(i, n)
            )
            del_btn.pack(side="left", padx=4)

    # Bind live search
    search_entry.bind("<KeyRelease>", refresh_list)

    # Initial load
    refresh_list()


def render_trash_view(parent, on_restored=None):
    """Renders the Recycle Bin view with deleted contacts and restore/delete forever actions."""
    for widget in parent.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=25, pady=20)

    # Header
    top_row = ctk.CTkFrame(container, fg_color="transparent")
    top_row.pack(fill="x", pady=(0, 15))

    title_frame = ctk.CTkFrame(top_row, fg_color="transparent")
    title_frame.pack(side="left")

    title_lbl = ctk.CTkLabel(
        title_frame,
        text="🗑️ Recycle Bin",
        font=ctk.CTkFont(size=22, weight="bold"),
        anchor="w"
    )
    title_lbl.pack(anchor="w")

    subtitle_lbl = ctk.CTkLabel(
        title_frame,
        text="Restore contacts or delete them permanently",
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    )
    subtitle_lbl.pack(anchor="w", pady=(2, 0))

    cards_scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
    cards_scroll.pack(fill="both", expand=True)

    toast_lbl = ctk.CTkLabel(container, text="", font=ctk.CTkFont(size=12))
    toast_lbl.pack(pady=2)

    def show_toast(msg, color=COLORS["success"]):
        toast_lbl.configure(text=msg, text_color=color)
        container.after(3000, lambda: toast_lbl.configure(text=""))

    def restore_action(contact_id, name):
        DBHelper.restore_contact(contact_id)
        show_toast(f"✅ Restored '{name}' to active contacts!")
        refresh_trash()
        if on_restored:
            on_restored()

    def permanent_delete_action(contact_id, name):
        DBHelper.permanent_delete(contact_id)
        show_toast(f"❌ Permanently deleted '{name}'", color=COLORS["danger"])
        refresh_trash()

    def empty_trash_action():
        DBHelper.empty_trash()
        show_toast("🗑️ Recycle Bin emptied", color=COLORS["warning"])
        refresh_trash()

    def refresh_trash():
        for w in cards_scroll.winfo_children():
            w.destroy()

        rows = DBHelper.get_deleted_contacts()

        if not rows:
            empty_frame = ctk.CTkFrame(cards_scroll, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=60)
            ctk.CTkLabel(
                empty_frame,
                text="✨ Recycle Bin is empty",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=(0, 6))
            ctk.CTkLabel(
                empty_frame,
                text="No deleted contacts to restore.",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            ).pack()
            return

        for row in rows:
            cid, name, phone, email, address, grp, del_at = row
            card = ctk.CTkFrame(
                cards_scroll,
                corner_radius=12,
                fg_color=("#FFFFFF", "#1C202C")
            )
            card.pack(fill="x", pady=6, padx=2)

            # Initials
            avatar_btn = ctk.CTkButton(
                card,
                text=get_initials(name),
                width=50,
                height=50,
                corner_radius=25,
                fg_color=get_avatar_color(name),
                font=ctk.CTkFont(size=16, weight="bold"),
                state="disabled"
            )
            avatar_btn.pack(side="left", padx=16, pady=12)

            details_frame = ctk.CTkFrame(card, fg_color="transparent")
            details_frame.pack(side="left", fill="both", expand=True, pady=10)

            ctk.CTkLabel(
                details_frame,
                text=name,
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                details_frame,
                text=f"📞 {phone}  |  Group: {grp or 'Other'}  |  Deleted: {str(del_at)[:16] if del_at else 'Recent'}",
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(anchor="w", pady=(2, 0))

            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=16, pady=10)

            restore_btn = ctk.CTkButton(
                actions,
                text="♻️ Restore",
                width=80,
                height=32,
                corner_radius=6,
                fg_color=COLORS["success"],
                hover_color=COLORS["success_hover"],
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda i=cid, n=name: restore_action(i, n)
            )
            restore_btn.pack(side="left", padx=4)

            perm_btn = ctk.CTkButton(
                actions,
                text="Delete Forever",
                width=95,
                height=32,
                corner_radius=6,
                fg_color=("#FEE2E2", "#382025"),
                text_color=COLORS["danger"],
                hover_color=("#FECACA", "#4C242A"),
                font=ctk.CTkFont(size=11),
                command=lambda i=cid, n=name: permanent_delete_action(i, n)
            )
            perm_btn.pack(side="left", padx=4)

    # Empty All button in top row
    empty_btn = ctk.CTkButton(
        top_row,
        text="Empty Trash",
        height=34,
        corner_radius=8,
        fg_color=("#FEE2E2", "#382025"),
        text_color=COLORS["danger"],
        hover_color=("#FECACA", "#4C242A"),
        font=ctk.CTkFont(size=12),
        command=empty_trash_action
    )
    empty_btn.pack(side="right")

    refresh_trash()


def view_contact():
    """Fallback standalone window for view contacts."""
    modal = ctk.CTkToplevel(app)
    modal.geometry("750x600")
    modal.title("Contacts Directory")
    modal.transient(app)
    render_view_contacts(modal)