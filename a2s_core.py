import time
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import schedule 
import csv
import glob

student_set = set()
path1 = 'student_training_imgs'
path2 = 'faculty_training_imgs'
images = []
classNames = []
slist = os.listdir(path1)
if '.DS_Store' in slist:
    slist.remove('.DS_Store')

flist = os.listdir(path2)
if '.DS_Store' in flist:
    flist.remove('.DS_Store')
    
print(slist)
print(flist)

for cl in slist:
    curImg = cv2.imread(f'{path1}/{cl}')
    images.append(curImg)
    classNames.append('s_'+os.path.splitext(cl)[0])

for cl in flist:
    curImg = cv2.imread(f'{path2}/{cl}')
    images.append(curImg)
    classNames.append('f_'+os.path.splitext(cl)[0])
#print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name, fname):
    if name not in student_set :
        student_set.add(name)
        with open(fname, 'r+') as f:
            m = f.readlines()

            print(student_set)
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            if name.startswith('S_'):
                f.writelines(f'Student,{name[2:].title()},{dtString}\n')

            if name.startswith('F_'):
                f.writelines(f'Faculty,{name[2:].title()},{dtString}\n')


def takeAtt(fname):
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    timeout = time.time() + 10   # 5 minutes from now
    cap = cv2.VideoCapture(0)
    while True:
        if time.time() > timeout:
            break
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                if name.startswith('S_'):
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, name[2:], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                elif name.startswith('F_'):
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name[2:], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                markAttendance(name,fname)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

for filename in glob.glob("attendance*"):
    os.remove(filename)

headers = ["Category","Name","Time"]
now = datetime.now()
p_no = 0

def myatt():
    global p_no 
    p_no = p_no + 1
    now = datetime.now()

    k = "attendance_report.csv" 
    with open(k, "a") as stud:
        student = csv.writer(stud)
        student.writerow('')
        student.writerow(['Period No: '+str(p_no)])
        student.writerow(headers)

    global student_set
    student_set = set()
    
    takeAtt(k)

schedule.every(10).seconds.do(myatt)

while True:
    schedule.run_pending()
    time.sleep(0.1)