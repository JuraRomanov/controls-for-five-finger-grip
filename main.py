
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

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("SerialGUI")

serial1 = QSerialPort()
serial1.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)

posX = 200
posY = 100
listX = []
for x in range(100):
    listX.append(x)
listY = []
for x in range(100):
    listY.append(0)


def onRead():
    if not serial1.canReadLine():
        return     # выходим если нечего читать
    rx = serial1.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    if data[0] == '0':
        ui.lcdN.display(data[1])
        ui.tempB.setValue(int(float(data[3]) * 10))
        ui.tempL.setText(data[3])
        global listX
        global listY
        listY = listY[1:]
        listY.append(int(data[2]))
        ui.graph.clear()
        ui.graph.plot(listX, listY)

    if data[0] == '1':
        if data[1] == '0':
            ui.circle.setChecked(True)
        else:
            ui.circle.setChecked(False)

    if data[0] == '2':
        global posX
        global posY
        posX += int((int(data[1]) - 512) / 100)
        posY += int((int(data[2]) - 512) / 100)
        ui.circle.setGeometry(posX, posY, 20, 20)


def onOpen():
    global ser
    ser = serial.Serial(str(ui.comL.currentText()), 9600, timeout=1)
    cap = cv2.VideoCapture(0)  # основаня камера
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]
            fingers1 = detector.fingersUp(hand1)
            serialSend(fingers1)

        cv2.imshow("Image", img)
        if cv2.waitKey(40) == 27:
            break


def serialSend(data):

    for i, position in enumerate(data):
        ser.write((f"led{i+1}_{'on' if position else 'off'}").encode('utf8'))
        ser.flush()


def onClose():
    serial1.close()


serial1.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.show()
app.exec()
