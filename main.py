import customtkinter as ctk
from config import app  # main app instance

# Import after app is created to avoid circular import issues
from events import events
from setting import setting
from add import add_contact
from view import view_contact
from dashboard import dashboard


# Main label
label = ctk.CTkLabel(app, text="Hello There", font=("Arial", 30), text_color="white")
label.pack(pady=20)


class CustomMenu(ctk.CTkToplevel):
    def __init__(self, master, x, y):
        super().__init__(master)

        self.overrideredirect(True)
        self.geometry(f"150x150+{x}+{y}")
        self.grab_set()

        # Add menu buttons
        btn_add = ctk.CTkButton(self, text="Add", fg_color="purple",
                                hover_color="darkmagenta",
                                text_color="white",
                                corner_radius=200, command=lambda: [add_contact(), self.destroy()])
        btn_add.pack(pady=5, padx=10, fill="x")

        btn_view = ctk.CTkButton(self, text="View", fg_color="purple",
                                 hover_color="darkmagenta",
                                 text_color="white",
                                 corner_radius=200, command=lambda: [view_contact(), self.destroy()])
        btn_view.pack(pady=5, padx=10, fill="x")

        btn_dashboard = ctk.CTkButton(self, text="Dashboard", fg_color="purple",
                                      hover_color="darkmagenta",
                                      text_color="white",
                                      corner_radius=200, command=lambda: [dashboard(), self.destroy()])
        btn_dashboard.pack(pady=5, padx=10, fill="x")

        setting_btn = ctk.CTkButton(self, text="Settings", fg_color="purple",
                                    hover_color="darkmagenta",
                                    text_color="white",
                                    corner_radius=200, command=lambda: [setting(), self.destroy()])
        setting_btn.pack(pady=5, padx=10, fill="x")

        btn_quit = ctk.CTkButton(self, text="Quit", fg_color="purple",
                                 hover_color="darkmagenta",
                                 text_color="white",
                                 corner_radius=200, command=self.master.quit)
        btn_quit.pack(pady=(5, 10), padx=10, fill="x")

        # Close when focus is lost
        self.bind("<FocusOut>", lambda event: self.destroy())


def show_custom_menu(event):
    menu_button = event.widget
    # Position the menu relative to the button
    menu_x = menu_button.winfo_rootx()
    menu_y = menu_button.winfo_rooty() + menu_button.winfo_height() + 6

    CustomMenu(app, menu_x, menu_y)


# Main menu button
menu_btn = ctk.CTkButton(
    app,
    text="Menu",
    fg_color="purple",
    hover_color="darkmagenta",
    text_color="white",
    corner_radius=200,
)
menu_btn.pack(pady=20)
menu_btn.bind("<Button-1>", show_custom_menu)


# Optional: enable Events button
# group_btn = ctk.CTkButton(app, text="Events", command=events, fg_color="blue", hover_color="green", text_color="white", corner_radius=200)
# group_btn.pack(pady=20)

app.mainloop()
