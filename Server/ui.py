from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview, Style
from datetime import datetime
from PIL import Image as Img
from customtkinter import *
from ctypes import windll
from tkinter import *
import pandas as pd
import sqlite3
import os

set_appearance_mode("dark")

class UI(Frame):
    def __init__(self, parent, **kwargs):
        kwargs['bg'] = "#222222"
        super().__init__(parent, **kwargs)

        style = Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=35, fieldbackground="#2a2d2e", bordercolor="#343638", borderwidth=0, font=("Segoe UI", 12))
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=("Segoe UI", 14, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#565b5e')])

        parent.title("ElectED - Server")
        parent.minsize(1280, 720)
        parent.after(0, lambda: parent.state('zoomed'))
        parent.iconbitmap("res/icon.ico")
        self.parent = parent
        self.startDt = datetime.now()
        self.roundMode = True

        if not os.path.exists("res/banner.png"):
            messagebox.showerror("ElectED", "Banner image not found\nPlace a PNG image named \"banner.png\" with the resolution 1878x116\nQuitting the app")
            exit()
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

        self.votingModeBtn = CTkButton(self.votingInformationFrame, text="🖧", font=("Segoe UI", 20), command=self.changeVotingMode)
        self.votingModeBtn.place(relx=0.775, rely=0.015, relwidth=0.075, relheight=0.075)

        hideVotesBtn = CTkButton(self.votingInformationFrame, text="👁", command=self.hideVotes, font=("Segoe UI", 20))
        hideVotesBtn.place(relx=0.875, rely=0.015, relwidth=0.075, relheight=0.075)

        self.votingInformationTV = Treeview(self.votingInformationFrame, columns=("c1", "c2", "c3", "c4", "c5"), show="headings")
        self.votingInformationTV.column("#1", anchor=CENTER, width=50)
        self.votingInformationTV.heading("#1", text="S.NO")
        self.votingInformationTV.column("#2", anchor=CENTER, width=100)
        self.votingInformationTV.heading("#2", text="Category")
        self.votingInformationTV.column("#3", anchor=CENTER, width=250)
        self.votingInformationTV.heading("#3", text="Candidate Name")
        self.votingInformationTV.column("#4", anchor=CENTER, width=150)
        self.votingInformationTV.heading("#4", text="Party Name")
        self.votingInformationTV.column("#5", anchor=CENTER, width=150)
        self.votingInformationTV.heading("#5", text="N.O of votes")
        self.votingInformationTV.place(relx=0.025, rely=0.1, relwidth=0.925, relheight=0.86)
        self.votingInformationTVScrollbar = CTkScrollbar(self.votingInformationFrame, command=self.votingInformationTV.yview)
        self.votingInformationTVScrollbar.place(relx=0.95, rely=0.1, relwidth=0.025, relheight=0.86)
        self.votingInformationTV.configure(yscrollcommand=self.votingInformationTVScrollbar.set)

        self.logEnt = CTkTextbox(self.logFrame)
        self.logEnt.configure(state="disabled")
        self.logEnt.place(relx=0.02, rely=0.05, relwidth=0.96, relheight=0.9)

        self.manageCategoriesBtn = CTkButton(self.quickControlsFrame, text="Manage Categories", corner_radius=10, font=("Segoe UI", 20), command=self.manageCategoryFunc)
        self.manageCategoriesBtn.place(relx=0.005, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.manageCandidatesBtn = CTkButton(self.quickControlsFrame, text="Manage Candidates", corner_radius=10, font=("Segoe UI", 20), command=self.manageCandidatesFunc)
        self.manageCandidatesBtn.place(relx=0.25375, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.disconnectClientBtn = CTkButton(self.quickControlsFrame, text="Disconnect client", corner_radius=10, font=("Segoe UI", 20), command=self.disconnectClientFunc)
        self.disconnectClientBtn.place(relx=0.5025, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.concludeVotingBtn = CTkButton(self.quickControlsFrame, text="Conclude Voting", corner_radius=10, font=("Segoe UI", 20), command=self.concludeVotingFunc)
        self.concludeVotingBtn.place(relx=0.75125, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.place(relx=0, rely=0, relwidth=1, relheight=1)

    def changeVotingMode(self):
        if len(getAllChildren(self.connectedClientsTV)) != 0:
            messagebox.showinfo("ElectED - Server", "Please disconnect all clients before switching modes")
            return
        self.roundMode = not self.roundMode
        if self.roundMode:
            self.votingModeBtn.configure(text="🖧")
        else:
            self.votingModeBtn.configure(text="⏱")

    def hideVotes(self):
        self.database.hideVotes = not self.database.hideVotes
        values = []
        for i in self.database.getCandidates():
            values.append((i[0], i[1], i[2], i[3], i[5]))
        self.updateVotingInformationTV(values)
        
    def updateConnectedClientsTV(self, values):
        items = getAllChildren(self.connectedClientsTV)
        for item in items:
            self.connectedClientsTV.delete(item)
        
        for i in values:
            self.connectedClientsTV.insert('', 'end', values=(i[0], i[1], i[2], i[3]))

    def updateVotingInformationTV(self, values):
        items = getAllChildren(self.votingInformationTV)
        for item in items:
            self.votingInformationTV.delete(item)
        
        for i in values:
            self.votingInformationTV.insert('', 'end', values=(i[0], i[1], i[2], i[3], i[4]))
    
    def log(self, message):
        self.logEnt.configure(state="normal")
        self.logEnt.insert(END, f"[{datetime.now().strftime('%I:%M:%S %p')}] {message}\n")
        self.logEnt.configure(state="disabled")
        self.logEnt.see('end')
    
    def disconnectClientFunc(self):
        if len(self.connectedClientsTV.selection()) == 0:
            messagebox.showerror("ElectED - Server", "Please select a client")
            return
        self.disconnect(self.connectedClientsTV.item(self.connectedClientsTV.selection())['values'][0]-1)
    
    def manageCategoryFunc(self):
        self.manageCategoriesBtn.configure(state="disabled")
        mc = ManageCategory(self.manageCategoriesBtn, self.database)
        mc.updateParentTV = self.updateVotingInformationTV
        mc.connectedClientsTV = self.connectedClientsTV
        mc.disconnect = self.disconnectClientFunc
    
    def manageCandidatesFunc(self):
        if len(getAllChildren(self.connectedClientsTV)) != 0:
            messagebox.showinfo("ElectED - Server", "Please disconnect all clients before editing candidates")
            return
        self.manageCandidatesBtn.configure(state="disabled")
        mc = ManageCandidates(self.manageCandidatesBtn, self.database, self.updateVotingInformationTV)

    def concludeVotingFunc(self):
        self.closeServer()
        self.log("Server closed, voting concluded")
        delta = datetime.now() - self.startDt
        minutes = delta.seconds//60
        seconds = delta.seconds%60
        hours = minutes//60
        minutes = minutes%60
        self.log(f"Voting for {hours}h, {minutes}m and {seconds}s")

        database = sqlite3.connect("database.db")
        db = database.cursor()
               
        data = []
        index = []
        db.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryName")
        categories = db.fetchall()
        for i in categories:
            data += [["", "", ""],]
            index += [i[1],]
            db.execute(f"SELECT PartyName, CandidateName, NumVotes FROM Candidates WHERE Category={i[0]} ORDER BY NumVotes")
            sno = 1
            for x in db.fetchall():
                index += [sno,]
                sno += 1
                data += [x]
            index += ["",]
            data += [["", "", ""],]
        index += ["", "Winners"]
        data += [["", "", ""], ["", "", ""]]
        db.execute("SELECT CategoryName, PartyName, CandidateName, MAX(NumVotes) FROM Candidates A, Categories B WHERE A.Category = B.CategoryID GROUP BY CategoryName")
        for i in db.fetchall():
            index += [i[0],]
            data += [i[1:]]
        database.close()

        df = pd.DataFrame(data, index)
        df.columns = ["PartyName", "CandidateName", "NumVotes"]
        df.to_csv("Results.csv")
        self.log("Exported voting data to CSV")

        messagebox.showinfo("ElectED - Server", "Voting results have been saved to CSV\nPress Ok to close the app")
        exit()

class ManageCategory(CTkToplevel):
    def __init__(self, btn, database, *args, **kwargs):
        self.btn = btn
        self.database = database
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.minsize(1066, 600)
        self.resizable(False, False)
        self.geometry("1066x600+300+100")
        self.after(200, self.deiconify)
        self.title("ElectED - Manage Categories")

        self.titleLbl = CTkLabel(self, text="Manage Categories", font=("Segoe UI", 24, "bold"))
        self.titleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.175)

        self.categoryTV = Treeview(self, columns=("c1", "c2"), show="headings")
        self.categoryTV.column("#1", anchor=CENTER, width=50)
        self.categoryTV.heading("#1", text="Category ID")
        self.categoryTV.column("#2", anchor=CENTER, width=100)
        self.categoryTV.heading("#2", text="Category Name")
        self.categoryTV.place(relx=0.05, rely=0.175, relwidth=0.88, relheight=0.675)
        self.categoryTVScrollbar = CTkScrollbar(self, command=self.categoryTV.yview)
        self.categoryTVScrollbar.place(relx=0.93, rely=0.175, relwidth=0.02, relheight=0.675)
        self.categoryTV.configure(yscrollcommand=self.categoryTV.set)

        self.createCategoryBtn = CTkButton(self, text="Create Category", font=("Segoe UI", 18), command=self.createCategoryFunc)
        self.createCategoryBtn.place(relx=0.05, rely=0.875, relwidth=0.295, relheight=0.1)

        self.editCategoryBtn = CTkButton(self, text="Edit Category", font=("Segoe UI", 18), command=self.editCategoryFunc)
        self.editCategoryBtn.place(relx=0.35, rely=0.875, relwidth=0.295, relheight=0.1)

        self.deleteCategoryBtn = CTkButton(self, text="Delete Category", font=("Segoe UI", 18), command=self.deleteCategoryFunc)
        self.deleteCategoryBtn.place(relx=0.65, rely=0.875, relwidth=0.298, relheight=0.1)

        self.updateTV()
    
    def createCategoryFunc(self):
        categoryName = simpledialog.askstring("ElectED - Manage categories", "Enter category name")
        if categoryName == None: return
        if categoryName == "":
            messagebox.showerror("ElectED - Manage Categories", "Please enter a category name", parent=self)
            return
        self.database.createCategory(categoryName)
        messagebox.showinfo("ElectED - Manage Categories", f"Category {categoryName} successfully created", parent=self)
        self.updateTV()
    
    def editCategoryFunc(self):
        if len(self.categoryTV.selection()) == 0:
            messagebox.showerror("ElectED - Manage Categories", "Please select a category", parent=self)
            return
        categoryName = simpledialog.askstring("ElectED - Manage Categories", "Enter new category name", initialvalue=self.categoryTV.item(self.categoryTV.selection()[0], 'values')[1])
        if categoryName == None: return
        if categoryName == "":
            messagebox.showerror("ElectED - Manage Categories", "Please enter a category name", parent=self)
            return
        self.database.editCategory(self.categoryTV.item(self.categoryTV.selection()[0], 'values')[0], categoryName)
        for i in getAllChildren(self.connectedClientsTV):
                if self.connectedClientsTV.item(i, 'values')[1] == self.categoryTV.item(self.categoryTV.selection()[0], 'values')[1]:
                    self.connectedClientsTV.selection_set(i)
                    self.disconnect()
                    break
        messagebox.showinfo("ElectED - Manage Categories", "Category successfully edited", parent=self)
        self.updateTV()
        
        values = []
        for i in self.database.getCandidates():
            values.append((i[0], i[1], i[2], i[3], i[5]))
        self.updateParentTV(values)

    def deleteCategoryFunc(self):
        if len(self.categoryTV.selection()) == 0:
            messagebox.showerror("ElectED - Manage Categories", "Please select a category", parent=self)
            return
        if messagebox.askyesno("ElectED - Manage Categories", "Are you sure you want to delete the category and the candidates in that category?\nThis action is IRREVERSIBLE", parent=self):
            self.database.deleteCategory(self.categoryTV.item(self.categoryTV.selection()[0], 'values')[0])
            for i in getAllChildren(self.connectedClientsTV):
                if self.connectedClientsTV.item(i, 'values')[1] == self.categoryTV.item(self.categoryTV.selection()[0], 'values')[1]:
                    self.connectedClientsTV.selection_set(i)
                    self.disconnect()
                    break
            messagebox.showinfo("ElectED - Manage Categories", f"Category {self.categoryTV.item(self.categoryTV.selection()[0], 'values')[1]} deleted successfully", parent=self)
            self.updateTV()

            values = []
            for i in self.database.getCandidates():
                values.append((i[0], i[1], i[2], i[3], i[5]))
            self.updateParentTV(values)

    def onClose(self):
        self.btn.configure(state="normal")
        self.destroy()

    def updateTV(self):
        items = getAllChildren(self.categoryTV)
        for item in items:
            self.categoryTV.delete(item)
        for i in self.database.getCategories():
            self.categoryTV.insert('', 'end', values=i)

class ManageCandidates(CTkToplevel):
    def __init__(self, btn, database, updateParentTV, *args, **kwargs):
        self.btn = btn
        self.database = database
        self.updateParentTV = updateParentTV
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.minsize(1066, 600)
        self.resizable(False, False)
        self.geometry("1066x600+300+100")
        self.after(200, self.deiconify)
        self.title("ElectED - Manage Candidates")

        self.titleLbl = CTkLabel(self, text="Manage Candidates", font=("Segoe UI", 24, "bold"))
        self.titleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.175)

        self.candidateTV = Treeview(self, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings")
        self.candidateTV.column("#1", anchor=CENTER, width=70, stretch=NO)
        self.candidateTV.heading("#1", text="S.NO")
        self.candidateTV.column("#2", anchor=CENTER, width=0, stretch=NO, minwidth=0)
        self.candidateTV.heading("#2", text="ID")
        self.candidateTV.column("#3", anchor=CENTER, width=100)
        self.candidateTV.heading("#3", text="Category")
        self.candidateTV.column("#4", anchor=CENTER, width=100)
        self.candidateTV.heading("#4", text="Candidate Name")
        self.candidateTV.column("#5", anchor=CENTER, width=100)
        self.candidateTV.heading("#5", text="Party Name")
        self.candidateTV.column("#6", anchor=CENTER, width=100)
        self.candidateTV.heading("#6", text="Party Art")
        self.candidateTV.column("#7", anchor=CENTER, width=0)
        self.candidateTV.heading("#7", text="Vote Count")
        self.candidateTV.place(relx=0.05, rely=0.175, relwidth=0.88, relheight=0.675)
        self.candidateTVScrollbar = CTkScrollbar(self, command=self.candidateTV.yview)
        self.candidateTVScrollbar.place(relx=0.93, rely=0.175, relwidth=0.02, relheight=0.675)
        self.candidateTV.configure(yscrollcommand=self.candidateTV.set)

        self.createCandidateBtn = CTkButton(self, text="Create Candidate", font=("Segoe UI", 18), command=self.createCandidateFunc)
        self.createCandidateBtn.place(relx=0.05, rely=0.875, relwidth=0.295, relheight=0.1)

        self.editCandidateBtn = CTkButton(self, text="Edit Candidate", font=("Segoe UI", 18), command=self.editCandidateFunc)
        self.editCandidateBtn.place(relx=0.35, rely=0.875, relwidth=0.295, relheight=0.1)

        self.deleteCandidateBtn = CTkButton(self, text="Delete Candidate", font=("Segoe UI", 18), command=self.deleteCandidateFunc)
        self.deleteCandidateBtn.place(relx=0.65, rely=0.875, relwidth=0.298, relheight=0.1)

        self.updateTV()
    
    def createCandidateFunc(self):
        createCandidateForm = CreateEditCandidateForm(self, self.database, self.updateTV, CTkFrame(self))
        createCandidateForm.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)
    
    def editCandidateFunc(self):
        if len(self.candidateTV.selection()) == 0:
            messagebox.showerror("ElectED - Manage Candidates", "Please select a candidate", parent=self)
            return
        edit = self.candidateTV.item(self.candidateTV.selection()[0], 'values')[1:]
        createCandidateForm = CreateEditCandidateForm(self, self.database, self.updateTV, CTkFrame(self), edit)
        createCandidateForm.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

    def deleteCandidateFunc(self):
        if len(self.candidateTV.selection()) == 0:
            messagebox.showerror("ElectED - Manage Candidates", "Please select a candidate", parent=self)
            return
        if messagebox.askyesno("ElectED - Manage Candidates", "Are you sure you want to delete the candidate?\nThis action is IRREVERSIBLE",parent=self):
            self.database.deleteCandidate(self.candidateTV.item(self.candidateTV.selection()[0], 'values')[1])
            messagebox.showinfo("ElectED - Manage Candidates", f"Candidate {self.candidateTV.item(self.candidateTV.selection()[0], 'values')[3]} deleted successfully", parent=self)
            self.updateTV()

            values = []
            for i in self.database.getCandidates():
                values.append((i[0], i[1], i[2], i[3], i[5]))
            self.updateParentTV(values)

    def onClose(self):
        self.btn.configure(state="normal")
        self.destroy()

    def updateTV(self):
        items = getAllChildren(self.candidateTV)
        for item in items:
            self.candidateTV.delete(item)
        candidates = self.database.getCandidates(hideVotes=False)
        for i in range(len(candidates)):
            self.candidateTV.insert('', 'end', values=(i+1, *candidates[i]))
        
        values = []
        for i in self.database.getCandidates():
            values.append((i[0], i[1], i[2], i[3], i[5]))
        self.updateParentTV(values)

class CreateEditCandidateForm(CTkFrame):
    def __init__(self, parent, database, updateTV, backgroundOverlayFrame, edit=False, *args, **kwargs):
        kwargs["fg_color"] = "#222222"
        kwargs["bg_color"] = "#2A2C2C"
        kwargs["corner_radius"] = 20
        super().__init__(parent, *args, **kwargs)
        self.edit = edit
        self.database = database
        self.updateTV = updateTV
        self.backgroundOverlayFrame = backgroundOverlayFrame
        self.parent = parent
        setOpacity(self.backgroundOverlayFrame, 0.5)
        self.backgroundOverlayFrame.bind("<Button-1>", self.closeForm)
        self.backgroundOverlayFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        createCandidateFormLbl = CTkLabel(self, text="Create Candidate", font=("Segoe UI", 24, "bold"))
        createCandidateFormLbl.place(relx=0.2, rely=0, relwidth=0.6, relheight=0.15)

        categoryLbl = CTkLabel(self, text="Category:", font=("Segoe UI", 18), anchor="w")
        categoryLbl.place(relx=0.1, rely=0.25, relwidth=0.4, relheight=0.075)

        self.categoryDropDownVar = StringVar(master=self, value="Select...")
        categoryDropDown = CTkOptionMenu(self, variable=self.categoryDropDownVar, font=("Segoe UI", 18), values=[x[1] for x in self.database.getCategories()])
        categoryDropDown.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.075)

        cNameLbl = CTkLabel(self, text="Candidate Name:", font=("Segoe UI", 18), anchor="w")
        cNameLbl.place(relx=0.1, rely=0.4, relwidth=0.4, relheight=0.075)

        self.cNameEnt = CTkEntry(self, font=("Segoe UI", 18), placeholder_text="Candidate Name...")
        self.cNameEnt.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.075)

        pNameLbl = CTkLabel(self, text="Party Name:", font=("Segoe UI", 18), anchor="w")
        pNameLbl.place(relx=0.1, rely=0.55, relwidth=0.4, relheight=0.075)

        self.pNameEnt = CTkEntry(self, font=("Segoe UI", 18), placeholder_text="Party Name...")
        self.pNameEnt.place(relx=0.5, rely=0.55, relwidth=0.4, relheight=0.075)

        pArtLbl = CTkLabel(self, text="Party Art:", font=("Segoe UI", 18), anchor="w")
        pArtLbl.place(relx=0.1, rely=0.7, relwidth=0.4, relheight=0.075)

        self.pArtEnt = CTkEntry(self, font=("Segoe UI", 18), placeholder_text="Party Art...")
        self.pArtEnt.bind("<FocusIn>", self.pArtBind)
        self.pArtEnt.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.075)

        self.cancelButton = CTkButton(self, font=("Segoe UI", 18), text="Cancel", command=self.closeForm)
        self.cancelButton.place(relx=0.1, rely=0.85, relwidth=0.375, relheight=0.1)

        self.createButton = CTkButton(self, font=("Segoe UI", 18), text="Create", command=self.createFunc)
        self.createButton.place(relx=0.525, rely=0.85, relwidth=0.4, relheight=0.1)

        if edit != False:
            self.createButton.configure(text="Save")
            createCandidateFormLbl.configure(text="Edit candidate")
            self.categoryDropDownVar.set(edit[1])
            self.cNameEnt.insert(END, edit[2])
            self.pNameEnt.insert(END, edit[3])
            self.pArtEnt.insert(END, edit[4])

    def createFunc(self):
        if self.categoryDropDownVar.get() == "Select...":
            messagebox.showerror("ElectED - Manage Candidates", "Please select a category", parent=self)
            return
        if self.cNameEnt.get() == "":
            messagebox.showerror("ElectED - Manage Candidates", "Please enter candidate name", parent=self)
            return
        if self.pNameEnt.get() == "":
            messagebox.showerror("ElectED - Manage Candidates", "Please enter party name", parent=self)
            return
        if self.pArtEnt.get() == "":
            messagebox.showerror("ElectED - Manage Candidates", "Please select a party image", parent=self)
            return
        if not self.edit:
            self.database.createCandidate(self.categoryDropDownVar.get(), self.cNameEnt.get(), self.pNameEnt.get(), self.pArtEnt.get())
        else:
            self.database.editCandidate(self.edit[0], self.categoryDropDownVar.get(), self.cNameEnt.get(), self.pNameEnt.get(), self.pArtEnt.get(), self.edit[5])
        messagebox.showinfo("ElectED - Manage Candidates", "Created" if not self.edit else "Edited" + " candidate sucessfully", parent=self)
        self.closeForm()
    
    def pArtBind(self, *_):
        self.focus_set()
        img = PartyImageForm(self.parent, self.pArtEnt, CTkFrame(self.parent))

    def closeForm(self, *_):
        self.updateTV()
        self.backgroundOverlayFrame.place_forget()
        self.place_forget()

class PartyImageForm(CTkFrame):
    def __init__(self, parent, pArtEnt, overlayFrame, *args, **kwargs):
        kwargs['corner_radius'] = 30
        super().__init__(parent, *args, **kwargs)
        self.path = None
        self.overlayFrame = overlayFrame
        self.pArtEnt = pArtEnt
        setOpacity(self.overlayFrame, 0.5)
        self.overlayFrame.bind("<Button-1>", self.closeForm)
        self.overlayFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.titleLbl = CTkLabel(self, text="Choose Image", font=("Segoe UI", 24, "bold"))
        self.titleLbl.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.15)

        self.mainFrame = CTkScrollableFrame(self)
        self.mainFrame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.lof = os.listdir("./PartyArt/")
        self.btns = []
        for i in range(len(self.lof)):
            btn = CTkLabel(self.mainFrame, text="", image=CTkImage(None, Img.open(f"./PartyArt/{self.lof[i]}"), (200,200)), corner_radius=20)
            btn.bind("<Button-1>", lambda *_, i=i: self.selectImage(i))
            btn.grid(row=i//2, column=i%2, ipadx=10, ipady=35)
            self.btns.append(btn)
        if self.btns == []:
            noImageLbl = CTkLabel(self, text="There are no images\nPlease put the party art images in the folder \"PartyArt\"", font=("Segoe UI", 16))
            noImageLbl.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.cancelButton = CTkButton(self, text="Cancel", command=self.closeForm, font=("Segoe UI", 18))
        self.cancelButton.place(relx=0.1, rely=0.89, relwidth=0.39, relheight=0.07)

        self.selectButton = CTkButton(self, text="Select", command=self.closeForm, font=("Segoe UI", 18))
        self.selectButton.place(relx=0.51, rely=0.89, relwidth=0.39, relheight=0.07)

        self.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)
    
    def closeForm(self, *_):
        self.overlayFrame.place_forget()
        self.place_forget()
        if self.path == None: return
        self.pArtEnt.delete(0, END)
        self.pArtEnt.insert(0, self.path)
    
    def selectImage(self, i, *_):
        self.path = self.lof[i]
        for x in self.btns:
            x.configure(fg_color="transparent")
        self.btns[i].configure(fg_color="#1f6aa5")

def getAllChildren(tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += getAllChildren(tree, child)
        return children

def setOpacity(widget, value: float):
    widget = widget.winfo_id()
    value = int(255*value)
    wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
    new_exstyle = wnd_exstyle | 0x00080000  
    windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
    windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)
