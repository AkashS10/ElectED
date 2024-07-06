# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Client":
    os.chdir("Client")

from customtkinter import *
import threading
import socket

s = socket.socket()

# root.attributes("-fullscreen", True)
root = CTk()
root.title("ElectED")
root.geometry("400x500")
root.resizable(False, False)
root.iconbitmap("icon.ico")

connectFrame = CTkFrame(root)
connectFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

cTitleLbl = CTkLabel(connectFrame, text="Connect", font=("Segoe UI", 24, "bold"))
cTitleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)

root.mainloop()