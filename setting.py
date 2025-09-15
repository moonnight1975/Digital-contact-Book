import customtkinter as ctk
from config import app

def setting():
    # Settings window
    setting_win = ctk.CTkToplevel(app)
    setting_win.geometry("400x450")
    setting_win.title("Settings")

    # Section title
    ctk.CTkLabel(setting_win, text="Settings", font=("Arial", 20)).pack(pady=10)

    # =========================
    # Appearance Section
    # =========================
    ctk.CTkLabel(setting_win, text="Appearance", font=("Arial", 16, "bold")).pack(pady=10)

    # Function to update colors
    def update_colors(mode):
        ctk.set_appearance_mode(mode)
        if mode == "Dark":
            for widget in setting_win.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="white")
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color="grey", hover_color="green", text_color="white")
        elif mode == "Light":
            for widget in setting_win.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="black")
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color="lightgrey", hover_color="green", text_color="black")
        else:  # System default
            for widget in setting_win.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="blue")
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color="grey", hover_color="green", text_color="black")

    appearance_var = ctk.StringVar(value=ctk.get_appearance_mode())
    appearance_dropdown = ctk.CTkOptionMenu(
        setting_win,
        values=["Light", "Dark", "System"],
        variable=appearance_var,
        command=update_colors
    )
    appearance_dropdown.pack(pady=10, padx=20, fill="x")

    reset_btn = ctk.CTkButton(
        setting_win,
        text="Reset to System Default",
        command=lambda: update_colors("System")
    )
    reset_btn.pack(pady=10, padx=20, fill="x")

    # =========================
    # About Section
    # =========================
    ctk.CTkLabel(setting_win, text="About", font=("Arial", 16, "bold")).pack(pady=20)
    ctk.CTkLabel(setting_win, text="Digital Contact Book", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(setting_win, text="Version 1.0.0", font=("Arial", 14)).pack(pady=5)
