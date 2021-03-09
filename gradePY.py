from xmljson import badgerfish, XMLData
from urllib.parse import urlparse
from studentvue import StudentVue
from tabulate import tabulate
from getpass import getpass
from lxml import etree
import json
import time
import os

def studentInfo():
    info = student.get_student_info()['StudentInfo']
    print("Student name:",info["FormattedName"]["$"])
    print("Student ID:",info["PermID"]["$"])
    print("Current School:",str(info["CurrentSchool"]["$"]))
    print("Gender:",info["Gender"]["$"])
    print("Grade:",str(info["Grade"]["$"]))
    print("Date of Birth:",str(info["BirthDate"]["$"]))

def absences():
    print("Absences:\n")
    absences = student.get_attendance()["Attendance"]["Absences"]["Absence"]
    for absence in absences[::-1]:
        print("Date:",absence["@AbsenceDate"])
        classes = []
        if isinstance(absence["Periods"]["Period"], list):
            for period in absence["Periods"]["Period"]:
                if period["@Name"] != "":
                    classes.append(period["@Course"]+": "+period["@Staff"])
        else:
            temp = absence["Periods"]["Period"]
            classes.append(temp["@Course"]+": "+temp["@Staff"])
        
        
        if len(classes) > 1:
            print("Classes: ")
        else:
            print("Class:")
        for i in classes:
            print(i)
        print("")

def mail():
    print(json.dumps(student.get_messages()))

def reportCard():
    #print(json.dumps(student.list_report_cards()))
    #print(json.dumps(student.get_report_card("6F654710-E236-4DFE-878D-65D693428A19")))
    print(json.dumps(student._xml_json_serialize(student._make_service_request('PXP.GradesData'))))

def gradeOverview():

    grades = student.get_gradebook()["Gradebook"]["Courses"]["Course"]

    print("Classes:\n")
    for course in grades:
        print(str(course["@Period"])+". "+course["@Title"]+": "+bold(str(course["Marks"]["Mark"]["@CalculatedScoreRaw"])+"("+str(course["Marks"]["Mark"]["@CalculatedScoreString"])+")"))

def individualGrades():
    grades = student.get_gradebook()["Gradebook"]["Courses"]["Course"][temp-1]
    print("Individual grades for "+grades["@Title"]+":")
    print("\nWeighted Averages:\n")
    for weight in grades["Marks"]["Mark"]["GradeCalculationSummary"]["AssignmentGradeCalc"]:
        print(weight["@Type"]+": "+weight["@Weight"]+" - "+bold(str(weight["@WeightedPct"])))
    print("")
    headers = [bold("Assignment"),bold("Weight"),bold("Score"),bold("Date")]
    gradeList = []
    for assignment in grades["Marks"]["Mark"]["Assignments"]["Assignment"]:
        content = [assignment["@Measure"],assignment["@Type"],assignment["@Score"],assignment["@Date"]]
        if assignment["@Measure"] == "TOTAL":
            content[2] = underline(content[2])
        gradeList.append(content)
    print(tabulate(gradeList, headers=headers))

def bold(word):
    return("\033[1m" + word + "\033[0m")

def underline(word):
    return("\033[4" + word + "\033[0m")


while True:
    username = input("Enter username: ")
    #password = input("Enter password: ")
    password = getpass("Enter password(hidden): ")
    student = StudentVue(username,password,"md-mcps-psv.edupoint.com")
    try:
        temp = student.get_attendance()["RT_ERROR"]["@ERROR_MESSAGE"]
        print("Invalid username or password. \n")
        time.sleep(1)
        os.system("cls")
    except:
        break
    
os.system("cls") 
name = student.get_student_info()['StudentInfo']["NickName"]["$"]
print("Welcome",name+"!")
grades = student.get_gradebook(2)

while True:
    os.system("cls")
    print("1. Student Info")
    print("2. Absences")
    print("3. Gradebook")
    print("4. Synergy Mail")
    print("5. Report Card")
    print("6. Refresh Data")

    try:
        print("")
        temp = int(input())
        if temp < 1 or temp > 6:
            print("\n")
            print("Invalid input. Please try again.")
            time.sleep(1)
            os.system("cls")
            continue
    except:
        print("\n")
        print("Invalid input. Please try again.")
        time.sleep(1)
        os.system("cls")
        continue
    if temp == 1:
        os.system("cls")
        studentInfo()
        temp = input("\nPress enter to return to the menu: ")
    elif temp == 2:
        os.system("cls") 
        absences()
        temp = input("\nPress enter to return to the menu: ")
    elif temp == 3:
        while True:
            os.system("cls") 
            gradeOverview()
            temp = input("\nSelect period to view individual grades for, or press enter to go back: ")
            if temp == "":
                break
            try:
                temp = int(temp)
            except:
                print("\n")
                print("Invalid input. Please try again.")
                time.sleep(1)
                os.system("cls")
                continue
            if temp < 1 or temp > len(student.get_gradebook()["Gradebook"]["Courses"]["Course"]):
                print("\n")
                print("Invalid input. Please try again.")
                time.sleep(1)
                os.system("cls")
                continue
            os.system("cls") 
            individualGrades()
            temp = input("\nPress enter to return to the grade overview: ")
                
    elif temp == 4:
        os.system("cls")
        temp = input("Due to API limitations, currently only the subject line and some other information can be displayed. Press enter to continue: ")
        os.system("cls")
        mail()
        temp = input("\nPress enter to return to the menu: ")
    elif temp == 5:
        os.system("cls") 
        reportCard()
        temp = input("\nPress enter to return to the menu: ")
    elif temp == 6:
        os.system("cls") 
        print("Refreshing...")
        student = StudentVue(username,password,"md-mcps-psv.edupoint.com")
        

  
#for i in range(len(grades["Gradebook"]["Courses"]["Course"])):
#    print(grades["Gradebook"]["Courses"]["Course"][i]["@Title"])


