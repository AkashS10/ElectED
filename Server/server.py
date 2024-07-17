# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Server":
    os.chdir("Server")

import threading
import hashlib
import socket
import time

import databaseHandler
import ui

root = ui.CTk()
uiFrame = ui.UI(root)
connectedClients = []

class Client:
    def __init__(self, c):
        self.c = c
        self.categories = []
        self.categoryID = None
        self.category = None
        self.hostname = None
        self.numVotes = 0
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
                print("Error: ", e)
                self.c.close()
                break
            if data == "": break
            elif data == "/d/":
                print(f"{self.hostname if self.hostname != None else 'Client'} disconnected")
                self.disconnect()
                break
            elif data.startswith("/cts/"):
                data = data[5:]
                for i in database.getCategories():
                    if i[1] == data:
                        self.categoryID = int(i[0])
                        self.category = i[1]
                print(f"{self.hostname if self.hostname != None else 'Client'} chose category {self.category}, {self.categoryID}")
                updateConnectedClientsTV()
                candidates = []
                for i in database.getCandidates():
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
                print(f"Received hostname: {self.hostname}")
                updateConnectedClientsTV()
            else:
                print("Data received: ", data)
    
    def disconnect(self):
        connectedClients.remove(self)
        updateConnectedClientsTV()
        self.c.close()

def updateConnectedClientsTV():
    values = []
    for i in range(0, len(connectedClients)):
        values.append((i+1, connectedClients[i].category, connectedClients[i].hostname, connectedClients[i].numVotes))
    uiFrame.updateConnectedClientsTV(values)

def socketAcceptLoop():
    while True:
        c, addr = s.accept()
        print("Client connected")
        connectedClients.append(Client(c))

database = databaseHandler.DatabaseHandler()

s = socket.socket()
s.bind(("0.0.0.0", 15165))
s.listen()
tSocketLoop = threading.Thread(target=socketAcceptLoop, daemon=True)
tSocketLoop.start()

root.mainloop()
#Disconnect before stopping the thread
for client in connectedClients:
    client.c.close()
    client.thread.join(0)
tSocketLoop.join(0)
database.database.close()
