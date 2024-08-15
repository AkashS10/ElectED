from tkinter.ttk import Treeview, Style
from tkinter import messagebox
from datetime import datetime
from PIL import Image as Img
from customtkinter import *
from tkinter import *

set_appearance_mode("dark")

class UI(Frame):
    def __init__(self, parent, **kwargs):
        kwargs['bg'] = "#222222"
        super().__init__(parent, **kwargs)

        style = Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=35, fieldbackground="#343638", bordercolor="#343638", borderwidth=0, font=("Segoe UI", 12))
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=("Segoe UI", 14, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#565b5e')])

        parent.title("ElectED - Server")
        parent.minsize(1280, 720)
        parent.after(0, lambda: parent.state('zoomed'))
        parent.iconbitmap("res/icon.ico")

        self.header = CTkLabel(parent, fg_color="#333333", corner_radius=15, text="", image=CTkImage(None, Img.open('res/banner.png'), (1500, 90)))
        self.header.place(relx=0.014, rely=0.0226, relwidth=0.972, relheight=0.1126)

        self.connectedClientsFrame = CTkFrame(parent, fg_color="#333333", corner_radius=20)
        self.connectedClientsFrame.place(relx=0.014, rely=0.156, relwidth=0.479, relheight=0.33)

        self.logFrame = CTkFrame(parent, fg_color="#333333", corner_radius=20)
        self.logFrame.place(relx=0.014, rely=0.5068, relwidth=0.479, relheight=0.33)
        
        self.votingInformationFrame = CTkFrame(parent, fg_color="#333333", corner_radius=20)
        self.votingInformationFrame.place(relx=0.507, rely=0.156, relwidth=0.479, relheight=0.688)

        self.quickControlsFrame = CTkFrame(parent, fg_color="#333333", corner_radius=15)
        self.quickControlsFrame.place(relx=0.014, rely=0.864, relwidth=0.972, relheight=0.1)

        connectedClientsLbl = CTkLabel(self.connectedClientsFrame, text="Connected Clients", font=("Segoe UI", 20, "bold"))
        connectedClientsLbl.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.1)

        self.connectedClientsTV = Treeview(self.connectedClientsFrame, columns=("c1", "c2", "c3", "c4"), show="headings")
        self.connectedClientsTV.column("#1", anchor=CENTER, width=21)
        self.connectedClientsTV.heading("#1", text="S.NO")
        self.connectedClientsTV.column("#2", anchor=CENTER, width=300)
        self.connectedClientsTV.heading("#2", text="Category Name")
        self.connectedClientsTV.column("#3", anchor=CENTER, width=150)
        self.connectedClientsTV.heading("#3", text="Name")
        self.connectedClientsTV.column("#4", anchor=CENTER, width=150)
        self.connectedClientsTV.heading("#4", text="N.O of votes")
        self.connectedClientsTV.place(relx=0.025, rely=0.2, relwidth=0.925, relheight=0.75)
        self.connectedClientsTVScrollbar = CTkScrollbar(self.connectedClientsFrame, command=self.connectedClientsTV.yview)
        self.connectedClientsTVScrollbar.place(relx=0.95, rely=0.2, relwidth=0.025, relheight=0.75)
        self.connectedClientsTV.configure(yscrollcommand=self.connectedClientsTVScrollbar.set)

        connectedClientsLbl = CTkLabel(self.votingInformationFrame, text="Voting Information", font=("Seoge UI", 20, "bold"))
        connectedClientsLbl.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.1)

        self.votingInformationTV = Treeview(self.votingInformationFrame, columns=("c1", "c2", "c3", "c4"), show="headings")
        self.votingInformationTV.column("#1", anchor=CENTER, width=21)
        self.votingInformationTV.heading("#1", text="S.NO")
        self.votingInformationTV.column("#2", anchor=CENTER, width=300)
        self.votingInformationTV.heading("#2", text="Candidate Name")
        self.votingInformationTV.column("#3", anchor=CENTER, width=150)
        self.votingInformationTV.heading("#3", text="Party Name")
        self.votingInformationTV.column("#4", anchor=CENTER, width=150)
        self.votingInformationTV.heading("#4", text="N.O of votes")
        self.votingInformationTV.place(relx=0.025, rely=0.1, relwidth=0.925, relheight=0.86)
        self.votingInformationTVScrollbar = CTkScrollbar(self.votingInformationFrame, command=self.connectedClientsTV.yview)
        self.votingInformationTVScrollbar.place(relx=0.95, rely=0.1, relwidth=0.025, relheight=0.86)
        self.votingInformationTV.configure(yscrollcommand=self.votingInformationTVScrollbar.set)

        self.logEnt = CTkTextbox(self.logFrame)
        self.logEnt.configure(state="disabled")
        self.logEnt.place(relx=0.02, rely=0.05, relwidth=0.96, relheight=0.9)

        self.manageCategoriesBtn = CTkButton(self.quickControlsFrame, text="Manage Categories", corner_radius=10, font=("Segoe UI", 18))
        self.manageCategoriesBtn.place(relx=0.01, rely=0.125, relwidth=0.225, relheight=0.75)

        self.manageCandidatesBtn = CTkButton(self.quickControlsFrame, text="Manage Candidates", corner_radius=10, font=("Segoe UI", 18))
        self.manageCandidatesBtn.place(relx=0.24, rely=0.125, relwidth=0.225, relheight=0.75)

        self.disconnectClientBtn = CTkButton(self.quickControlsFrame, text="Disconnect client", corner_radius=10, font=("Segoe UI", 18), command=self.disconnectClientFunc)
        self.disconnectClientBtn.place(relx=0.47, rely=0.125, relwidth=0.225, relheight=0.75)

        self.place(relx=0, rely=0, relwidth=1, relheight=1)

    def updateConnectedClientsTV(self, values):
        items = self.getAllChildren(self.connectedClientsTV)
        for item in items:
            self.connectedClientsTV.delete(item)
        
        for i in values:
            self.connectedClientsTV.insert('', 'end', values=(i[0], i[1], i[2], i[3]))

    def updateVotingInformationTV(self, values):
        items = self.getAllChildren(self.votingInformationTV)
        for item in items:
            self.votingInformationTV.delete(item)
        
        for i in values:
            self.votingInformationTV.insert('', 'end', values=(i[0], i[1], i[2], i[3]))

    def getAllChildren(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.getAllChildren(tree, child)
        return children
    
    def log(self, message):
        self.logEnt.configure(state="normal")
        self.logEnt.insert(END, f"[{datetime.now().strftime('%I:%M:%S %p')}] {message}\n")
        self.logEnt.configure(state="disabled")
    
    def disconnectClientFunc(self):
        if len(self.connectedClientsTV.selection()) == 0:
            messagebox.showerror("ElectED - Server", "Please select a client")
            return
        self.disconnect(self.connectedClientsTV.item(self.connectedClientsTV.selection())['values'][0]-1)
        
if __name__ == "__main__":
    import os
    os.chdir("Server")
    import server