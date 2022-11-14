# Modified by Augmented Startups & Geeky Bee
# October 2020
# Facial Recognition Attendence GUI
# Full Course - https://augmentedstartups.info/yolov4release
# *-
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.uic import loadUi
# from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
# from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication,QFileDialog
# from PyQt5 import QtWidgets
# # from os.path import dirname, join
# import cv2
# import face_recognition
# import numpy as np
# import datetime
# import os
# import csv
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication,QFileDialog
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv

":UI Initialization"
class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        now = QDate.currentDate()
        curdate = now.toString('ddd dd MMMM yyyy')
        curtime = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_label.setText(curdate)
        self.Time_label.setText(curtime)

        self.image = None
        self._new_window = None
        self.viewbtn.clicked.connect(self.viewfun)
        self.Capture.clicked.connect(self.picap)


        img_counter = 0
        nameimg = 0


    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """

        self.capture = cv2.VideoCapture(0)

        #self.mental = self.capture.close()


        # while True:
            #ret, frame = self.capture.read()
            # print("hey")

            # if k%256 == 32:
            #     img_name = "Profile_Image_{}.png".format(img_counter)
            #
            #     #capture fn
            #     cv2.imwrite(img_name, frame)

        # if len(camera_name) == 1:
        # 	self.capture = cv2.VideoCapture(int(camera_name))
        # else:
        # 	self.capture = cv2.VideoCapture(camera_name)


        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'


        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        # print(attendance_list)
        """
        Opening File
        """
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(400)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # csv
        def mark_attendance(name):
            """
            :param name: detected face known or unknown one
            :return:
            """
            if self.ClockInButton.isChecked():
                self.ClockInButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'Unknown'):
                            buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking In?',
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:

                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string},Clock In')
                                self.ClockInButton.setChecked(False)

                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Student')
                                self.HoursLabel.setText('Arrived')
                                self.MinLabel.setText('')

                                # self.CalculateElapse(name)
                                # print('Yes clicked and detected')
                                self.Time1 = datetime.datetime.now()
                                # print(self.Time1)
                                self.ClockInButton.setEnabled(True)
                            else:
                                print('Not clicked.')
                                self.ClockInButton.setEnabled(True)

            elif self.ClockOutButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'Unknown'):
                            buttonReply = QMessageBox.question(self, 'Cheers ' + name,'Are you Clocking Out?',QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string},Clock Out')
                                self.ClockOutButton.setChecked(False)

                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Student')
                                self.Time2 = datetime.datetime.now()
                                # print(self.Time2)

                                self.ElapseList(name)
                                self.TimeList2.append(datetime.datetime.now())
                                CheckInTime = self.TimeList1[-1]
                                CheckOutTime = self.TimeList2[-1]
                                self.ElapseHours = (CheckOutTime - CheckInTime)
                                self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60) % 60) + ' m')
                                self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60 ** 2)) + ' h')
                                self.ClockOutButton.setEnabled(True)
                            else:
                                print('Not clicked.')
                                self.ClockOutButton.setEnabled(True)

        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "Unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            mark_attendance(name)

        return frame

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def ElapseList(self, name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':
                            if row[0] == name:
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out':
                            if row[0] == name:
                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

    def profun (self):
        print("Capturing Process")
        self._new_window1 = Ui_ProfileDialog()
        self._new_window1.show()
        print("Showing")

    def viewfun (self):
        print("Opening")
        self._new_window = Ui_AttendanceDialog()
        self._new_window.show()
        print("Showing")

    def picap (self):
        print("Captured Image")
        msgbox = QMessageBox.question(self, 'Hey','Do you want to Create a new Profile', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msgbox == QMessageBox.Yes:
            nameimg = 0
            self.profun()
            print("Yes")
        else:
            print("No")

class Ui_AttendanceDialog(QDialog):
    def __init__(self):
        super(Ui_AttendanceDialog, self).__init__()
        loadUi("./attendwindow.ui", self)


class Ui_ProfileDialog(QDialog):
    def __init__(self):
        super(Ui_ProfileDialog, self).__init__()
        loadUi("./profilewindow.ui", self)