# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Server":
    os.chdir("Server")

import threading
import socket

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
                data, addr = self.c.recvfrom(1024)
                data = data.decode()
            except Exception as e:
                print("Error: ", e)
                self.c.close()
                break
            if data == "": break
            elif data == "/d/":
                print("Client disconnected")
                self.disconnect()
                break
            elif data.startswith("/cts/"):
                data = data[5:]
                for i in database.getCategories():
                    if i[1] == data:
                        self.categoryID = i[0]
                        self.category = i[1]
                print(f"{self.hostname if self.hostname != None else 'Client'} chose category {self.category}, {self.categoryID}")
                updateConnectedClientsTV()
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
