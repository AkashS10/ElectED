# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Client":
    os.chdir("Client")

from tkinter import messagebox
from customtkinter import *
import os

import backend

def changeState(data):
    cCategoryOptionMenuVar.set("Select...")
    cCategoryOptionMenu.configure(values=eval(data))
    cConnectBtn.configure(state="disabled")
    cIPEnt.configure(state="disabled")
    cPortEnt.configure(state="disabled")
    cCategoryOptionMenu.configure(state="enabled")
    cBeginVotingBtn.configure(state="enabled")

root = CTk()
root.title("ElectED")
root.geometry("400x500")
root.resizable(False, False)
root.iconbitmap("icon.ico")

s = backend.NetworkHandler(messagebox, root)

configureFrame = CTkFrame(root)
configureFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

cTitleLbl = CTkLabel(configureFrame, text="Configure", font=("Segoe UI", 24, "bold"))
cTitleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)

cIPEnt = CTkEntry(configureFrame, placeholder_text="IP Address", font=("Segoe UI", 20))
cIPEnt.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

cPortEnt = CTkEntry(configureFrame, placeholder_text="Port", font=("Segoe UI", 20))
cPortEnt.place(relx=0.1, rely=0.325, relwidth=0.8, relheight=0.1)

cConnectBtn = CTkButton(configureFrame, text="Connect", font=("Segoe UI", 20), command=lambda: s.connect(cIPEnt.get(), cPortEnt.get(), changeState))
cConnectBtn.place(relx=0.1, rely=0.475, relwidth=0.8, relheight=0.1)

cCategoryOptionMenuVar = StringVar(root, "Select...")
cCategoryOptionMenu = CTkOptionMenu(root, variable=cCategoryOptionMenuVar, font=("Segoe UI", 20), state="disabled")
cCategoryOptionMenu.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.06)

cBeginVotingBtn = CTkButton(configureFrame, text="Begin Voting", font=("Segoe UI", 20), state="disabled", command=lambda: s.beginVoting(cCategoryOptionMenuVar.get(), configureFrame, vCategoryTitleLbl, vTotalVoteCountLbl))
cBeginVotingBtn.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.125)

votingFrame = CTkFrame(root)
s.votingFrame = votingFrame

vCategoryTitleLbl = CTkLabel(votingFrame, text="Category", font=("Segoe UI", 32, "bold"))
vCategoryTitleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.15)

vTotalVoteCountLbl = CTkLabel(votingFrame, text="Total Vote Count\n0", font=("Segoe UI", 24, "bold"))
vTotalVoteCountLbl.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.15)

if os.path.isfile("previousConnection.txt"):
    fPC = open("previousConnection.txt", "r")
    read = fPC.read()
    fPC.close()
    read = read.split("|")
    cIPEnt.insert(0, read[0])
    cPortEnt.insert(0, read[1])

root.mainloop()
s.disconnect()