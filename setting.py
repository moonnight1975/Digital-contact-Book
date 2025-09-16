import customtkinter as ctk
from config import app

# --- Global list to track all open windows (main app + Toplevels) ---
# We start with the main app instance.
open_windows = [app]

def setting():
    # --- Settings Window Setup ---
    setting_win = ctk.CTkToplevel(app)
    setting_win.geometry("400x300")
    setting_win.title("Settings")
    setting_win.transient(app)

    # **FIX**: Add the new window to our tracker list
    open_windows.append(setting_win)
    # **FIX**: When the window is closed, remove it from the list to prevent errors
    setting_win.bind("<Destroy>", lambda e: open_windows.remove(setting_win))

    title_label = ctk.CTkLabel(setting_win, text="Settings", font=("Arial", 20))
    title_label.pack(pady=10)

    # =========================
    # Appearance Section
    # =========================
    def open_appearance_window():
        apper_win = ctk.CTkToplevel(setting_win)
        apper_win.geometry("400x300")
        apper_win.title("Appearance")
        apper_win.transient(setting_win)

        # **FIX**: Track this new window as well
        open_windows.append(apper_win)
        apper_win.bind("<Destroy>", lambda e: open_windows.remove(apper_win))

        label = ctk.CTkLabel(apper_win, text="Choose Appearance Mode", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        # Dropdown for Light/Dark/System
        def update_appearance_mode(mode):
            ctk.set_appearance_mode(mode)

        appearance_dropdown = ctk.CTkOptionMenu(
            apper_win,
            values=["Light", "Dark", "System"],
            command=update_appearance_mode
        )
        appearance_dropdown.set(ctk.get_appearance_mode())
        appearance_dropdown.pack(pady=10, padx=20, fill="x")

        # --- **FIXED**: Function to change the background color of ALL windows ---
        def change_bg_color(choice):
            color = choice.lower()
            # Iterate through all tracked windows and update their background
            for window in open_windows:
                if window.winfo_exists():
                    window.configure(fg_color=color)

        color_label = ctk.CTkLabel(apper_win, text="Pick Background Color", font=("Arial", 14))
        color_label.pack(pady=10)

        color_combo = ctk.CTkComboBox(
            apper_win,
            values=["Maroon", "#a2d2ff", "Green", "Black"], # Added default dark color
            command=change_bg_color,
            width=200
        )
        color_combo.set("Select Color")
        color_combo.pack(pady=10)

        # --- **FIXED**: Reset button to restore default colors on all windows ---
        def reset_to_default():
            # Set mode back to System
            ctk.set_appearance_mode("System")
            appearance_dropdown.set("System")

            # Get the default background color for the current theme
            default_color = ctk.ThemeManager.theme["CTk"]["fg_color"]

            # Apply default color to all open windows
            for window in open_windows:
                if window.winfo_exists():
                    window.configure(fg_color=default_color)

        reset_btn = ctk.CTkButton(apper_win, text="Reset to System Default", fg_color="purple",
                                  hover_color="darkmagenta",
                                  text_color="white",
                                  corner_radius=200, command=reset_to_default)
        reset_btn.pack(pady=20, padx=20, fill="x")

    appear_btn = ctk.CTkButton(setting_win, text="Appearance", fg_color="purple",
                               hover_color="darkmagenta",
                               text_color="white",
                               corner_radius=200, command=open_appearance_window)
    appear_btn.pack(pady=10, padx=20, fill="x")

    # =========================
    # About Section
    # =========================
    def open_about_window():
        about_win = ctk.CTkToplevel(setting_win)
        about_win.geometry("400x250")
        about_win.title("About")
        about_win.transient(setting_win)

        # **FIX**: Track the about window
        open_windows.append(about_win)
        about_win.bind("<Destroy>", lambda e: open_windows.remove(about_win))

        # **FIX**: Apply the current background color when opening
        current_bg = app.cget("fg_color")
        about_win.configure(fg_color=current_bg)

        label1 = ctk.CTkLabel(about_win, text="About This App", font=("Arial", 16, "bold"))
        label1.pack(pady=10)

        label2 = ctk.CTkLabel(
            about_win,
            text="Digital Contact Book\nVersion 1.10\nDeveloped by Litto & Anant",
            justify="center"
        )
        label2.pack(pady=20)

        close_btn = ctk.CTkButton(about_win, text="Close", fg_color="purple",
                                  hover_color="darkmagenta",
                                  text_color="white",
                                  corner_radius=200, command=about_win.destroy)
        close_btn.pack(pady=10)

    about_btn = ctk.CTkButton(setting_win, text="About", fg_color="purple",
                              hover_color="darkmagenta",
                              text_color="white",
                              corner_radius=200, command=open_about_window)
    about_btn.pack(pady=10, padx=20, fill="x")