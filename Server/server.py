import threading
import hashlib
import socket
import time

import databaseHandler
import ui

class Client:
    def __init__(self, c):
        self.c = c
        self.categories = []
        self.categoryID = None
        self.category = None
        self.hostname = None
        self.numVotes = 0
        self.voted = False
        for i in database.getCategories():
            self.categories.append(i[1])
        self.c.send(f"/act/{self.categories}".encode()) # ACT - Available CaTegories
        self.thread = threading.Thread(target=self.recv, daemon=True)
        self.thread.start()

    def recv(self):
        while True:
            try:
                data, addr = self.c.recvfrom(4096)
                data = data.decode()
            except Exception as e:
                disconnect(self)
                return
            if data == "": break
            elif data == "/d/":
                uiFrame.log(f"{self.hostname if self.hostname != None else 'Client'} disconnected")
                disconnect(self)
                break
            elif data.startswith("/cts/"):
                if data[5:] in [uiFrame.connectedClientsTV.item(i, 'values')[1] for i in ui.getAllChildren(uiFrame.connectedClientsTV)]:
                    self.c.send(b"/cae/")
                    continue
                data = data[5:]
                for i in database.getCategories():
                    if i[1] == data:
                        self.categoryID = int(i[0])
                        self.category = i[1]
                uiFrame.log(f"{self.hostname if self.hostname != None else 'Client'} chose category {self.category}, {self.categoryID}")
                updateConnectedClientsTV()
                candidates = []
                for i in database.getCandidates(hideVotes=False):
                    if i[1] == self.category:
                        candidates.append(i)
                for imagePath in candidates:
                    imagePath = imagePath[4]
                    f = open(f"partyArt/{imagePath}", "rb")
                    image = f.read()
                    f.close()
                    self.c.send(f"/pim/{imagePath}/{len(image)}/{hashlib.sha256(image).hexdigest()}/".encode()) # PIM - Party IMage
                    time.sleep(0.1)
                    self.c.send(image)
                self.c.send(f"/cdl/{candidates}".encode()) # CDL - CanDidates List

            elif data.startswith("/hn/"):
                data = data[4:]
                self.hostname = data
                uiFrame.log(f"Received hostname: {self.hostname}")
                updateConnectedClientsTV()

            elif data.startswith("/vc/"):
                if self.voted: continue
                data = data[4:]
                id = int(data)
                database.voteCandidate(id)
                self.numVotes += 1
                self.voted = True
                updateConnectedClientsTV()
                updateVotingInformationTV()
                
                uiFrame.log(f"Recieved vote from {self.hostname}")

                allVoted = True
                for i in connectedClients:
                    allVoted = allVoted and i.voted
                if allVoted:  
                    for i in connectedClients:
                        i.voted = False
                        i.c.send("/nr/".encode()) # NR - Next Round
            else:
                uiFrame.log(f"Data received from {self.hostname if self.hostname else 'a client'}: {data}")

def disconnect(self, kicked=False):
    if type(self) == int:
        disconnect(connectedClients[self], True)
        return
    if self not in connectedClients:
        return
    connectedClients.remove(self)
    try:
        if kicked:
            self.c.send("/dis/".encode())
            uiFrame.log(f"{self.hostname} was disconnected from the server")
        else:
            self.c.send("/bye/".encode())
        try:
            self.thread.join(0)
        except RuntimeError:
            pass
    except (ConnectionResetError, OSError) as e:
        pass
    try:
        updateConnectedClientsTV()
    except:
        pass
    self.c.close()
    allVoted = True
    for i in connectedClients:
        allVoted = allVoted and i.voted
    if allVoted:  
        for i in connectedClients:
            i.voted = False
            i.c.send("/nr/".encode()) # NR - Next Round

def updateConnectedClientsTV():
    values = []
    for i in range(0, len(connectedClients)):
        values.append((i+1, connectedClients[i].category, connectedClients[i].hostname, connectedClients[i].numVotes))
    uiFrame.updateConnectedClientsTV(values)

def updateVotingInformationTV():
    values = []
    for i in database.getCandidates():
        values.append((i[0], i[1], i[2], i[3], i[5]))
    uiFrame.updateVotingInformationTV(values)

def socketAcceptLoop():
    while True:
        try:
            c, addr = s.accept()
        except OSError:
            return
        uiFrame.log("Client connected")
        connectedClients.append(Client(c))

def closeServer():
    for client in connectedClients:
        disconnect(client)
    tSocketLoop.join(0)
    database.database.close()
    s.close()

root = ui.CTk()
uiFrame = ui.UI(root)
uiFrame.disconnect = disconnect
uiFrame.closeServer = closeServer
connectedClients = []

ip = "0.0.0.0"
port = 15165
s = socket.socket()
s.bind((ip, port))
s.listen()
tSocketLoop = threading.Thread(target=socketAcceptLoop, daemon=True)
tSocketLoop.start()

database = databaseHandler.DatabaseHandler()
uiFrame.database = database
updateVotingInformationTV()

uiFrame.log(f"Server running on {ip}:{port}")

root.mainloop()
closeServer()
