import customtkinter as ctk
from config import app, DBHelper
from theme import COLORS, get_avatar_color, get_initials, get_group_style


def render_add_view(parent, on_saved=None, edit_data=None):
    """
    Renders the Add / Edit contact form inside the given parent frame or window.
    If edit_data is provided (dict or tuple), pre-fills the form for editing.
    """
    # Clear parent if it's a container frame
    for widget in parent.winfo_children():
        widget.destroy()

    is_edit = edit_data is not None
    contact_id = edit_data[0] if is_edit and isinstance(edit_data, (tuple, list)) else (edit_data.get("id") if is_edit else None)
    initial_name = (edit_data[1] if isinstance(edit_data, (tuple, list)) else edit_data.get("name", "")) if is_edit else ""
    initial_phone = (edit_data[2] if isinstance(edit_data, (tuple, list)) else edit_data.get("phone", "")) if is_edit else ""
    initial_email = (edit_data[3] if isinstance(edit_data, (tuple, list)) else edit_data.get("email", "")) if is_edit else ""
    initial_address = (edit_data[4] if isinstance(edit_data, (tuple, list)) else edit_data.get("address", "")) if is_edit else ""
    initial_group = (edit_data[5] if isinstance(edit_data, (tuple, list)) else edit_data.get("contact_group", "Other")) if is_edit else "Other"
    initial_birthday = (edit_data[6] if isinstance(edit_data, (tuple, list)) and len(edit_data) > 6 else edit_data.get("birthday", "")) if is_edit else ""

    # Outer scrollable frame
    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=25, pady=20)

    # Header
    title_text = "✏️ Edit Contact" if is_edit else "➕ Add New Contact"
    subtitle_text = "Update contact details below" if is_edit else "Fill in the details to save a new contact"

    header_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    title_label = ctk.CTkLabel(
        header_frame,
        text=title_text,
        font=ctk.CTkFont(size=22, weight="bold"),
        anchor="w"
    )
    title_label.pack(anchor="w")

    subtitle_label = ctk.CTkLabel(
        header_frame,
        text=subtitle_text,
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    )
    subtitle_label.pack(anchor="w", pady=(2, 0))

    # Center card container
    card = ctk.CTkFrame(scroll, corner_radius=14, fg_color=("#FFFFFF", "#1C202C"))
    card.pack(fill="x", padx=10, pady=10)

    # Avatar preview container
    avatar_container = ctk.CTkFrame(card, fg_color="transparent")
    avatar_container.pack(pady=(20, 10))

    avatar_btn = ctk.CTkButton(
        avatar_container,
        text=get_initials(initial_name) if initial_name else "👤",
        width=70,
        height=70,
        corner_radius=35,
        fg_color=get_avatar_color(initial_name) if initial_name else COLORS["primary"],
        font=ctk.CTkFont(size=24, weight="bold"),
        state="disabled"
    )
    avatar_btn.pack()

    # Form Fields
    form_frame = ctk.CTkFrame(card, fg_color="transparent")
    form_frame.pack(fill="x", padx=40, pady=(10, 20))

    # Helper for field labels
    def create_field(parent_frame, label_text, placeholder, default_val=""):
        f_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        f_frame.pack(fill="x", pady=8)
        lbl = ctk.CTkLabel(f_frame, text=label_text, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
        lbl.pack(anchor="w", pady=(0, 3))
        entry = ctk.CTkEntry(f_frame, placeholder_text=placeholder, height=38, corner_radius=8)
        entry.pack(fill="x")
        if default_val:
            entry.insert(0, str(default_val))
        return entry

    name_entry = create_field(form_frame, "Full Name *", "e.g. Litto Biju", initial_name)
    phone_entry = create_field(form_frame, "Phone Number *", "e.g. +1 555 123 4567", initial_phone)
    email_entry = create_field(form_frame, "Email Address", "e.g. litto@example.com", initial_email)
    address_entry = create_field(form_frame, "Address", "e.g. 123 Innovation Way", initial_address)
    bday_entry = create_field(form_frame, "Birthday (optional)", "e.g. YYYY-MM-DD", initial_birthday)

    # Category dropdown
    cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    cat_frame.pack(fill="x", pady=8)
    cat_lbl = ctk.CTkLabel(cat_frame, text="Contact Group", font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
    cat_lbl.pack(anchor="w", pady=(0, 3))

    group_var = ctk.StringVar(value=initial_group if initial_group in ["Family", "Work", "Friends", "Other"] else "Other")
    group_menu = ctk.CTkOptionMenu(
        cat_frame,
        values=["Family", "Work", "Friends", "Other"],
        variable=group_var,
        height=38,
        corner_radius=8,
        fg_color=COLORS["primary"],
        button_color=COLORS["primary_hover"]
    )
    group_menu.pack(fill="x")

    # Live avatar updater
    def on_name_change(event=None):
        n = name_entry.get().strip()
        avatar_btn.configure(
            text=get_initials(n) if n else "👤",
            fg_color=get_avatar_color(n) if n else COLORS["primary"]
        )

    name_entry.bind("<KeyRelease>", on_name_change)

    # Filter digits in phone
    def validate_phone(event=None):
        current = phone_entry.get()
        # Keep digits, spaces, plus, hyphens
        filtered = ''.join(c for c in current if c.isdigit() or c in "+ -()")
        if current != filtered:
            phone_entry.delete(0, 'end')
            phone_entry.insert(0, filtered)

    phone_entry.bind("<KeyRelease>", validate_phone)

    # Toast feedback container
    status_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=13))
    status_label.pack(pady=4)

    def show_feedback(msg, is_error=False):
        status_label.configure(
            text=msg,
            text_color=COLORS["danger"] if is_error else COLORS["success"]
        )
        card.after(3500, lambda: status_label.configure(text=""))

    # Actions container
    actions_frame = ctk.CTkFrame(card, fg_color="transparent")
    actions_frame.pack(fill="x", padx=40, pady=(10, 25))

    def save_action():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        group = group_var.get()
        birthday = bday_entry.get().strip() or None

        if not name or not phone:
            show_feedback("⚠️ Name and Phone are required.", is_error=True)
            return

        try:
            if is_edit:
                DBHelper.update_contact(contact_id, name, phone, email, address, group, birthday)
                show_feedback("✅ Contact updated successfully!")
            else:
                DBHelper.add_contact(name, phone, email, address, group, birthday)
                show_feedback(f"✅ {name} added to {group}!")
                # Reset fields
                name_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                email_entry.delete(0, 'end')
                address_entry.delete(0, 'end')
                bday_entry.delete(0, 'end')
                group_var.set("Other")
                on_name_change()

            if on_saved:
                card.after(600, on_saved)

        except Exception as e:
            show_feedback(f"❌ Error: {e}", is_error=True)

    save_btn = ctk.CTkButton(
        actions_frame,
        text="💾 Save Changes" if is_edit else "➕ Add Contact",
        command=save_action,
        height=42,
        corner_radius=8,
        fg_color=COLORS["primary"],
        hover_color=COLORS["primary_hover"],
        font=ctk.CTkFont(size=14, weight="bold")
    )
    save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def clear_action():
        name_entry.delete(0, 'end')
        phone_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        address_entry.delete(0, 'end')
        bday_entry.delete(0, 'end')
        group_var.set("Other")
        on_name_change()

    clear_btn = ctk.CTkButton(
        actions_frame,
        text="Clear",
        command=clear_action,
        height=42,
        corner_radius=8,
        fg_color=("#E2E8F0", "#2D3446"),
        text_color=("#0F172A", "#F8FAFC"),
        hover_color=("#CBD5E1", "#3B445B"),
        font=ctk.CTkFont(size=14)
    )
    clear_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))


def add_contact(edit_data=None, on_saved=None):
    """Fallback top-level modal if called as a standalone window."""
    modal = ctk.CTkToplevel(app)
    modal.geometry("520x650")
    modal.title("Edit Contact" if edit_data else "Add Contact")
    modal.transient(app)
    modal.grab_set()

    def handle_saved():
        if on_saved:
            on_saved()
        modal.destroy()

    render_add_view(modal, on_saved=handle_saved, edit_data=edit_data)