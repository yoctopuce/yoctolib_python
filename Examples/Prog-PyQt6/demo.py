#!/usr/bin/python
# ********************************************************************
#
#  Example PyQt6 GUI application using Yoctopuce devices
#
#  This code shows how to properly use a separate thread
#  for running possibly blocking I/O operations
#
#  For more details, read
#  https://www.yoctopuce.com/EN/article/creating-a-yoctopuce-application-with-pyqt
#
# *********************************************************************
# -*- coding: utf-8 -*-
import os, sys,time

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_anbutton import *
from yocto_relay import YRelay

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject, QThread, QTimer

# Starting with PyQt v5.5, unhandled Python exception result in a call
# to Qt’s qFatal() function, which will cause your application to stop
# without any explanation in an IDE like PyCharm, and prevent debugging.
# The lines below restore the previous behaviour
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
sys.excepthook = except_hook

# Helper to get the unique identifier of current thread
def currThread():
    return '[thread-' + str(int(QThread.currentThreadId())) + ']'

class YoctopuceTask(QObject):

    startTask = pyqtSignal()            # in: start the task
    stopTask = pyqtSignal()             # in: stop the task
    toggleRelay = pyqtSignal(str)       # in: toggle a relay
    statusMsg = pyqtSignal(str)         # out: publish the task status
    arrival = pyqtSignal(dict)          # out: publish a new device arrival
    newValue = pyqtSignal(str,str)      # out: publish a new function value
    removal = pyqtSignal(dict)          # out: publish a device disconnect

    def __init__(self):
        super(YoctopuceTask, self).__init__()
        # connect incoming signals
        self.startTask.connect(self.initAPI)
        self.toggleRelay.connect(self.toggleIt)
        self.stopTask.connect(self.freeAPI)

    @pyqtSlot()
    def initAPI(self):
        print('Yoctopuce task started', currThread())
        errmsg = YRefParam()
        YAPI.RegisterLogFunction(self.logfun)
        # Setup the API to use Yoctopuce devices on localhost
        if YAPI.RegisterHub('127.0.0.1', errmsg) != YAPI.SUCCESS:
            self.statusMsg.emit('Failed to init Yoctopuce API: ' +
                                errmsg.value)
            return
        YAPI.RegisterDeviceArrivalCallback(self.deviceArrival)
        YAPI.RegisterDeviceRemovalCallback(self.deviceRemoval)
        self.statusMsg.emit('Yoctopuce task ready')
        # prepare to scan Yoctopuce events periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleEvents)
        self.checkDevices = 0
        self.timer.start(50)

    @pyqtSlot()
    def freeAPI(self):
        self.timer.stop()
        YAPI.FreeAPI()
        self.statusMsg.emit('Yoctopuce task stopped')

    @pyqtSlot()
    def handleEvents(self):
        if self.checkDevices <= 0:
            YAPI.UpdateDeviceList()
            self.checkDevices = 10
        else:
            self.checkDevices -= 1
        YAPI.HandleEvents()

    @pyqtSlot(str)
    def toggleIt(self, relayName):
        print("Toggle "+relayName, currThread())
        relay = YRelay.FindRelay(relayName)
        if relay.isOnline():
            relay.toggle()
        else:
            self.statusMsg.emit('Relay "' + relayName + '" is not online')

    def deviceArrival(self, m: YModule):
        serialNumber = m.get_serialNumber()
        # build a description of the device as a dictionnary
        device = { 'serial': serialNumber, 'functions': {} }
        fctcount = m.functionCount()
        for i in range(fctcount):
            device['functions'][m.functionId(i)] = m.functionType(i)
        m.set_userData(device)
        # pass it to the UI thread via the arrival signal
        self.arrival.emit(device)
        # make sure to get notified about each new value
        for functionId in device['functions']:
            bt = YFunction.FindFunction(serialNumber + '.' + functionId)
            bt.registerValueCallback(self.functionValueChangeCallback)

    def functionValueChangeCallback(self, fct: YFunction, value: str):
        hardwareId = fct.get_hardwareId()
        self.newValue.emit(hardwareId, value)

    def deviceRemoval(self, m: YModule):
        # pass the disconnect to the UI thread via the removal signal
        self.removal.emit(m.get_userData())

    def logfun(self, line: str):
        msg = line.rstrip()
        print("API Log: " + msg, currThread())
        # show low-level API logs as status
        self.statusMsg.emit(msg)

class SensorDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.refreshCount = 0
        self.setWindowTitle('Sample PyQT6 application')
        self.message = QLabel(self)
        self.message.setStyleSheet("background: white")
        self.functionValues = {}
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.show()
        print("MainWindow created", currThread())

    def startIO(self):
        # Start Yoctopuce I/O task in a separate thread
        self.yoctoThread = QThread()
        self.yoctoThread.start()
        self.yoctoTask = YoctopuceTask()
        self.yoctoTask.moveToThread(self.yoctoThread)
        self.yoctoTask.statusMsg.connect(self.showMsg)
        self.yoctoTask.arrival.connect(self.arrival)
        self.yoctoTask.newValue.connect(self.newValue)
        self.yoctoTask.removal.connect(self.removal)
        self.yoctoTask.startTask.emit()

    @pyqtSlot(str)
    def showMsg(self, str):
        self.message.setText(str)

    @pyqtSlot(dict)
    def arrival(self, device):
        # log arrival
        print('Device connected:', device, currThread())
        # for relay functions, create a toggle button
        for functionId in device['functions']:
            if device['functions'][functionId] == 'Relay':
                hardwareId = device['serial'] + '.' + functionId
                newButton = QPushButton('toggle '+hardwareId)
                newButton.clicked.connect(
                    lambda checked,hwid=hardwareId:
                        self.toggleRelayPressed(hwid)
                )
                self.layout.addWidget(newButton)

    @pyqtSlot(str,str)
    def newValue(self, hardwareId, value):
        if hardwareId not in self.functionValues:
            # create a new label when first value arrives
            newLabel = QLabel(self)
            self.layout.addWidget(newLabel)
            self.functionValues[hardwareId] = newLabel
        # then update it for each reported value
        self.functionValues[hardwareId].setText(hardwareId + ": " + value)

    @pyqtSlot(QPushButton)
    def toggleRelayPressed(self, hardwareId):
        print('toggleRelayPressed:', hardwareId, currThread())
        self.yoctoTask.toggleRelay.emit(hardwareId)

    @pyqtSlot(dict)
    def removal(self, device):
        # log arrival
        print('Device disconnected:', device, currThread())
        # mark all reported values as disconnected
        for functionId in device['functions']:
            hardwareId = device['serial'] + '.' + functionId
            if hardwareId in self.functionValues:
                self.functionValues[hardwareId].setText(hardwareId + ": disconnected")

app = QApplication(sys.argv)
window = SensorDisplay()
window.startIO()
sys.exit(app.exec())
