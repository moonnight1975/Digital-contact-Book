import customtkinter

class CustomMenu(customtkinter.CTkToplevel):
    def __init__(self, master, x, y):
        super().__init__(master)

        # Make the window a temporary, borderless popup
        self.overrideredirect(True)
        self.geometry(f"150x120+{x}+{y}")

        # Make the window grab focus so no other window can be interacted with
        self.grab_set()

        # Add buttons to the menu frame
        button1 = customtkinter.CTkButton(
            self,
            text="Option 1",
            command=lambda: self.on_option_selected("Option 1")
        )
        button1.pack(pady=(10, 5), padx=10, fill="x")

        button2 = customtkinter.CTkButton(
            self,
            text="Option 2",
            command=lambda: self.on_option_selected("Option 2")
        )
        button2.pack(pady=5, padx=10, fill="x")

        button3 = customtkinter.CTkButton(
            self,
            text="Quit",
            command=self.master.quit
        )
        button3.pack(pady=(5, 10), padx=10, fill="x")

        # Bind a click event to the top-level window to dismiss it
        self.bind("<FocusOut>", self.on_focus_lost)

    def on_option_selected(self, option):
        print(f"{option} clicked!")
        self.destroy()

    def on_focus_lost(self, event):
        # Dismiss the menu if it loses focus
        self.destroy()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")
        self.title("Robust Custom Menu Example")

        self.menu_button = customtkinter.CTkButton(
            self,
            text="Menu",
            command=self.show_menu
        )
        self.menu_button.place(x=20, y=20)

        self.current_menu = None

    def show_menu(self):
        # If a menu is already open, destroy it first
        if self.current_menu and self.current_menu.winfo_exists():
            self.current_menu.destroy()

        # Get the position of the button to place the menu correctly
        button_x = self.menu_button.winfo_x() + self.menu_button.winfo_width()
        button_y = self.menu_button.winfo_y() + self.menu_button.winfo_height() + 5

        # Create and show the new custom menu
        self.current_menu = CustomMenu(self, self.winfo_x() + button_x, self.winfo_y() + button_y)

if __name__ == "__main__":
    app = App()
    app.mainloop()