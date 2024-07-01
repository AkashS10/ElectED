import sqlite3

# Database Structure
# TABLE: Categories
# CategoryID INT PRIMARY KEY
# CategoryName VARCHAR
#
# TABLE: Candidates
# CandidateID INT PRIMARY KEY
# Category FORIGEN KEY Cateogries.CategoryID
# CandidateName VARCHAR
# PartyName VARCHAR
# PartyArt VARCHAR (stores the image name of the party's art present in Server/PartyArt/imageName.jpg)
# NumVotes INT

class DatabaseHandler:
    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.db = self.database.cursor()
        self.initalizeDatabase()

    def initalizeDatabase(self):
        self.db.execute("SELECT * FROM sqlite_master WHERE type='table'")
        if self.db.fetchall() == []:
            self.db.execute("CREATE TABLE Categories(CategoryID INT PRIMARY KEY, CategoryName VARCHAR(20));")
            self.db.execute("CREATE TABLE Candidates(CandidateID INT PRIMARY KEY, FOREIGN KEY(Category) REFERENCES Categories(CategoryID), CandidateName VARCHAR(40), PartyName VARCHAR(40), PartyArt VARCHAR(20), NumVotes INT);")