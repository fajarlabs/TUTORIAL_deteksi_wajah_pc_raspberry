'''
Developed by fajarlabs
'''

import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import face_recognition
import imutils
import pickle
import cv2
import datetime
import time
import threading
import copy
from cvzone.HandTrackingModule import HandDetector
import numpy as np

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    appendUser = pyqtSignal(str)
    setName = pyqtSignal(str)
    appendAgenda = pyqtSignal(str)

    def run(self):
        # Initialize 'currentname' to trigger only when a new person is identified.
        currentname = "unknown"
        # Determine faces from encodings.pickle file model created from train_model.py
        encodingsP = "encodings.pickle"
        # use this xml file
        cascade = "haarcascade_frontalface_default.xml"

        hand_detector = HandDetector(detectionCon=0.5, maxHands=1)

        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open(encodingsP, "rb").read())
        detector = cv2.CascadeClassifier(cascade)

        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")

        # ################################
        wCam, hCam = 1920, 1080
        # ################################

        cap = cv2.VideoCapture(2)
        cap.set(3, wCam)
        cap.set(4, hCam)

        # used to record the time when we processed last frame
        prev_frame_time = 0

        while True:
            success, img = cap.read()
            #img = cv2.flip(img, 1)
            is_real_face = True
            if success :
                try :
                    imgCopy = copy.deepcopy(img)
                    imgCopy = hand_detector.findHands(imgCopy, draw=True)
                    hand_detector.findPosition(imgCopy)
                    myHandType = hand_detector.handType()
                    if myHandType is not None :
                        is_real_face = False
                except Exception as e :
                    pass

                # font which we will be using to display FPS
                font = cv2.FONT_HERSHEY_SIMPLEX
                # time when we finish processing for this frame
                new_frame_time = time.time()

                # Calculating the fps

                # fps will be number of frame processed in given time frame
                # since their will be most of time error of 0.001 second
                # we will be subtracting it to get more accurate result
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time

                # converting the fps into integer
                fps = int(fps)

                # converting the fps to string so that we can display it on frame
                # by using putText function
                fps = str(fps)

                # putting the FPS count on the frame
                cv2.putText(img, f'{fps}Fps', (7, 70), font, 1, (100, 255, 0), 3, cv2.LINE_AA)

                frame = imutils.resize(img, width=500)

                # convert the input frame from (1) BGR to grayscale (for face
                # detection) and (2) from BGR to RGB (for face recognition)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # detect faces in the grayscale frame
                rects = detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                # OpenCV returns bounding box coordinates in (x, y, w, h) order
                # but we need them in (top, right, bottom, left) order, so we
                # need to do a bit of reordering
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

                # compute the facial embeddings for each face bounding box
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []

                #
                # loop over the facial embeddings
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(data["encodings"], encoding)
                    name = "Unknown"  # if face is not recognized, then print Unknown

                    if is_real_face == False :
                        matches = []

                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                            name = data["names"][i]
                            dt_usr = None
                            if len(entries) > 0 :
                                try :
                                    is_name_is_not_found = False
                                    # check name if exist in any element or temporary database
                                    if not any(d['name'] == name.strip() for d in entries): 
                                        for usr in user_list :
                                            if name.strip() == usr["name"] :
                                                dt_usr = usr
                                                dt_now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                # add to list
                                                entries.append({ "name" : dt_usr['name'], "nik":dt_usr['nik'], "timestamp" : dt_now_str })
                                                self.appendUser.emit(f'{dt_usr["name"]}/{dt_usr["nik"]} : {dt_now_str}')
                                                self.setName.emit(dt_usr["name"])
                                                self.appendAgenda.emit(dt_usr["name"])
                                                break
                                    else :
                                        for ent in entries :
                                            is_found = False
                                            for usr in user_list :
                                                if name.strip() == ent["name"] and name.strip() == usr["name"] :
                                                    idx = next((index for (index, d) in enumerate(entries) if d["name"] == name.strip()), None) # get index of list entriest
                                                    dt_usr = usr
                                                    dt_now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                    dt_now_obj = datetime.datetime.strptime(dt_now_str, "%Y-%m-%d %H:%M:%S")
                                                    dt_last_obj = datetime.datetime.strptime(ent["timestamp"], "%Y-%m-%d %H:%M:%S")
                                                    dt_comp = dt_now_obj - dt_last_obj
                                                    if dt_comp.seconds > 5 :
                                                        entries[idx] = { "name" : dt_usr['name'], "nik":dt_usr['nik'], "timestamp" : dt_now_str }
                                                        self.appendUser.emit(f'{dt_usr["name"]}/{dt_usr["nik"]} : {dt_now_str}')
                                                        self.setName.emit(dt_usr["name"])
                                                        self.appendAgenda.emit(dt_usr["name"])
                                                    break
                                except Exception as e :
                                    print(e)
                            else : # if entries is empty
                                try :
                                    dt_now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    for usr in user_list:
                                        if usr["name"].strip() == name:
                                            dt_usr = usr
                                            break
                                    entries.append({"name": dt_usr['name'], "nik": dt_usr['nik'], "timestamp": dt_now_str})
                                    self.appendUser.emit(f'{dt_usr["name"]}/{dt_usr["nik"]} : {dt_now_str}')
                                    self.setName.emit(dt_usr["name"])
                                except Exception as e :
                                    print(e)

                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)

                        # If someone in your dataset is identified, print their name on the screen
                        if currentname != name:
                            currentname = name

                        self.appendAgenda.emit(name)
                        self.setName.emit(name)

                    # update the list of names
                    names.append(name)

                # loop over the recognized faces
                for ((top, right, bottom, left), name) in zip(boxes, names):
                    # draw the predicted face name on the image - color is in BGR
                    cv2.rectangle(frame, (left, top), (right, bottom),
                                  (0, 255, 225), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                .8, (0, 255, 255), 2)

                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(509, 521 , Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('template.ui', self)
        self.setWindowTitle('Absensi Wajah Menggunakan Webcam')
        self.setFixedSize(743, 440);
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.appendUser.connect(self.appendUser)
        th.setName.connect(self.setName)
        th.appendAgenda.connect(self.appendAgenda)
        th.start()

        tmr = threading.Thread(target=self.runTimer)
        tmr.start()

        # self.pushButton_2.clicked.connect(self.on_click)
        self.show()

    def runTimer(self):
        while True :
            dt_now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.label_timer.setText(dt_now_str)
            time.sleep(1)

    # imagine if you use database
    def search_agenda(self, name):
        event = ""
        if name == 'fajar' :
            event = 'Jam 12:30 ketemu client di depok untuk membahas proyek'
        if name == 'elonmusk':
            event = 'Jam 14:00 Membahas tentang pembayaran bitcoin bersama direktur tesla'
        return event

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def appendAgenda(self, name):

        # dummy data
        # imagine this from the database.
        agenda = ''
        agenda = self.search_agenda(name)

        item = QtGui.QStandardItem(agenda)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listAgenda.clear()
        self.listAgenda.addItem(QListWidgetItem(agenda))
        self.listAgenda.sortItems(order=Qt.DescendingOrder)

    @pyqtSlot(str)
    def appendUser(self, user):
        item = QtGui.QStandardItem(user)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Unchecked)
        if self.listWidget.count() >= 9 :
            self.listWidget.clear()
        self.listWidget.addItem(QListWidgetItem(user))
        self.listWidget.sortItems(order=Qt.DescendingOrder)

    @pyqtSlot(str)
    def setName(self, name):
        self.label_name.setText(name)

if __name__ == "__main__":

    # dummy data
    # imagine this from the database.
    user_list = [
        {"name": "fajar", "nik": "FJR-102378393"},
        {"name": "elonmusk", "nik": "MSK-384992949"},
    ]

    # dummy attendance list
    entries = []

    # imagine this from the database.
    # dt_now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # entries = [{ "name" : 'elonmusk', "nik":'MSK-384992949', "timestamp" : dt_now_str }]

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
