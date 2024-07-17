# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Client":
    os.chdir("Client")

from tkinter import messagebox
from customtkinter import *
import threading
import hashlib
import socket
import os

class SocketConnHandler:
    def __init__(self):
        self.s = socket.socket()
        self.connected = False
        self.candidates = []

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
            self.connected = True
        except Exception:
            messagebox.showerror("ElectED", "Invalid IP/Port")
            return
        
        self.s.send(f"/hn/{socket.gethostname()}".encode())

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
        self.thread = threading.Thread(target=self.recv, daemon=True)
        self.thread.start()

    def recv(self):
        while True:
            data, addr = self.s.recvfrom(4096)
            data = data.decode()
            if data.startswith("/pim/"):
                data = data[5:]
                filename = data.split("/")[0]
                length = int(data.split("/")[1])
                hash = data.split("/")[2]
                buffer = data[7+len(filename)+len(str(length))+len(hash):].encode()
                data, addr = self.s.recvfrom(length)
                buffer += data
                try:
                    assert hashlib.sha256(buffer).hexdigest() == hash
                except AssertionError:
                    messagebox.showerror("ElectED", f"Failed to verify image integrity")
                    root.destroy()
                    exit()

                f = open(filename, "wb+")
                try:
                    f.write(buffer)
                except Exception as e:
                    messagebox.showerror("ElectED", f"Failed to receieve images, exiting the app\nError: {e}")
                    root.destroy()
                    exit()
                f.close()
            elif data.startswith("/cdl/"):
                self.candidates = eval(data[5:])
                self.displayCandidates()
    
    def displayCandidates(self):
        if len(self.candidates) == 2:
            c1 = CTkFrame(votingFrame, corner_radius=20)
            c1.place(relx=0.2, rely=0.375, relwidth=0.225, relheight=0.4)
            c2 = CTkFrame(votingFrame, corner_radius=20)
            c2.place(relx=0.575, rely=0.375, relwidth=0.225, relheight=0.4)
    
    def beginVoting(self):
        category = cCategoryOptionMenuVar.get()
        if category == "Select...":
            messagebox.showerror("ElectED", "Select a category to begin voting")
            return
        self.s.send(f"/cts/{category}".encode()) # CTS - CaTegory Select

        #TODO: Send candidates list from server and receieve
        
        configureFrame.place_forget()
        cCategoryOptionMenu.place_forget()
        root.wm_attributes("-fullscreen", True)
        root.state("zoomed")
        votingFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        vCategoryTitleLbl.configure(text=f"Vote for {cCategoryOptionMenuVar.get()} candidate")

    def disconnect(self, terminated=False):
        self.thread.join(0)
        self.s.send("/d/".encode())
        self.s.close()
        if terminated:
            messagebox.showinfo("ElectED", "The client session was terminated from the server")
            root.destroy()
        lof = os.listdir(".")
        for i in lof:
            if i.endswith(".png"):
                os.remove(i)
        exit()

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

votingFrame = CTkFrame(root)

vCategoryTitleLbl = CTkLabel(votingFrame, text="Category", font=("Segoe UI", 32, "bold"))
vCategoryTitleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.15)

vTotalVoteCountLbl = CTkLabel(votingFrame, text="Total Vote Count\n0", font=("Segoe UI", 24, "bold"))
vTotalVoteCountLbl.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.15)

root.mainloop()

s.disconnect()