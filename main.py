# coding: utf8
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import cv2
import mediapipe as mp
import math
import serial
from serial import Serial
from cvzone.HandTrackingModule import HandDetector


class User_Preference:

    def __init__(self):

        self.QSerial = QSerialPort()
        pass

    def setComPort(self, ui):
        self.ser = serial.Serial(str(ui.comL.currentText()), 9600, timeout=1)

    def getComPort(self):
        return self.ser

    def setCap(self):
        self.cap = cv2.VideoCapture(0)

    def setReadCap(self, Read):
        self.isRead = Read

    def getReadCap(self):
        return self.isRead


def onOpen(ui, Preference):
    Preference.setComPort(ui)
    Preference.setCap()
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    Preference.setReadCap(True)

    while Preference.getReadCap():
        success, img = Preference.cap.read()
        hands, img = detector.findHands(img)
        if hands:
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            serialSend(fingers1, Preference.getComPort())

        cv2.imshow("Image", img)
        if cv2.waitKey(40) == 27:
            onClose(Preference)
            break


def serialSend(data, ser):
    for i, position in enumerate(data):
        ser.write((f"led{i+1}_{'on' if position else 'off'}").encode('utf8'))
        ser.flush()


def onClose(Preference):
    Preference.setReadCap(False)
    cv2.destroyAllWindows()


def initialization_ui(Preference):

    Preference.QSerial.setBaudRate(115200)
    portList = [port.portName() for port in QSerialPortInfo().availablePorts()]

    app = QtWidgets.QApplication([])
    ui = uic.loadUi("design.ui")
    ui.setWindowTitle("SerialGUI")
    ui.comL.addItems(portList)

    ui.openB.clicked.connect(lambda: onOpen(ui, Preference))
    ui.closeB.clicked.connect(lambda: onClose(Preference))
    ui.show()
    app.exec()
    pass


if __name__ == "__main__":

    Preference = User_Preference()
    initialization_ui(Preference)
