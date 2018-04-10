from populateDatabaseUtils import LogUtil
from populateDatabaseUtils import DynamoDbHelpers
from tkinter import *

class HandleCommands():
    def DeleteTableCalled(self):
        LogUtil.Write("Delete Called")
        DynamoDbHelpers.DeleteTable("project1.school")
        DynamoDbHelpers.DeleteTable("project1.school.transfer.map")

    def PrintAllTableNamesCalled(self):
        LogUtil.Write("PrintAllTableNames Called")
        DynamoDbHelpers.PrintAllTables()

    def CreateTableCalled(self):
        LogUtil.Write("Create Called")
        
        keySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  #Partition key
                }
            ]
        attributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N' #Sort key
                }

            ]
        DynamoDbHelpers.CreateTable('project1.school',keySchema,attributeDefinitions)

        
        keySchema=[
                {
                    'AttributeName': 'school_id',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'course_id',
                    'KeyType': 'RANGE'  #Sort key
                }
            ]
        attributeDefinitions=[
                {
                    'AttributeName': 'school_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'course_id',
                    'AttributeType': 'S'
                }
            ]
        DynamoDbHelpers.CreateTable('project1.school.transfer.map',keySchema,attributeDefinitions)

def createTables():
    LogUtil.Write("CreateTables: started")

def main():
    LogUtil.Write("Main: started")
    # print command line argument
    hndlCommands = HandleCommands()

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            LogUtil.Write(arg)
    else:
        root = Tk()
        app = Application(master=root)
        app.setCallBack(hndlCommands)
        app.mainloop()
        root.destroy()

    LogUtil.Write("Main: end")

class Application(Frame):
    hndlCommands = HandleCommands()

    def setCallBack(self, mainHandleCommands):
        global hndlCommands
        hndlCommands = mainHandleCommands

    def createTablesBtn(self):
        print("createTablesBtn called")
        hndlCommands.CreateTableCalled()

    def printAllTableNamesBtn(self):
        print("printAllTableNamesBtn called")
        hndlCommands.PrintAllTableNamesCalled()

    def deleteTablesBtn(self):
        print("deleteTablesBtn called")
        hndlCommands.DeleteTableCalled()

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["compound"] = "center"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "bottom"})

        self.create_table = Button(self)
        self.create_table["text"] = "Create Tables"
        self.create_table["compound"] = "center"
        self.create_table["command"] = self.createTablesBtn
        self.create_table.pack({"side": "top"})
        
        self.view_table = Button(self)
        self.view_table["text"] = "Print All Table Names"
        self.view_table["compound"] = "center"
        self.view_table["command"] = self.printAllTableNamesBtn
        self.view_table.pack({"side": "top"})
        
        self.delete_table = Button(self)
        self.delete_table["text"] = "Delete Tables"
        self.delete_table["compound"] = "center"
        self.delete_table["command"] = self.deleteTablesBtn
        self.delete_table.pack({"side": "top"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

if __name__ == "__main__":
    main()