from tkinter.ttk import Treeview, Style
from tkinter import messagebox, simpledialog
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
        self.parent = parent

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

        self.manageCandidatesBtn = CTkButton(self.quickControlsFrame, text="Manage Candidates", corner_radius=10, font=("Segoe UI", 20))
        self.manageCandidatesBtn.place(relx=0.25375, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.disconnectClientBtn = CTkButton(self.quickControlsFrame, text="Disconnect client", corner_radius=10, font=("Segoe UI", 20), command=self.disconnectClientFunc)
        self.disconnectClientBtn.place(relx=0.5025, rely=0.125, relwidth=0.24375, relheight=0.75)

        self.concludeVotingBtn = CTkButton(self.quickControlsFrame, text="Conclude Voting", corner_radius=10, font=("Segoe UI", 20))
        self.concludeVotingBtn.place(relx=0.75125, rely=0.125, relwidth=0.24375, relheight=0.75)

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
            self.votingInformationTV.insert('', 'end', values=(i[0], i[1], i[2], i[3], i[4]))

    def getAllChildren(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.getAllChildren(tree, child)
        return children
    
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
        mc = ManageCategory(self.manageCategoriesBtn, self.database, self.getAllChildren)
        mc.updateParentTV = self.updateVotingInformationTV
        mc.connectedClientsTV = self.connectedClientsTV
        mc.disconnect = self.disconnectClientFunc

class ManageCategory(CTkToplevel):
    def __init__(self, btn, database, getAllChildren, *args, **kwargs):
        self.btn = btn
        self.database = database
        self.getAllChildren = getAllChildren
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
        categoryName = simpledialog.askstring("ElectED - Manage categories", "Enter new category name", initialvalue=self.categoryTV.item(self.categoryTV.selection()[0], 'values')[1])
        if categoryName == "":
            messagebox.showerror("ElectED - Manage Categories", "Please enter a category name", parent=self)
            return
        self.database.editCategory(self.categoryTV.item(self.categoryTV.selection()[0], 'values')[0], categoryName)
        for i in self.getAllChildren(self.connectedClientsTV):
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
        if messagebox.askyesno("ElectED - Manage Categories", "Are you sure you want to delete the category and the candidates in that category?\nThis action is IRREVERSIBLE"):
            self.database.deleteCategory(self.categoryTV.item(self.categoryTV.selection()[0], 'values')[0])
            for i in self.getAllChildren(self.connectedClientsTV):
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
        items = self.getAllChildren(self.categoryTV)
        for item in items:
            self.categoryTV.delete(item)
        for i in self.database.getCategories():
            self.categoryTV.insert('', 'end', values=i)

if __name__ == "__main__":
    import os
    os.chdir("Server")
    import server