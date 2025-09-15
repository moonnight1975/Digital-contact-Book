import customtkinter as ctk
from config import app

def setting():
    # Settings window
    setting_win = ctk.CTkToplevel(app)
    setting_win.geometry("400x450")
    setting_win.title("Settings")

    ctk.CTkLabel(setting_win, text="Settings", font=("Arial", 20)).pack(pady=10)

    # =========================
    # Appearance Section
    # =========================
    def open_appearance_window():
        apper_win = ctk.CTkToplevel(setting_win)
        apper_win.geometry("400x300")
        apper_win.title("Appearance")

        ctk.CTkLabel(apper_win, text="Choose Appearance Mode", font=("Arial", 16, "bold")).pack(pady=10)

        appearance_var = ctk.StringVar(value=ctk.get_appearance_mode())

        def update_colors(mode):
            ctk.set_appearance_mode(mode)

        # Dropdown
        appearance_dropdown = ctk.CTkOptionMenu(
            apper_win,
            values=["Light", "Dark", "System"],
            variable=appearance_var,
            command=update_colors
        )
        appearance_dropdown.pack(pady=10, padx=20, fill="x")

        # Reset button
        reset_btn = ctk.CTkButton(
            apper_win,
            text="Reset to System Default",
            command=lambda: (appearance_var.set("System"), update_colors("System"))
        )
        reset_btn.pack(pady=10, padx=20, fill="x")

    appear_btn = ctk.CTkButton(setting_win, text="Appearance", command=open_appearance_window)
    appear_btn.pack(pady=10, padx=20, fill="x")

    # =========================
    # About Section
    # =========================
    def open_about_window():
        about_win = ctk.CTkToplevel(setting_win)
        about_win.geometry("400x250")
        about_win.title("About")

        ctk.CTkLabel(about_win, text="About This App", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(
            about_win,
            text="Digital Contact Book\nVersion 1.0\nDeveloped by Litto & Anant",
            justify="center"
        ).pack(pady=20)

        close_btn = ctk.CTkButton(about_win, text="Close", command=about_win.destroy)
        close_btn.pack(pady=10)

    about_btn = ctk.CTkButton(setting_win, text="About", command=open_about_window)
    about_btn.pack(pady=10, padx=20, fill="x")
