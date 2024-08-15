from PIL import Image as Img
from customtkinter import *
import threading
import hashlib
import socket
import os

set_appearance_mode("dark")

class NetworkHandler:
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
        match len(self.candidates):
            case 2:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][2], self.candidates[0][3], self.candidates[0][4])
                c1.place(relx=0.2, rely=0.375, relwidth=0.225, relheight=0.4)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][2], self.candidates[1][3], self.candidates[1][4])
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
        except Exception:
            pass
        if disconnected:
            self.messagebox.showinfo("ElectED", "You were disconnected from the Server")
        elif serverClosed:
            self.messagebox.showinfo("ElectED", "Server Closed")
        lof = os.listdir(".")
        for i in lof:
            if i.endswith(".png"):
                os.remove(i)
        try:
            self.root.destroy()
        except:
            pass
        exit()

class CandidateFrame(CTkFrame):
    def __init__(self, parent, candidateName, partyName, partyArtPath, **kwargs):
        kwargs['corner_radius'] = 20
        super().__init__(parent, **kwargs)

        nameLbl = CTkLabel(self, text=candidateName, font=("Seoge UI", 24, "bold"), corner_radius=20)
        nameLbl.place(relx=0.1, rely=0.04, relwidth=0.8, relheight=0.15)

        pNameLbl = CTkLabel(self, text=partyName, font=("Segoe UI", 20))
        pNameLbl.place(relx=0.2, rely=0.19, relwidth=0.6, relheight=0.1)

        pImage = CTkLabel(self, text="", image=CTkImage(None, Img.open(partyArtPath), (200, 200)))
        pImage.place(relx=0.175, rely=0.315, relwidth=0.65, relheight=0.65)

        self.bind("<Button-1>", self.callback)
        nameLbl.bind("<Button-1>", self.callback)
        pNameLbl.bind("<Button-1>", self.callback)
        pImage.bind("<Button-1>", self.callback)
    
    def callback(self, e):
        # Communicate to server, move mouse to center, overlay waiting frame and wait for command from server for next round
        print("Clicked")

if __name__ == "__main__":
    import os
    os.chdir("Client")
    import main # type: ignore