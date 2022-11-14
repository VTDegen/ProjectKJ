import sys
from os import path

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


#recording
class RecordVideo:
    def __init__(self, camera_port=0):
        self.camera = cv2.VideoCapture(camera_port)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            read, image = self.camera.read()
            # TODO: detect faces now

#face detection
class FaceDetection:
    def __init__(self, haar_cascade_filepath):
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self._min_size = (30, 30)

    def detect_faces(self, image):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=4,flags=cv2.CASCADE_SCALE_IMAGE, min_size=self._min_size)

        # TODO: Paint on a surface and add the faces.

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, image = self.camera.read()
        if read:
            self.image_ready.emit(image)