import sys
import cv2
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *

class ProWindow(QDialog):
    def __init__(self):
        super(ProWindow, self).__init__()
        loadUi('profilewindow.ui', self)
        self.image=None
        self.start.clicked.connect(self.start_webcam)
        self.stop.clicked.connect(self.stop_webcam)

    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, self.image=self.capture.read()
        self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)

    def stop_webcam(self):
        self.capture.imwrite("b.png".format(1),self.capture)

    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img, img.shape[1],img.shape[0],img.strides[0], qformat)
        outImage=outImage.rgbSwapped()

        if window==1:
            self.kjLabel.setPixmap(QPixmap.fromImage(outImage))
            self.kjLabel.setScaledContents(True)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=ProWindow()
    window.setWindowTitle('Profile Creation')
    window.show()
    sys.exit(app.exec_())