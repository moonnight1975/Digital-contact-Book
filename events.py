import customtkinter as ctk
from config import app, DBHelper
from theme import COLORS, get_avatar_color, get_initials


def render_events_view(parent):
    """Renders events and upcoming birthdays view."""
    for widget in parent.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=25, pady=20)

    # Header
    ctk.CTkLabel(
        container,
        text="📅 Events & Reminders",
        font=ctk.CTkFont(size=22, weight="bold"),
        anchor="w"
    ).pack(fill="x", pady=(0, 4))

    ctk.CTkLabel(
        container,
        text="Keep track of contact birthdays and upcoming anniversaries.",
        font=ctk.CTkFont(size=13),
        text_color="gray",
        anchor="w"
    ).pack(fill="x", pady=(0, 16))

    card = ctk.CTkFrame(container, corner_radius=12, fg_color=("#FFFFFF", "#1C202C"))
    card.pack(fill="both", expand=True)

    contacts = DBHelper.get_contacts()
    with_bday = [c for c in contacts if c[6]]

    if not with_bday:
        empty = ctk.CTkFrame(card, fg_color="transparent")
        empty.pack(expand=True, pady=60)
        ctk.CTkLabel(
            empty,
            text="🎂 No upcoming events scheduled",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 6))
        ctk.CTkLabel(
            empty,
            text="Add birthdays to your contacts when creating or editing them.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack()
    else:
        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=16)

        for c in with_bday:
            cid, name, phone, email, address, grp, bday = c
            row = ctk.CTkFrame(scroll, corner_radius=8, fg_color=("#F8FAFC", "#161922"))
            row.pack(fill="x", pady=4)

            avatar = ctk.CTkButton(
                row,
                text=get_initials(name),
                width=40,
                height=40,
                corner_radius=20,
                fg_color=get_avatar_color(name),
                font=ctk.CTkFont(size=13, weight="bold"),
                state="disabled"
            )
            avatar.pack(side="left", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=6)

            ctk.CTkLabel(
                row,
                text=f"🎂 {bday}",
                font=ctk.CTkFont(size=13),
                text_color=COLORS["primary"]
            ).pack(side="right", padx=16)


def events():
    """Fallback standalone modal for events."""
    modal = ctk.CTkToplevel(app)
    modal.geometry("500x400")
    modal.title("Events & Reminders")
    modal.transient(app)
    render_events_view(modal)
