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
        self.db.execute("SELECT * FROM sqlite_master WHERE type='table'")
        if self.db.fetchall() == []:
            self.db.execute("CREATE TABLE Categories(CategoryID INT PRIMARY KEY, CategoryName VARCHAR(20));")
            self.db.execute("CREATE TABLE Candidates(CandidateID INT PRIMARY KEY, Category INT, CandidateName VARCHAR(40), PartyName VARCHAR(40), PartyArt VARCHAR(20), NumVotes INT, FOREIGN KEY(Category) REFERENCES Categories(CategoryID));")
        self.database.commit()

    def createCategory(self, categoryName):
        self.db.execute(f"SELECT MAX(CategoryID) FROM Categories")
        maxCategoryID = self.db.fetchone()[0]
        self.db.execute(f"INSERT INTO Categories VALUES({maxCategoryID+1 if maxCategoryID != None else 1}, '{categoryName}')")
        self.database.commit()
    
    def deleteCategory(self, categoryID):
        self.db.execute(f"DELETE FROM Categories WHERE CateogoryID={categoryID}")
        self.database.commit()
    
    def createCandidate(self, category, candidateName, partyName, partyArt):
        self.db.execute(f"SELECT MAX(CandidateID) FROM Candidates")
        maxCandidateID = self.db.fetchone()[0]
        self.db.execute(f"SELECT CategoryID FROM Categories WHERE CategoryName='{category}'")
        categoryID = self.db.fetchone()[0]
        self.db.execute(f"INSERT INTO Candidates VALUES({maxCandidateID+1 if maxCandidateID != None else 1}, {categoryID}, '{candidateName}', '{partyName}', '{partyArt}', 0)")
        self.database.commit()
    
    def editCandidate(self, candidateID, category, candidateName, partyName, partyArt):
        self.db.execute(f"SELECT CategoryID FROM Categories WHERE CategoryName='{category}'")
        categoryID = self.db.fetchone()[0]
        self.db.execute(f"UPDATE Candidates SET Category={categoryID}, CandidateName='{candidateName}', PartyName='{partyName}', PartyArt='{partyArt} WHERE CandidateID={candidateID}'")
        self.database.commit()

    def deleteCandidate(self, candidateID):
        self.db.execute(f"DELETE FROM Candidates WHERE CandidateID={candidateID}")
        self.database.commit()

    def getCategories(self):
        self.db.execute("SELECT * FROM Categories")
        return self.db.fetchall()

    def getCandidates(self):
        self.db.execute("SELECT CandidateID, CategoryName, CandidateName, PartyName, PartyArt, NumVotes FROM Candidates A, Categories B WHERE A.Category = B.CategoryID")
        return self.db.fetchall()

#TODO: Remove after development
if __name__ == "__main__":
     db = DatabaseHandler()

     db.createCategory("SPL Boy")
     db.createCategory("SPL Girl")
     db.createCategory("ASPL Boy")
     db.createCategory("ASPL Girl")

     db.createCandidate("SPL Boy", "Sri Sai Raj", "Party1", "1.png")
     db.createCandidate("SPL Girl", "Sri a Raj", "Party2", "2.png")
     db.createCandidate("ASPL Boy", "ads Sai Raj", "Party4", "3.png")
     db.createCandidate("ASPL Boy", "ads Sai Raj", "Party67", "4.png")
     db.createCandidate("SPL Boy", "Sri Sai fsf", "Party5", "5.png")

     print(*db.getCategories(), sep="\n")
     print("\n")
     print(*db.getCandidates(), sep="\n")