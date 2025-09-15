import customtkinter as ctk
from config import app


# Global list to store widgets that need theme updates
themed_widgets = []

def setting():
    # Settings window
    setting_win = ctk.CTkToplevel(app)
    setting_win.geometry("400x450")
    setting_win.title("Settings")

    title_label = ctk.CTkLabel(setting_win, text="Settings", font=("Arial", 20))
    title_label.pack(pady=10)
    themed_widgets.append(title_label)  # add label to themed widgets

    # =========================
    # Appearance Section
    # =========================
    def open_appearance_window():
        apper_win = ctk.CTkToplevel(setting_win)
        apper_win.geometry("400x350")
        apper_win.title("Appearance")

        label = ctk.CTkLabel(apper_win, text="Choose Appearance Mode", font=("Arial", 16, "bold"))
        label.pack(pady=10)
        themed_widgets.append(label)

        appearance_var = ctk.StringVar(value=ctk.get_appearance_mode())

        def update_colors(mode):
            ctk.set_appearance_mode(mode)

        # Dropdown for Light/Dark/System
        appearance_dropdown = ctk.CTkOptionMenu(
            apper_win,
            values=["Light", "Dark", "System"],
            variable=appearance_var,
            command=update_colors
        )
        appearance_dropdown.pack(pady=10, padx=20, fill="x")
        themed_widgets.append(appearance_dropdown)

        # Combobox for background color
        def change_color(choice):
            color = choice.lower()
            app.configure(fg_color=color)  # main app background

            # Apply same color to all themed widgets
            for widget in themed_widgets:
                try:
                    widget.configure(fg_color=color)
                except:
                    pass  # skip widgets that don’t support fg_color

        color_label = ctk.CTkLabel(apper_win, text="Pick Background Color", font=("Arial", 14))
        color_label.pack(pady=10)
        themed_widgets.append(color_label)

        color_combo = ctk.CTkComboBox(
            apper_win,
            values=["RED", "BLUE", "GREEN", "YELLOW", "PINK", "BLACK", "WHITE"],
            command=change_color,
            width=200
        )
        color_combo.pack(pady=10)
        color_combo.set("COLOURS")
        themed_widgets.append(color_combo)

        # Reset button
        reset_btn = ctk.CTkButton(
            apper_win,
            text="Reset to System Default",
            command=lambda: (
                appearance_var.set("System"),
                update_colors("System"),
                app.configure(fg_color="SystemButtonFace")
            )
        )
        reset_btn.pack(pady=10, padx=20, fill="x")
        themed_widgets.append(reset_btn)

    appear_btn = ctk.CTkButton(setting_win, text="Appearance", command=open_appearance_window)
    appear_btn.pack(pady=10, padx=20, fill="x")
    themed_widgets.append(appear_btn)

    # =========================
    # About Section
    # =========================
    def open_about_window():
        about_win = ctk.CTkToplevel(setting_win)
        about_win.geometry("400x250")
        about_win.title("About")

        label1 = ctk.CTkLabel(about_win, text="About This App", font=("Arial", 16, "bold"))
        label1.pack(pady=10)
        themed_widgets.append(label1)

        label2 = ctk.CTkLabel(
            about_win,
            text="Digital Contact Book\nVersion 1.10\nDeveloped by Litto & Anant",
            justify="center"
        )
        label2.pack(pady=20)
        themed_widgets.append(label2)

        close_btn = ctk.CTkButton(about_win, text="Close", command=about_win.destroy)
        close_btn.pack(pady=10)
        themed_widgets.append(close_btn)

    about_btn = ctk.CTkButton(setting_win, text="About", command=open_about_window)
    about_btn.pack(pady=10, padx=20, fill="x")
    themed_widgets.append(about_btn)
