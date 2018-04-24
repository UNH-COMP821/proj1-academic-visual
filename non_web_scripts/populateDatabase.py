from populateDatabaseUtils import LogUtil
from populateDatabaseUtils import DynamoDbHelpers
from tkinter import filedialog, Button, Frame, Tk
import sys
#from tkinter import *
#from tkFileDialog import *
#import Tkinter, Tkconstants, tkFileDialog
import os
import re
import PyPDF2

class HandleCommands():
    nhtiUniversityId =1
    nhtiUniversityName="Concord Community College"
    nhtiDepartmentCisId =1
    nhtiDepartmentCisName ="Computer Information System"
    nhtiDepartmentCsId =2
    nhtiDepartmentCsName ="Computer Science"

    nccUniversityId =2
    nccUniversityName="Nashua Community College"
    nccDepartmentCisId =1
    nccDepartmentCisName ="Computer Information System"
    nccDepartmentSoftDevId =2
    nccDepartmentSoftDevName ="Software Developer"

    mccUniversityId =3
    mccUniversityName="Manchester Community College"
    mccDepartmentCisId =1
    mccDepartmentCisName ="Computer Information System"

    schoolTblName="project1.school"
    schoolTblPe = "#i, #n"
    schoolTblEan = { "#i": "id","#n": "name",}

    schoolDepartmentTblName="project1.school.department"
    schoolDepartmentTblPe = "#i, department_id, #n"
    schoolDepartmentTblEan = { "#i": "school_id","#n": "name",}

    schoolTransferMapTblName="project1.school.transfer.map"
    schoolTransferMapTblPe = "#i, department_id, courses_map"
    schoolTransferMapTblEan = { "#i": "school_id"}

    def PrintAllTableValuesCalled(self):
        LogUtil.Write("PrintAllTableValuesCalled Called")  
        DynamoDbHelpers.FindCoursesForSchool(str(DynamoDbHelpers.nccUniversityId), str(DynamoDbHelpers.nccDepartmentCisId))      
        #DynamoDbHelpers.PrintTableData(self.schoolTblName, self.schoolTblPe, self.schoolTblEan)
        #DynamoDbHelpers.PrintTableData(self.schoolDepartmentTblName, self.schoolDepartmentTblPe, self.schoolDepartmentTblEan)
        #DynamoDbHelpers.PrintTableData(self.schoolTransferMapTblName, self.schoolTransferMapTblPe, self.schoolTransferMapTblEan)

    def loadSchoolDataFromFile(self, filePath, universityId, departmentId, lineStartIndex, lineEndIndex):
        courseMapStr="["
        i = 0
        with open(filePath) as fp:
            for line in fp:
                #print(line)
                i = i+1
                if i > lineStartIndex and i < lineEndIndex:
                    replaceChar = "\xAD"
                    line= line.replace(replaceChar, "-")
                    print("line#>"+str(i) + ", line1>" + line)
                    words2 = re.split(r"\s\s",line)
                    words2 = list(filter(None, words2)) 

                    if len(words2) > 1:
                        classNum=words2[0].strip()
                        
                        classNumList = re.split(" or ",classNum)
                        classNumList = list(filter(None, classNumList))
                        mappingCourseRaw=words2[1].strip()
                        mappingCourseRaw = re.split(" - ",mappingCourseRaw)
                        mappingCourse = mappingCourseRaw[0].strip()
                        
                        classNum=""

                        if len(mappingCourse) < 2:
                            line = fp.readline()
                            i = i+1
                            print("line#>"+str(i) + ", line2>" + line)
                            words2 = re.split(r"\s\s",line)
                            words2 = list(filter(None, words2)) 
                            mappingCourse=words2[0].strip()
                            classNum =  re.split(" - ",classNumList[0])[0].strip()
                            print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'")
                            courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
                        elif len(classNumList) == 1:
                            classNumList =  re.split(" - ",classNumList[0])
                            classNum = classNumList[0].strip()
                            if len(classNumList) > 0:
                                if classNumList[len(classNumList)-1].strip().lower().endswith(" or"):
                                    line = fp.readline()
                                    replaceChar = "\xAD"
                                    line= line.replace(replaceChar, "-")
                                    i = i+1
                                    print("line#>"+str(i) + ", line3>" + line)
                                    words2 = re.split(r"\s\s",line)
                                    words2 = list(filter(None, words2)) 
                                    classNumOrRaw = words2[0].strip()
                                    classNum = classNum +" or " + re.split(" - ",classNumOrRaw)[0].strip()
                                    if len(mappingCourseRaw) > 1:
                                        if mappingCourseRaw[1].lower().endswith(" or"):
                                            mappingCourseRaw2=words2[1].strip()
                                            mappingCourseRaw2 = re.split(" - ",mappingCourseRaw2)
                                            mappingCourse2 = mappingCourseRaw2[0].strip()
                                            mappingCourse = mappingCourse + " or " + mappingCourse2

                            print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'") 
                            courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
                        elif len(classNumList) > 1:
                            classNum=""
                            for classNumOrRaw in classNumList:
                                classNumOr =  re.split(" - ",classNumOrRaw)[0].strip()

                                if len(classNum) > 0:
                                    classNum = classNum + " or "
                                if classNumOrRaw.endswith(" or"):
                                    line = fp.readline()
                                    replaceChar = "\xAD"
                                    line= line.replace(replaceChar, "-")
                                    i = i+1
                                    print("line#>"+str(i) + ", line4>" + line)
                                    words2 = re.split(r"\s\s",line)
                                    words2 = list(filter(None, words2)) 
                                    classNumOrRaw = words2[0].strip()
                                    classNumOr =  re.split(" - ",classNumOrRaw)[0].strip()
                                classNum = classNum + classNumOr                        

                            print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'") 
                            courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
                        elif classNum.endswith(" or"):
                            line = fp.readline()
                            i = i+1
                            print("line#>"+str(i) + ", line5>" + line)
                            print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'")
                            courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)                     
                    else:
                        #classNum=words2[0].strip()
                        print("NOT ENTERED")
                elif i > (lineEndIndex -1):
                    print("@line > " + str(lineEndIndex -1))
                    break
        #fp.close()
        courseMapStr = courseMapStr +"]"
        print("json>"+courseMapStr)
        item={
                'school_id':universityId,
                'department_id':departmentId,
                'courses_map':courseMapStr,
            }
        DynamoDbHelpers.InsertData(self.schoolTransferMapTblName, item)


    def loadMccCis(self, filePath, universityId, departmentId):
        courseMapStr="["
        fp = open(filePath)
        for i, line in enumerate(fp):
            #print(line)
            if i > 9 and i < 31:
                print(line)
                replaceChar = "\xAD"
                line= line.replace(replaceChar, "-")
                #line = re.sub(r"\w(-)\w", "*", line)
                
                #print(line)
                pattern = " - "
                words2 = re.split(pattern,line)
                classNum=""
                mappingCourse=""
                #print(">>"+str(len(words2)))
                if len(words2) > 1:
                    classNum = words2[0].strip()
                    mapCourseIndex = len(words2)-2
                    if mapCourseIndex < 1:
                        mapCourseIndex = 1
                    mappingCourse = words2[mapCourseIndex].strip()    
                    foundIndex= mappingCourse.find("  ")
                    mappingCoursePre= mappingCourse[:foundIndex].strip()
                    mappingCourse= mappingCourse[foundIndex:].strip()
                    print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'")                
                    courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
                                   
                    if mappingCoursePre.endswith("or"):
                        line = fp.readline()
                        line= line.replace(replaceChar, "-")
                        print("next:" + line)
                        words2 = re.split(pattern,line)
                        classNum = words2[0].strip()
                        print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'")                
                        courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
                else:
                    print("match?" + words2[0])
                    words2[0] = words2[0].strip()
                    foundIndex= words2[0].find("  ")
                    classNum= words2[0][:foundIndex].strip()
                    mappingCourse= words2[0][foundIndex:].strip()
                    print("classNum-mappingCourse='" + classNum+"', '"+mappingCourse+"'")                    
                    courseMapStr = self.appendCourses(courseMapStr, classNum, mappingCourse)
            elif i > 30:
                print("@line > 31")
                break
        fp.close()
        courseMapStr = courseMapStr +"]"
        print("json>"+courseMapStr)
        item={
                'school_id':universityId,
                'department_id':departmentId,
                'courses_map':courseMapStr,
            }
        DynamoDbHelpers.InsertData(self.schoolTransferMapTblName, item)

    def appendCourses(self,courseMapStr,classNum,mappingCourse):
        if len(courseMapStr) > 1:
            courseMapStr = courseMapStr + ","
        courseMapStr = courseMapStr + "{" + "\"course\":\"" + classNum +"\",\"unh_map\":\""+mappingCourse+"\"}"
        return courseMapStr

    def LoadMccFileCalled(self, fileDir):
        LogUtil.Write("LoadMccFileCalled Called")
        LogUtil.Write("fileDir:" + fileDir)
        
        #1) delete all university data
        #2) load basic university data
        #2) load department from  

        self.clearAllTables()
        self.populateInitialDbValues()

        for file in os.listdir(fileDir):
            if file.endswith(".txt"):
                print(os.path.join(fileDir, file))
                filePath = os.path.join(fileDir, file)
                print(file)
                if str(file) == "mcc_cis_pathways.txt":
                    print("found mcc_cis_pathways.txt")
                    ##self.loadMccCis(filePath, self.mccUniversityId, self.mccDepartmentCisId)
                    self.loadSchoolDataFromFile(filePath, self.mccUniversityId, self.mccDepartmentCisId, 10, 33)
                elif str(file) == "ncc_comp_net_cis_pathways.txt":
                    print("found ncc_comp_net_cis_pathways.txt")
                    self.loadSchoolDataFromFile(filePath, self.nccUniversityId, self.nccDepartmentCisId, 10, 33)
                elif str(file) == "ncc_software_dev_cis_pathways.txt":
                    print("found ncc_software_dev_cis_pathways.txt")
                    self.loadSchoolDataFromFile(filePath, self.nccUniversityId, self.nccDepartmentSoftDevId, 10, 36)
                elif str(file) == "nhti_cis_pathways.txt":
                    print("found nhti_cis_pathways.txt")
                    self.loadSchoolDataFromFile(filePath, self.nhtiUniversityId, self.nhtiDepartmentCisId, 15, 41)
                elif str(file) == "nhti_cs_pathways.txt":
                    print("found nhti_cs_pathways.txt")
                    self.loadSchoolDataFromFile(filePath, self.nhtiUniversityId, self.nhtiDepartmentCsId, 15, 41)
                else:                    
                    print("unknown file>" + file)

    def clearAllTables(self):
        pe ="#i"
        # Expression Attribute Names for Projection Expression only.
        ean = { "#i": "id",}
        DynamoDbHelpers.ClearTable(self.schoolTblName,pe, ean, "id")
        
        pe ="#sid,department_id"
        ean = { "#sid": "school_id",}
        DynamoDbHelpers.ClearTable(self.schoolTransferMapTblName,pe, ean, "school_id","department_id")
        
        pe ="#sid,department_id"
        ean = { "#sid": "school_id",}
        DynamoDbHelpers.ClearTable(self.schoolDepartmentTblName,pe, ean, "school_id","department_id")
        
        pe ="#sid,department_id"
        ean = { "#sid": "school_id",}
        DynamoDbHelpers.ClearTable(self.schoolTransferMapTblName,pe, ean, "school_id","department_id")

    def populateInitialDbValues(self):
        print("begin populateInitialDbValues")
        self.initialLoadNhti()
        self.initialLoadNcc()
        self.initialLoadMcc()
        print("End populateInitialDbValues")

    def initialLoadNhti(self):        
        item={
            'id':self.nhtiUniversityId,
            'name':self.nhtiUniversityName,
        }
        DynamoDbHelpers.InsertData(self.schoolTblName, item)

        item={
            'school_id':self.nhtiUniversityId,
            'department_id':self.nhtiDepartmentCisId,
            'name':self.nhtiDepartmentCisName,
        }
        DynamoDbHelpers.InsertData(self.schoolDepartmentTblName, item)

        item={
            'school_id':self.nhtiUniversityId,
            'department_id':self.nhtiDepartmentCsId,
            'name':self.nhtiDepartmentCsName,
        }
        DynamoDbHelpers.InsertData(self.schoolDepartmentTblName, item)


    def initialLoadNcc(self):        
        item={
            'id':self.nccUniversityId,
            'name':self.nccUniversityName,
        }
        DynamoDbHelpers.InsertData(self.schoolTblName, item)
              
        item={
            'school_id':self.nccUniversityId,
            'department_id':self.nccDepartmentCisId,
            'name':self.nccDepartmentCisName,
        }
        DynamoDbHelpers.InsertData(self.schoolDepartmentTblName, item)
        item={
            'school_id':self.nccUniversityId,
            'department_id':self.nccDepartmentSoftDevId,
            'name':self.nccDepartmentSoftDevName,
        }
        DynamoDbHelpers.InsertData(self.schoolDepartmentTblName, item)
    
    def initialLoadMcc(self):
        item={
                'id':self.mccUniversityId,
                'name':self.mccUniversityName,
            }
        DynamoDbHelpers.InsertData(self.schoolTblName, item)

        item={
            'school_id':self.mccUniversityId,
            'department_id':self.mccDepartmentCisId,
            'name':self.mccDepartmentCisName,
        }
        DynamoDbHelpers.InsertData(self.schoolDepartmentTblName, item)

    def loadInitialUniversityValues(self):
        print("End loadInitialUniversityValues")

    def InsertDataCalled(self):
        LogUtil.Write("Insert Called")
        self.initialLoadNhti()
        self.initialLoadMcc()
        self.initialLoadNcc()

    def DeleteTableCalled(self):
        LogUtil.Write("Delete Called")
        DynamoDbHelpers.DeleteTable("project1.school")
        DynamoDbHelpers.DeleteTable("project1.school.transfer.map")
        DynamoDbHelpers.DeleteTable("project1.school.department")

    def PrintAllTableNamesCalled(self):
        LogUtil.Write("PrintAllTableNames Called")
        DynamoDbHelpers.PrintAllTables()

    def ClearAllTableCalled(self):
        LogUtil.Write("ClearAllTableCalled Called")
        self.clearAllTables()

    def CreateTableCalled(self):
        LogUtil.Write("Create Called")

        # create project1.school
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


        # create project1.school.department
        keySchema=[
                {
                    'AttributeName': 'school_id',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'department_id',
                    'KeyType': 'RANGE'  #Sort key
                }
            ]
        attributeDefinitions=[
                {
                    'AttributeName': 'school_id',
                    'AttributeType': 'N' 
                },
                {
                    'AttributeName': 'department_id',
                    'AttributeType': 'N' 
                }
            ]
        DynamoDbHelpers.CreateTable('project1.school.department',keySchema,attributeDefinitions)
        
        # create project1.school.transfer.map
        keySchema=[
                {
                    'AttributeName': 'school_id',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'department_id',
                    'KeyType': 'RANGE'  #Sort key
                }
            ]
        attributeDefinitions=[
                {
                    'AttributeName': 'school_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'department_id',
                    'AttributeType': 'N'
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

    def clearAllTableBtn(self):
        print("clearAllTableBtn called")
        hndlCommands.ClearAllTableCalled()


    def printAllTableValuesBtn(self):
        print("printAllTableValuesBtn called")
        hndlCommands.PrintAllTableValuesCalled()

    def LoadMccFileBtn(self):
        print("LoadMccFileBtn called")
        fileDirectory = filedialog.askdirectory()
        hndlCommands.LoadMccFileCalled(fileDirectory)
        
    def deleteTablesBtn(self):
        print("deleteTablesBtn called")
        hndlCommands.DeleteTableCalled()
    
    def insertDataBtn(self):
        print("insertDataBtn called")
        hndlCommands.InsertDataCalled()

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

        self.clear_table = Button(self)
        self.clear_table["text"] = "Clear all values in Tables"
        self.clear_table["compound"] = "center"
        self.clear_table["command"] = self.clearAllTableBtn
        self.clear_table.pack({"side": "top"})
        
        self.delete_table = Button(self)
        self.delete_table["text"] = "Delete Tables"
        self.delete_table["compound"] = "center"
        self.delete_table["command"] = self.deleteTablesBtn
        self.delete_table.pack({"side": "top"})

        self.insertdata = Button(self)
        self.insertdata["text"] = "insert dummy data"
        self.insertdata["compound"] = "center"
        self.insertdata["command"] = self.insertDataBtn
        self.insertdata.pack({"side": "top"})

        self.dumpData = Button(self)
        self.dumpData["text"] = "print table values"
        self.dumpData["compound"] = "center"
        self.dumpData["command"] = self.printAllTableValuesBtn
        self.dumpData.pack({"side": "top"})

        
        self.loadMcc = Button(self)
        self.loadMcc["text"] = "Load Mcc data from directory"
        self.loadMcc["compound"] = "center"
        self.loadMcc["command"] = self.LoadMccFileBtn
        self.loadMcc.pack({"side": "top"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

if __name__ == "__main__":
    main()