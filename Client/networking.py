from customtkinter import *
import threading
import hashlib
import socket
import os

class SocketConnHandler:
    def __init__(self, messagebox, root):
        self.s = socket.socket()
        self.connected = False
        self.candidates = []
        self.messagebox = messagebox
        self.root = root
        self.votingFrame = None

    def connect(self, ip, port, changeState):
        try:
            port = int(port)
        except ValueError:
            self.messagebox.showerror("ElectED", "Please enter a valid port")
            return
        try:
            self.s.connect((ip, port))
            self.connected = True
        except Exception:
            self.messagebox.showerror("ElectED", "Invalid IP/Port")
            return
        
        f = open("previousConnection.txt", "w+")
        f.write(f"{ip}|{port}")
        f.close()
        self.s.send(f"/hn/{socket.gethostname()}".encode())

        data, addr = self.s.recvfrom(4096)
        data = data.decode()
        if data.startswith("/act/"):
            data = data[5:]
            changeState(data)
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
                    self.messagebox.showerror("ElectED", f"Failed to verify image integrity")
                    self.root.destroy()
                    exit()

                f = open(filename, "wb+")
                try:
                    f.write(buffer)
                except Exception as e:
                    self.messagebox.showerror("ElectED", f"Failed to receieve images, exiting the app\nError: {e}")
                    self.root.destroy()
                    exit()
                f.close()
            elif data.startswith("/cdl/"):
                self.candidates = eval(data[5:])
                self.displayCandidates()
            elif data.startswith("/bye/"):
                self.disconnect(serverClosed=True)
                break
            elif data.startswith("/dis/"):
                self.disconnect(disconnected=True)
                break
    
    def displayCandidates(self):
        if len(self.candidates) == 2:
            c1 = CTkFrame(self.votingFrame, corner_radius=20)
            c1.place(relx=0.2, rely=0.375, relwidth=0.225, relheight=0.4)
            c2 = CTkFrame(self.votingFrame, corner_radius=20)
            c2.place(relx=0.575, rely=0.375, relwidth=0.225, relheight=0.4)
    
    def beginVoting(self, category, configureFrame, vCategoryTitleLbl):
        if category == "Select...":
            self.messagebox.showerror("ElectED", "Select a category to begin voting")
            return
        self.s.send(f"/cts/{category}".encode()) # CTS - CaTegory Select
        
        configureFrame.place_forget()
        self.root.wm_attributes("-fullscreen", True)
        self.root.state("zoomed")
        self.votingFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        vCategoryTitleLbl.configure(text=f"Vote for {category} candidate")

    def disconnect(self, disconnected=False, serverClosed=False):
        try:
            self.thread.join(0)
            self.s.send("/d/".encode())
            self.s.close()
        except AttributeError or ConnectionResetError:
            pass
        if disconnected:
            self.messagebox.showinfo("ElectED", "You were disconnected from the Server")
        elif serverClosed:
            self.messagebox.showinfo("ElectED", "Server Closed")
        self.root.destroy()
        lof = os.listdir(".")
        for i in lof:
            if i.endswith(".png"):
                os.remove(i)
        exit()