import hashlib

# Theme Color Palette
COLORS = {
    "dark": {
        "bg": "#0F1117",
        "sidebar_bg": "#161922",
        "sidebar_active": "#242938",
        "card_bg": "#1C202C",
        "card_hover": "#252B3B",
        "input_bg": "#222736",
        "border": "#2D3446",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
    },
    "light": {
        "bg": "#F8FAFC",
        "sidebar_bg": "#FFFFFF",
        "sidebar_active": "#F1F5F9",
        "card_bg": "#FFFFFF",
        "card_hover": "#F8FAFC",
        "input_bg": "#F1F5F9",
        "border": "#E2E8F0",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "text_muted": "#94A3B8",
    },
    "primary": "#6366F1",        # Indigo
    "primary_hover": "#4F46E5",
    "secondary": "#06B6D4",      # Cyan
    "secondary_hover": "#0891B2",
    "success": "#10B981",        # Emerald
    "success_hover": "#059669",
    "danger": "#EF4444",         # Rose / Red
    "danger_hover": "#DC2626",
    "warning": "#F59E0B",        # Amber
    "warning_hover": "#D97706",
    "whatsapp": "#25D366",       # WhatsApp Green
    "whatsapp_hover": "#1EBE5D",
}

GROUP_COLORS = {
    "Family": {"bg": "#8B5CF6", "fg": "#FFFFFF"},
    "Work": {"bg": "#3B82F6", "fg": "#FFFFFF"},
    "Friends": {"bg": "#10B981", "fg": "#FFFFFF"},
    "Other": {"bg": "#64748B", "fg": "#FFFFFF"},
}

AVATAR_COLORS = [
    "#6366F1",  # Indigo
    "#8B5CF6",  # Purple
    "#EC4899",  # Pink
    "#F43F5E",  # Rose
    "#F97316",  # Orange
    "#EAB308",  # Amber
    "#10B981",  # Emerald
    "#06B6D4",  # Cyan
    "#3B82F6",  # Blue
]


def get_avatar_color(name: str) -> str:
    """Returns a deterministic vibrant color based on contact name."""
    if not name:
        return AVATAR_COLORS[0]
    hash_val = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
    return AVATAR_COLORS[hash_val % len(AVATAR_COLORS)]


def get_initials(name: str) -> str:
    """Extracts up to 2 capitalized initials from name."""
    if not name or not name.strip():
        return "?"
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return parts[0][:2].upper()


def get_group_style(group: str) -> dict:
    """Returns color styling for contact category badges."""
    return GROUP_COLORS.get(group, GROUP_COLORS["Other"])


def open_whatsapp(phone: str):
    """Clean phone number and open WhatsApp chat via browser/desktop app."""
    import webbrowser
    if not phone:
        return False
    # Keep only digits
    clean_digits = "".join(c for c in str(phone) if c.isdigit())
    if not clean_digits:
        return False
    # If standard 10 digit Indian number without country code, prepend 91
    if len(clean_digits) == 10:
        clean_digits = "91" + clean_digits
    url = f"https://wa.me/{clean_digits}"
    webbrowser.open(url)
    return True
