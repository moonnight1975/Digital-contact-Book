import customtkinter as ctk
from config import conn, cur, app

def events():
    events_win = ctk.CTkToplevel(app)
    events_win.geometry("400x250")
    events_win.title("Events")

    adde_btn=ctk.CTkButton(events_win,text="Add Event",font=("Arial",20),
    fg_color="blue",
    hover_color="green",
    text_color="white")
    adde_btn.pack(padx=10,pady=10)

    reme_btn=ctk.CTkButton(events_win,text="Remove Event",font=("Arial",20), fg_color="blue",
                           hover_color="green",
                           text_color="white")
    reme_btn.pack(padx=10,pady=10)


