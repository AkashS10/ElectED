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

def socketLoop():
    while True:
        c, addr = s.accept()
        connectedClients.append(c)

database = databaseHandler.databaseHandler()

s = socket.socket()
s.bind(("0.0.0.0", 15165))
s.listen()
tSocketLoop = threading.Thread(target=socketLoop, daemon=True)
tSocketLoop.start()

root.mainloop()
tSocketLoop.join(0)
