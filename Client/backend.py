from win32api import GetSystemMetrics
from PIL import Image as Img
from tkinter import messagebox
from customtkinter import *
import threading
import hashlib
import socket
import mouse
import math
import os

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
        f.write(f"{ip}")
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
            try:
                data, addr = self.s.recvfrom(4096)
                data = data.decode()
            except ConnectionResetError:
                self.disconnect(serverClosed=True)
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
                self.configureFrame.place_forget()
                self.root.wm_attributes("-fullscreen", True)
                self.root.state("zoomed")
                self.votingFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
                self.vCategoryTitleLbl.configure(text=f"Vote for {self.category} candidate")
            elif data.startswith("/cae/"):
                self.messagebox.showerror("ElectED", f"Another client has already chosen this category\nPlease select some other category")
            elif data.startswith("/bye/"):
                self.disconnect(serverClosed=True)
                break
            elif data.startswith("/dis/"):
                self.disconnect(disconnected=True)
                break
            elif data == "/nr/":
                self.waitingOverlay.place_forget()
                self.numVotes += 1
                self.vTotalVoteCountLbl.configure(text=f"Total Vote Count\n{self.numVotes}")
    
    def displayCandidates(self):
        numRows = math.ceil(len(self.candidates) / 4)
        horizontalSpacing = 0.015
        verticalSpacing = 0.025
        width = 0.23125
        height = 0.4

        if numRows == 1:
            j = 0.5
            numCols = len(self.candidates)
            for i in range(numCols):
                CandidateFrame(self.votingFrame, self.candidates[(math.floor(j) * 4) + i], self).place(relx=((width * i) + horizontalSpacing * (i + 1)) + (((4 - numCols) * (width + horizontalSpacing)) / 2), rely=0.125 + (height * j) + verticalSpacing * (j + 1), relwidth=width, relheight=height)
        elif numRows == 2:
            for j in range(2):
                numCols = 4 if j == 0 else len(self.candidates) - 4
                for i in range(numCols):
                    CandidateFrame(self.votingFrame, self.candidates[(math.floor(j) * 4) + i], self).place(relx=((width * i) + horizontalSpacing * (i + 1)) + (((4 - numCols) * (width + horizontalSpacing)) / 2), rely=0.125 + (height * j) + verticalSpacing * (j + 1), relwidth=width, relheight=height)

        self.waitingOverlay = CTkFrame(self.votingFrame)
        waitingLbl = CTkLabel(self.waitingOverlay, text="Vote casted successfully\nWaiting for next round...", font=("Segoe UI", 28, "bold"))
        waitingLbl.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.numVotes = 0
        for i in self.candidates:
            self.numVotes += int(i[5])
        self.vTotalVoteCountLbl.configure(text=f"Total Vote Count\n{self.numVotes}")
    
    def beginVoting(self, category, configureFrame, vCategoryTitleLbl, vTotalVoteCountLbl):
        if category == "Select...":
            self.messagebox.showerror("ElectED", "Select a category to begin voting")
            return
        self.s.send(f"/cts/{category}".encode()) # CTS - CaTegory Select
        self.configureFrame = configureFrame
        self.vCategoryTitleLbl = vCategoryTitleLbl
        self.vTotalVoteCountLbl = vTotalVoteCountLbl
        self.category = category

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
    def __init__(self, parent, info, networkHandler, **kwargs):
        kwargs['corner_radius'] = 20
        kwargs['fg_color'] = ("#c8c8c8", "#545454")
        super().__init__(parent, **kwargs)
        self.networkHandler = networkHandler
        self.id = info[0]
        candidateName = info[2]
        partyName = info[3]
        partyArtPath = info[4]

        pNameLbl = CTkLabel(self, text=candidateName + " - " + partyName, font=("Segoe UI", 20, "bold"))
        pNameLbl.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.1)

        try:
            pImage = CTkLabel(self, text="", image=CTkImage(None, Img.open(partyArtPath), (320, 260)))
            pImage.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.75)
        except:
            messagebox.showerror("ElectED Lite", f"Party Art image {partyArtPath} doesn't exist")
            sys.exit()

        self.bind("<Button-1>", self.callback)
        pNameLbl.bind("<Button-1>", self.callback)
        pImage.bind("<Button-1>", self.callback)
    
    def callback(self, e):
        self.networkHandler.waitingOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        x = GetSystemMetrics(0)/2
        y = GetSystemMetrics(1)/2
        mouse.move(x, y)

        self.networkHandler.s.send(f"/vc/{self.id}".encode()) #VC - Vote Candidate