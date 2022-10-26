import solver
import json
import os

if(__name__ == "__main__"):
    # studentName = input("Enter student name: ")

    # print(studentName)

    studentId = input("Enter student id: ")

    print(studentId)

    data = solver.processCodeOrgData()

    studentId = int(studentId)
    if(studentId in data):
        print(json.dumps(data[studentId]))
    else:
        print('no such id: {}', studentId)
