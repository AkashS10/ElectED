# TODO Remove this block after finishing development
import os
if os.getcwd()[-6:] != "Server":
    os.chdir("Server")

import threading
import socket

import databaseHandler
import ui

root = ui.Tk()
uiFrame = ui.UI(root)
connectedClients = []

class Client:
    def __init__(self, c):
        self.c = c
        self.thread = threading.Thread(target=self.recv, daemon=True)

    def recv(self):
        while True:
            try:
                data, addr = self.c.recvfrom(1024)
            except Exception as e:
                print("Error: ", e)
                self.c.close()
                break
            print("Data received: ", data.decode())

def socketAcceptLoop():
    while True:
        c, addr = s.accept()
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
