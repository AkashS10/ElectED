# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Client":
    os.chdir("Client")

from customtkinter import *
from tkinter import messagebox
import threading
import socket

class SocketConnHandler:
    def __init__(self):
        self.s = socket.socket()

    def connect(self):
        ip = cIPEnt.get()
        port = cPortEnt.get()
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("ElectED", "Please enter a valid port")
            return
        try:
            self.s.connect((ip, port))
        except Exception:
            messagebox.showerror("ElectED", "Invalid IP/Port")
            return
        
        data, addr = self.s.recvfrom(4096)
        data = data.decode()
        if data.startswith("/act/"):
            data = data[5:]
            cCategoryOptionMenuVar.set("Select...")
            cCategoryOptionMenu.configure(values=eval(data))
            cConnectBtn.configure(state="disabled")
            cIPEnt.configure(state="disabled")
            cPortEnt.configure(state="disabled")
            cCategoryOptionMenu.configure(state="enabled")
            cBeginVotingBtn.configure(state="enabled")
    
    def beginVoting(self):
        category = cCategoryOptionMenuVar.get()
        if category == "Select...":
            messagebox.showerror("ElectED", "Select a category to begin voting")
            return
        self.s.send(f"/cts/{category}".encode()) # CTS - CaTegory Select

s = SocketConnHandler()

# root.attributes("-fullscreen", True)
root = CTk()
root.title("ElectED")
root.geometry("400x500")
root.resizable(False, False)
root.iconbitmap("icon.ico")

configureFrame = CTkFrame(root)
configureFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

cTitleLbl = CTkLabel(configureFrame, text="Configure", font=("Segoe UI", 24, "bold"))
cTitleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)

cIPEnt = CTkEntry(configureFrame, placeholder_text="IP Address", font=("Segoe UI", 20))
cIPEnt.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

cPortEnt = CTkEntry(configureFrame, placeholder_text="Port", font=("Segoe UI", 20))
cPortEnt.place(relx=0.1, rely=0.325, relwidth=0.8, relheight=0.1)

cConnectBtn = CTkButton(configureFrame, text="Connect", font=("Segoe UI", 20), command=s.connect)
cConnectBtn.place(relx=0.1, rely=0.475, relwidth=0.8, relheight=0.1)

cCategoryOptionMenuVar = StringVar(root, "Select...")
cCategoryOptionMenu = CTkOptionMenu(root, variable=cCategoryOptionMenuVar, font=("Segoe UI", 20), state="disabled")
cCategoryOptionMenu.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.06)

cBeginVotingBtn = CTkButton(configureFrame, text="Begin Voting", font=("Segoe UI", 20), state="disabled", command=s.beginVoting)
cBeginVotingBtn.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.125)

root.mainloop()