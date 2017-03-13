import cv2                                                                      # openCV
import numpy as np                                                              # for numpy arrays
import sqlite3
import dlib

# cap = cv2.VideoCapture('video_for_training.mp4')
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

def insertOrUpdate(Id, Name, roll) :                                            # this function is for database
    connect = sqlite3.connect("Face-DataBase")                                  # connecting to the database
    cmd = "SELECT * FROM Students WHERE ID = " + Id                             # selecting the row of an id into consideration
    cursor = connect.execute(cmd)
    isRecordExist = 0
    for row in cursor:                                                          # checking wheather the id exist or not
        isRecordExist = 1
    if isRecordExist == 1:                                                      # updating name and roll no
        connect.execute("UPDATE Students SET Name = ? WHERE ID = ?",(Name, Id))
        connect.execute("UPDATE Students SET Roll = ? WHERE ID = ?",(roll, Id))
    else:
    	params = (Id, Name, roll)                                               # insering a new student data
    	connect.execute("INSERT INTO Students VALUES(?, ?, ?)", params)
    connect.commit()                                                            # commiting into the database
    connect.close()                                                             # closing the connection

Id = raw_input('Enter user id : ')
name = raw_input("Enter student's name : ")
roll = raw_input("Enter student's roll no. : ")
insertOrUpdate(Id, name, roll)                                                  # calling the sqlite3 database
sampleNum = 0
while(True):
    ret, img = cap.read()                                                       # reading the camera input
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                # Converting to GrayScale
    dets = detector(img, 1)
    for i, d in enumerate(dets):                                                           # loop will run for each face detected
        sampleNum += 1
        cv2.imwrite("./dataset/User."+Id+"."+str(sampleNum)+".jpg",
                    img[d.top():d.bottom(), d.left():d.right()])                # Saving the faces
        cv2.rectangle(img, (d.left(), d.top()),(d.right(), d.bottom()),(0,255,0) ,2) # Forming the rectangle
        cv2.waitKey(200)                                                        # waiting time of 200 milisecond
    cv2.imshow('frame', img)                                                    # showing the video input from camera on window
    cv2.waitKey(1)
    if(sampleNum >= 20):                                                        # will take 20 faces
        break

cap.release()                                                                   # turning the webcam off
cv2.destroyAllWindows()                                                         # Closing all the opened windows