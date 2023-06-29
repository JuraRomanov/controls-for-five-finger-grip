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
```

в функции **_onOpen_** происходит инцилизация технического зрения при нажатии на кнопку

```python

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
```

Функция **_serialSend_** , которыя вызвается в **_onOpen_** отвечает, за отправку данных на **_serial-port_**

```python
for i, position in enumerate(data):
        ser.write((f"led{i+1}_{'on' if position else 'off'}").encode('utf8'))
        ser.flush()
```

---

## Коментарии к коду для ардуино

Для того чтобы считать данные с **Serial Port** необходимо написать слюдующий код

```arduino
 if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');}
```

---
