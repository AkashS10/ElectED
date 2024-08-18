from PIL import Image as Img
from customtkinter import *
from win32api import GetSystemMetrics
import threading
import hashlib
import socket
import mouse
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
            elif data.startswith("/bye/"):
                self.disconnect(serverClosed=True)
                break
            elif data.startswith("/dis/"):
                self.disconnect(disconnected=True)
                break
            elif data == "/nr/":
                self.waitingOverlay.place_forget()
    
    def displayCandidates(self):
        match len(self.candidates):
            case 2:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.2, rely=0.375, relwidth=0.225, relheight=0.4)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.575, rely=0.375, relwidth=0.225, relheight=0.4)
            case 3:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.1225, rely=0.375, relwidth=0.225, relheight=0.4)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.3925, rely=0.375, relwidth=0.225, relheight=0.4)

                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.6625, rely=0.375, relwidth=0.225, relheight=0.4)
            case 4:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.0625, rely=0.375, relwidth=0.2, relheight=0.4)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.2875, rely=0.375, relwidth=0.2, relheight=0.4)
                
                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.5125, rely=0.375, relwidth=0.2, relheight=0.4)

                c4 = CandidateFrame(self.votingFrame, self.candidates[3][0], self.candidates[3][2], self.candidates[3][3], self.candidates[3][4], self)
                c4.place(relx=0.7375, rely=0.375, relwidth=0.2, relheight=0.4)
            case 5:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.0225, rely=0.375, relwidth=0.18, relheight=0.38)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.2125, rely=0.375, relwidth=0.18, relheight=0.38)
                
                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.4025, rely=0.375, relwidth=0.18, relheight=0.38)

                c4 = CandidateFrame(self.votingFrame, self.candidates[3][0], self.candidates[3][2], self.candidates[3][3], self.candidates[3][4], self)
                c4.place(relx=0.5925, rely=0.375, relwidth=0.18, relheight=0.38)

                c5 = CandidateFrame(self.votingFrame, self.candidates[4][0], self.candidates[4][2], self.candidates[4][3], self.candidates[4][4], self)
                c5.place(relx=0.7825, rely=0.375, relwidth=0.18, relheight=0.38)
            case 6:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
                
                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)

                c4 = CandidateFrame(self.votingFrame, self.candidates[3][0], self.candidates[3][2], self.candidates[3][3], self.candidates[3][4], self)
                c4.place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)

                c5 = CandidateFrame(self.votingFrame, self.candidates[4][0], self.candidates[4][2], self.candidates[4][3], self.candidates[4][4], self)
                c5.place(relx=0.2, rely=0.595, relwidth=0.2, relheight=0.38)

                c6 = CandidateFrame(self.votingFrame, self.candidates[5][0], self.candidates[5][2], self.candidates[5][3], self.candidates[5][4], self)
                c6.place(relx=0.575, rely=0.595, relwidth=0.2, relheight=0.38)
            case 7:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
                
                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)

                c4 = CandidateFrame(self.votingFrame, self.candidates[3][0], self.candidates[3][2], self.candidates[3][3], self.candidates[3][4], self)
                c4.place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)

                c5 = CandidateFrame(self.votingFrame, self.candidates[4][0], self.candidates[4][2], self.candidates[4][3], self.candidates[4][4], self)
                c5.place(relx=0.1225, rely=0.595, relwidth=0.2, relheight=0.38)

                c6 = CandidateFrame(self.votingFrame, self.candidates[5][0], self.candidates[5][2], self.candidates[5][3], self.candidates[5][4], self)
                c6.place(relx=0.3925, rely=0.595, relwidth=0.2, relheight=0.38)

                c7 = CandidateFrame(self.votingFrame, self.candidates[6][0], self.candidates[6][2], self.candidates[6][3], self.candidates[6][4], self)
                c7.place(relx=0.6625, rely=0.595, relwidth=0.2, relheight=0.38)
            case 8:
                c1 = CandidateFrame(self.votingFrame, self.candidates[0][0], self.candidates[0][2], self.candidates[0][3], self.candidates[0][4], self)
                c1.place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)

                c2 = CandidateFrame(self.votingFrame, self.candidates[1][0], self.candidates[1][2], self.candidates[1][3], self.candidates[1][4], self)
                c2.place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
                
                c3 = CandidateFrame(self.votingFrame, self.candidates[2][0], self.candidates[2][2], self.candidates[2][3], self.candidates[2][4], self)
                c3.place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)

                c4 = CandidateFrame(self.votingFrame, self.candidates[3][0], self.candidates[3][2], self.candidates[3][3], self.candidates[3][4], self)
                c4.place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)
                
                c5 = CandidateFrame(self.votingFrame, self.candidates[4][0], self.candidates[4][2], self.candidates[4][3], self.candidates[4][4], self)
                c5.place(relx=0.0625, rely=0.595, relwidth=0.2, relheight=0.38)

                c6 = CandidateFrame(self.votingFrame, self.candidates[5][0], self.candidates[5][2], self.candidates[5][3], self.candidates[5][4], self)
                c6.place(relx=0.2875, rely=0.595, relwidth=0.2, relheight=0.38)
                
                c7 = CandidateFrame(self.votingFrame, self.candidates[6][0], self.candidates[6][2], self.candidates[6][3], self.candidates[6][4], self)
                c7.place(relx=0.5125, rely=0.595, relwidth=0.2, relheight=0.38)

                c8 = CandidateFrame(self.votingFrame, self.candidates[7][0], self.candidates[7][2], self.candidates[7][3], self.candidates[7][4], self)
                c8.place(relx=0.7375, rely=0.595, relwidth=0.2, relheight=0.38)
        self.waitingOverlay = CTkFrame(self.votingFrame)
        waitingLbl = CTkLabel(self.waitingOverlay, text="Waiting for next round...", font=("Segoe UI", 28, "bold"))
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
        
        configureFrame.place_forget()
        self.root.wm_attributes("-fullscreen", True)
        self.root.state("zoomed")
        self.votingFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        vCategoryTitleLbl.configure(text=f"Vote for {category} candidate")
        self.vTotalVoteCountLbl = vTotalVoteCountLbl

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
    def __init__(self, parent, id, candidateName, partyName, partyArtPath, networkHandler, **kwargs):
        kwargs['corner_radius'] = 20
        super().__init__(parent, **kwargs)
        self.networkHandler = networkHandler
        self.id = id

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
        self.networkHandler.waitingOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        x = GetSystemMetrics(0)/2
        y = GetSystemMetrics(1)/2
        mouse.move(x, y)

        self.networkHandler.s.send(f"/vc/{self.id}".encode()) #VC - Vote Candidate
        self.networkHandler.numVotes += 1
        self.networkHandler.vTotalVoteCountLbl.configure(text=f"Total Vote Count\n{self.networkHandler.numVotes}")

if __name__ == "__main__":
    import os
    os.chdir("Client")
    import main # type: ignore