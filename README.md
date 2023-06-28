# Компьютерное зрение в робототехнике

## Подготовка к работе

---

Перед началом работы нам нужно установить необходимые _библиотеки_

```python
    pip install opencv-python
    pip install cvzone
    pip install mediapipe
    pip install python-math
    pip install pyserial
    pip install pyqtgraph
    pip install PyQt5
```

---

## Создание пользовательского интерфейса

---

Для создания интерфейса мы будем использовать программу [qt Designer](https://build-system.fman.io/qt-designer-download), но вы можете воспользоваться способами,которые будут удобны вам.

В открывшейся программе создаём новое окно.Для этого во вкладке **_File_** жмём на кпопку **_New_** и в окне,которое вспыло , выбираем **_Widget_**

Меняем длину и ширину создонного окна

![](image.png)

Из меню элементов, которое находится слева переносим **_Group Box_** в него помещаем **_Combo Box_** и два **_Puch Button_**
В итоге должно получиться что-то похожее на это

![](https://sun9-38.userapi.com/impg/hfYHDy5Y8v4pGPRAQvD-wxVvvxWxoUAMNc_1Xw/wW-O82GaRY8.jpg?size=438x141&quality=96&sign=5ef14d28b26c4fbaf4ccc16fff46dfba&type=album)

сохраняем проект и закрываем программу

---

## Пишем код для python

---

Импортиуем устоновленные ранее библиотеки

```python
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
```

Загружаем пользовательский интерфейс

```python

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

    if data[0] == 1:
        ser.write(str("led1_on"+'\n').encode('utf8'))
        ser.flush()
    else:
        ser.write(b"led1_off\n")
        ser.flush()

    if data[1] == 1:
        ser.write(b"led2_on\n")
        ser.flush()
    else:
        ser.write(b"led2_off\n")
        ser.flush()
    if data[2] == 1:
        ser.write(b"led3_on\n")
        ser.flush()
    else:
        ser.write(b"led3_off\n")
        ser.flush()
    if data[3] == 1:
        ser.write(b"led4_on\n")
        ser.flush()
    else:
        ser.write(b"led4_off\n")
        ser.flush()
    if data[4] == 1:
        ser.write(b"led5_on\n")
        ser.flush()
    else:
        ser.write(b"led5_off\n")
        ser.flush()

    ser.flush()
    line = ''


def onClose():
    serial1.close()


serial1.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.show()
app.exec()
```

в функции **_onOpen_** происходит инцилизация технического зрения при нажатии на кнопку

```python

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
```

Функция **_serialSend_** , которыя вызвается в **_onOpen_** отвечает, за отправку данных на **_serial-port_**

```python
if data[0] == 1:
    ser.write(str("led1_on"+'\n').encode('utf8'))
    ser.flush()
else:
ser.write(b"led1_off\n")
ser.flush()

if data[1] == 1:
    ser.write(b"led2_on\n")
    ser.flush()
else:
    ser.write(b"led2_off\n")
    ser.flush()
if data[2] == 1:
    ser.write(b"led3_on\n")
    ser.flush()
else:
    ser.write(b"led3_off\n")
    ser.flush()
if data[3] == 1:
    ser.write(b"led4_on\n")
    ser.flush()
else:
    ser.write(b"led4_off\n")
    ser.flush()
if data[4] == 1:
    ser.write(b"led5_on\n")
    ser.flush()
else:
    ser.write(b"led5_off\n")
    ser.flush()

ser.flush()
line = ''
```

---

## Коментарии к коду для ардуино

Для того чтобы считать данные с **Serial Port** необходимо написать слюдующий код

```arduino
 if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');}
```

---
