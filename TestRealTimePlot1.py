
import sys, os
from PyQt5 import QtGui
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QIcon
import functools, numpy as np, random as rd, matplotlib
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import time, threading, serial as s, serial.tools.list_ports, struct
from matplotlib import style
import crc16

style.use("ggplot")

dataSteps = [()]
writeData = [()]
start_time = time.time()
SCALE_DOWN = 0
SCALE_UP = 32000
SCALE_GRAPH_VAL = 0.001225
FREQ_VAL = 1
print_counter = 1
MAX_FORCE_VALUE = 0

def uniq(high, low):
    return high << 8 | low

SIZER = 1000


def setCustomSize(x, width, height):
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(x.sizePolicy().hasHeightForWidth())
    x.setSizePolicy(sizePolicy)
    x.setMinimumSize(QtCore.QSize(width, height))
    x.setMaximumSize(QtCore.QSize(width, height))


class CustomMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        global MAX_FORCE_VALUE
        _translate = QtCore.QCoreApplication.translate
        super(CustomMainWindow, self).__init__()
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('Manual Setup')
        self.setWindowIcon(QIcon('snow.png'))
        self.FRAME_A = QtWidgets.QFrame(self)
        self.LAYOUT_A = QtWidgets.QVBoxLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)
        self.myFig = CustomFigCanvas()
        self.toolbar = NavigationToolbar(self.myFig, self)
        self.horLayout = QtWidgets.QHBoxLayout()
        self.horLayout.setObjectName('horLayout')
        self.horLayout.addWidget(self.toolbar)


        self.labelTest = QtWidgets.QLabel(self)
        self.labelTest.setObjectName('labelTest')

       
        #self.labelTest.setText('Value')
        #self.valSpinBox = QtWidgets.QDoubleSpinBox(self)
        #self.valSpinBox.setMinimum(-100.0)
        #self.valSpinBox.setMaximum(100.0)
        #self.valSpinBox.setSingleStep(0.01)
        #self.valSpinBox.setValue(1.0)
        #self.valSpinBox.setDecimals(6)
        #self.valSpinBox.setObjectName('spinBox')


        self.btnSetVal = QtWidgets.QPushButton(self)
        self.btnSetVal.setObjectName('btnSetVal')
        self.btnSetVal.setText('Set')
        graphScaleFile = open('graph.txt', 'r')
        for line in graphScaleFile:
            if len(line) != 0:
                SCALE_GRAPH_VAL = float(line)
            else:
                SCALE_GRAPH_VAL = 1.0

        #self.valSpinBox.setValue(SCALE_GRAPH_VAL)
        self.setGraphVal()
        self.labelTestFreq = QtWidgets.QLabel(self)
        self.labelTestFreq.setObjectName('labelTestFreq')
        #self.labelTestFreq.setText('MAX VALUE: ' + str(MAX_FORCE_VALUE))
        self.horLayoutMini1 = QtWidgets.QHBoxLayout()
        self.horLayoutMini1.setObjectName('horLayoutMini1')
        self.horLayoutMini2 = QtWidgets.QHBoxLayout()
        self.horLayoutMini2.setObjectName('horLayoutMini2')
        self.horLayoutMini1.addWidget(self.labelTest)
        #self.horLayoutMini1.addWidget(self.valSpinBox)
        self.horLayoutMini1.addWidget(self.btnSetVal)
        self.horLayoutMini2.addWidget(self.labelTestFreq)
        self.verLayout = QtWidgets.QVBoxLayout()
        self.verLayout.setObjectName('verLayout')
        self.verLayout.addLayout(self.horLayoutMini1)
        self.verLayout.addLayout(self.horLayoutMini2)
        self.horLayout.addWidget(self.toolbar)
        self.horLayout.addLayout(self.verLayout)
        self.LAYOUT_A.addLayout(self.horLayout)
        self.LAYOUT_A.addWidget(self.myFig)
        self.portNameLine = QtWidgets.QComboBox(self)
        self.portNameLine.setObjectName('portNameLine')
        comlist = serial.tools.list_ports.comports()
        port_name = ''
        if len(comlist) == 0:
            print('ERROR! Not connected device!')
            return
        for com in comlist:
            self.portNameLine.addItem(com.device)
            port_name = comlist[1].device

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName('verticalLayout_7')
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        #self.btn_port = QtWidgets.QPushButton(self)
       # self.btn_port.setObjectName('btn_port')
        self.horizontalLayout_2.addWidget(self.portNameLine)
        #self.horizontalLayout_2.addWidget(self.btn_port)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName('label')
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.cb_mode = QtWidgets.QComboBox(self)
        self.cb_mode.setObjectName('cb_mode')
        self.cb_mode.addItem('')
        self.cb_mode.addItem('')
        self.horizontalLayout_3.addWidget(self.cb_mode)
        self.btn_Mode = QtWidgets.QPushButton(self)
        self.btn_Mode.setObjectName('btn_Mode')
        self.btn_Stop = QtWidgets.QPushButton(self)
        self.btn_Stop.setObjectName('btn_Stop')
        self.horizontalLayout_3.addWidget(self.btn_Mode)
        self.horizontalLayout_3.addWidget(self.btn_Stop)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName('groupBox')
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName('label_2')
        self.verticalLayout_2.addWidget(self.label_2)
        self.downLim = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.downLim.setAlignment(QtCore.Qt.AlignCenter)
        self.downLim.setMinimum(0)
        self.downLim.setMaximum(32000 * SCALE_GRAPH_VAL)
        self.downLim.setSingleStep(1000 * SCALE_GRAPH_VAL)
        self.downLim.setObjectName('downLim')
        self.verticalLayout_2.addWidget(self.downLim)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName('label_3')
        self.verticalLayout_3.addWidget(self.label_3)
        self.upLim = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.upLim.setAlignment(QtCore.Qt.AlignCenter)
        self.upLim.setMinimum(0 * SCALE_GRAPH_VAL)
        self.upLim.setMaximum(32000 * SCALE_GRAPH_VAL)
        self.upLim.setSingleStep(1000 * SCALE_GRAPH_VAL)
        self.upLim.setObjectName('upLim')
        self.verticalLayout_3.addWidget(self.upLim)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName('label_4')
        self.verticalLayout_4.addWidget(self.label_4)
        self.count = QtWidgets.QSpinBox(self.groupBox)
        self.count.setAlignment(QtCore.Qt.AlignCenter)
        self.count.setMinimum(0)
        self.count.setMaximum(1000000)
        self.count.setObjectName('count')
        self.verticalLayout_4.addWidget(self.count)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.label_3.raise_()
        self.verticalLayout_6.addWidget(self.groupBox)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.btn = QPushButton('Start Mass Checker', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)
        
        self.timer = QBasicTimer()
        self.step = 0




        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.horizontalSlider = QtWidgets.QSlider(self)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(1000)
        self.horizontalSlider.setSingleStep(20)
        self.horizontalSlider.setPageStep(20)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')
        #self.horizontalSlider.setText(_translate('Dialog', '1-st motor: RPM'))

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.horizontalSlider2 = QtWidgets.QSlider(self)
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(1000)
        self.horizontalSlider2.setSingleStep(20)
        self.horizontalSlider2.setPageStep(20)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName('horizontalSlider2')


        self.horizontalLayout_4.addWidget(self.horizontalSlider)
        self.horizontalLayout_2.addWidget(self.pbar) 
        self.horizontalLayout_2.addWidget(self.btn)
        self.horizontalLayout_5.addWidget(self.horizontalSlider2)
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(1000)
        self.spinBox.setSingleStep(20)
        self.spinBox.setObjectName('spinBox')
        #self.spinBox.setText()
        self.horizontalLayout_4.addWidget(self.spinBox)


        self.spinBox2 = QtWidgets.QSpinBox(self)
        self.spinBox2.setMinimum(0)
        self.spinBox2.setMaximum(1000)
        self.spinBox2.setSingleStep(20)
        self.spinBox2.setObjectName('spinBox2')
        #self.spinBox.setText()
        self.horizontalLayout_5.addWidget(self.spinBox2)

        self.spinBox3 = QtWidgets.QSpinBox(self)
        self.spinBox3.setMinimum(1)
        self.spinBox3.setMaximum(5000)
        self.spinBox3.setSingleStep(20)
        self.spinBox3.setObjectName('spinBox3')
        #self.spinBox.setText()
        

        self.spinBox4 = QtWidgets.QSpinBox(self)
        self.spinBox4.setMinimum(1)
        self.spinBox4.setMaximum(5000)
        self.spinBox4.setSingleStep(20)
        self.spinBox4.setObjectName('spinBox4')
        #self.spinBox.setText()
        

        

        self.btn_setDAC = QtWidgets.QPushButton(self)
        self.btn_setDAC.setObjectName('btn_setDAC')
        self.btn_setDAC2 = QtWidgets.QPushButton(self)
        self.btn_setDAC2.setObjectName('btn_setDAC2')
        self.btn_setDAC3 = QtWidgets.QPushButton(self)
        self.btn_setDAC3.setObjectName('btn_setDAC3')
        self.btn_setDAC4 = QtWidgets.QPushButton(self)
        self.btn_setDAC4.setObjectName('btn_setDAC4')
        #self.cb_heater = QtWidgets.QCheckBox(self)
        #self.cb_heater.setObjectName('cb_heater')
        #self.horizontalLayout_4.addWidget(self.cb_heater)
        self.horizontalLayout_4.addWidget(self.btn_setDAC)
        self.horizontalLayout_5.addWidget(self.btn_setDAC2)
        
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalSlider.valueChanged['int'].connect(self.spinBox.setValue)
        self.horizontalSlider2.valueChanged['int'].connect(self.spinBox2.setValue)
        
        #self.spinBox.valueChanged['int'].connect(self.horizontalSlider.setValue)
        self.downLim.valueChanged['double'].connect(self.correctUpDownValue)
        self.upLim.valueChanged['double'].connect(self.correctUpDownValue)
        #self.btn_port.setText(_translate('Dialog', 'Close Port'))
        self.label.setText(_translate('Dialog', 'PORT checking for signal ....'))
        self.cb_mode.setItemText(1, _translate('Dialog', 'Cyclictus: '))
        self.cb_mode.setItemText(0, _translate('Dialog', 'Normal: '))
        self.btn_Mode.setText(_translate('Dialog', 'Start'))
        self.btn_Stop.setText(_translate('Dialog', 'Stop'))
        #self.groupBox.setTitle(_translate('Dialog', 'Cycle options:'))
        self.label_2.setText(_translate('Dialog', 'Down Lim'))
        self.label_3.setText(_translate('Dialog', 'Up Lim'))
        self.label_4.setText(_translate('Dialog', 'Count'))
        self.btn_setDAC.setText(_translate('Dialog', 'Set 1-st RPM'))
        self.btn_setDAC2.setText(_translate('Dialog', 'Set 2-nd RPM'))

        self.horizontalLayout_4.addWidget(self.spinBox3)
        self.horizontalLayout_5.addWidget(self.spinBox4)
        self.horizontalLayout_4.addWidget(self.btn_setDAC3)
        self.horizontalLayout_5.addWidget(self.btn_setDAC4)
        self.btn_setDAC3.setText(_translate('Dialog', 'Set Loops in 1-st motor'))
        self.btn_setDAC4.setText(_translate('Dialog', 'Set Loops in 2-nd motor'))



        #self.cb_heater.setText(_translate('Dialog', 'Heater'))
        self.btn_setDAC.clicked.connect(self.setDAC)
       # self.btn_port.clicked.connect(self.portOperation)
        self.btn_Mode.clicked.connect(self.modeSelection)
        self.btn_Stop.clicked.connect(self.stopMoving)
        #self.btnSetVal.clicked.connect(self.setGraphVal)
        self.cb_mode.currentIndexChanged.connect(self.changeMode)
        self.groupBox.setVisible(False)
        self.LAYOUT_A.addLayout(self.verticalLayout_7)
        DACfile = open('dac.txt', 'r')
        DACval = 0
        for line in DACfile:
            DACval = line

        self.spinBox.setValue(int(DACval))
        DACfile.close()
        writeData.clear()
        self.p = ''
        print(port_name)
        self.p = s.Serial(port_name, 9600)
        time.sleep(0.3)
        self.setDAC()
        self.myDataLoop = threading.Thread(name='myDataLoop', target=dataSendLoop, daemon=True, args=(self.addData_callbackFunc, self.p))
        self.myDataLoop.start()

    def timerEvent(self, e):

            if self.step >= 100:
                self.timer.stop()
                self.btn.setText('Zero mass value!!!')
                return

            self.step = self.step + 0.05
            self.pbar.setValue(self.step)


    def doAction(self):

            if self.timer.isActive():
                self.timer.stop()
                self.btn.setText('Mass Update')
            else:
                self.timer.start(100, self)
                self.btn.setText('Stop Mass Check')

    def setFreqVal(self):
        global FREQ_VAL
        FREQ_VAL = self.valSpinBoxFreq.value()

    def setGraphVal(self):
        SCALE_GRAPH_VAL = 0.2 # self.valSpinBox.value()
        self.myFig.setScale(SCALE_GRAPH_VAL)
        graphScaleFile = open('graph.txt', 'w')
        graphScaleFile.write(str(SCALE_GRAPH_VAL))
        graphScaleFile.close()

    def correctUpDownValue(self, val): 
        if self.upLim.value() < self.downLim.value():
            self.upLim.setValue(val)
            self.downLim.setValue(val)

    def setDAC(self):
        sendData = b'\x03'
        heater = b'\x00\x01'
        sendData += self.spinBox.value().to_bytes(2, byteorder='big', signed=True) + heater + b'\x00\x00'
        calc_crc = crc16.crc(sendData)
        sendData = b'\x06\x85'+sendData + calc_crc.to_bytes(2, byteorder ='big', signed = False)
        print(sendData)
        self.p.write(sendData)
        DACfile = open('dac.txt', 'w')
        DACfile.write(str(self.spinBox.value()))
        DACfile.close()

    def portOperation(self):
        pass

    def changeMode(self):
        if self.cb_mode.currentText() == 'Cyclic':
            self.groupBox.setVisible(True)
            self.groupBox.setChecked(True)
            self.resize(800, 500)
        if self.cb_mode.currentText() == 'Single':
            self.groupBox.setChecked(False)
            self.groupBox.setVisible(False)
            self.resize(800, 400)

    def modeSelection(self):
        global SCALE_GRAPH_VAL
        global start_time
        up_limit = 5000
        down_limit = -22000
        count = 1
        sendData = b'\x02'
        recordData = True
        start_time = time.time()
        if self.cb_mode.currentText() == 'Cyclic':
            up_limit = -self.upLim.value() / SCALE_GRAPH_VAL
            down_limit = -self.downLim.value() / SCALE_GRAPH_VAL
            count = self.count.value()
            sendData = b'\x01'
            recordData = False
        sendData += int(up_limit).to_bytes(2, byteorder='big', signed=True)
        sendData += int(down_limit).to_bytes(2, byteorder='big', signed=True)
        sendData += int(count).to_bytes(2, byteorder='big', signed=True)
        calc_crc = crc16.crc(sendData)
        sendData = b'\x06\x85' + sendData + calc_crc.to_bytes(2, byteorder='big', signed=False)
        print(sendData)
        self.p.write(sendData)

    def stopMoving(self):
        sendData = b'\x04'
        sendData += (0).to_bytes(2, byteorder='big', signed=True) + (0).to_bytes(2, byteorder='big', signed=True) + (0).to_bytes(2, byteorder='big', signed=True)
        calc_crc = crc16.crc(sendData)
        sendData = b'\x06\x85' + sendData + calc_crc.to_bytes(2, byteorder='big', signed=False)
        self.p.write(sendData)
        print(sendData)
        fileData = open('DataSingle.txt', 'w')
        for elem in writeData:
            fileData.write(str(elem[0]) + ';' + str(elem[1]) + '\n')

        fileData.close()
        writeData.clear()
        self.labelTestFreq.setText('MAX VALUE: ' + str(MAX_FORCE_VALUE))

    def zoomBtnAction(self):
        p.close()

    def addData_callbackFunc(self, value):
        self.myFig.addData(value)


#Test Part block: need to remove
def roomTempGen(roomTemp):
    temp = np.ones(SIZER)*roomTemp
    return temp


def cooler(roomTemp, nitrogenTemp):
    temp = np.linspace(roomTemp, nitrogenTemp, SIZER/25)
    return temp

def nitrogenGenerator(nitrogenTemp):
    temp = np.ones(SIZER)*nitrogenTemp
    return temp



def createForwardSignal(roomTemp, nitrogenTemp):
    return np.array(list(roomTempGen(roomTemp) ) + list(cooler(roomTemp, nitrogenTemp)) + list(nitrogenGenerator(nitrogenTemp)))



def createBackSignal(roomTemp, nitrogenTemp):
    return np.array( list(cooler( nitrogenTemp, roomTemp)) +list(roomTempGen(roomTemp) ) )


roomTemp = 22
nitrogenTemp = - 65
dMass = 25


class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self):
        self.addedData = []
        #print(matplotlib.__version__)
        
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)

        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y = np.random.normal(0, 0.15, len(self.n)) + roomTemp
        self.fig = Figure(figsize=(10, 14), dpi=100)
        
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.grid(True)
        self.ax1.set_xlabel('time, s ')
        self.ax1.set_ylabel('Temperature ')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='blue')
        self.line1_head = Line2D([], [], color='blue', marker='o', markeredgecolor='blue')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim((SCALE_DOWN - 5000) * SCALE_GRAPH_VAL, SCALE_UP * SCALE_GRAPH_VAL)

       
  




        

        FigureCanvas.__init__(self, self.fig)
        
        TimedAnimation.__init__(self, self.fig, interval=5, blit=True)
        

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        self.addedData.append(value)

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom = value
        top -= value
        self.ax1.set_ylim(bottom, top)
        self.draw()

    def setScale(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        self.ax1.set_ylim(bottom, top)
        self.draw()

    def _step(self, *args):
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)

    def _draw_frame(self, framedata):
        margin = 2
        while len(self.addedData) > 0:
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del self.addedData[0]

        self.line1.set_data(self.n[0:self.n.size - margin], self.y[0:self.n.size - margin])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]


class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(float)


def dataSendLoop(addData_callbackFunc, p):
    global MAX_FORCE_VALUE
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    n = np.linspace(0, 499, 500)
    y = 50 + 25 * np.sin(n / 8.3) + 10 * np.sin(n / 7.5) - 5 * np.sin(n / 1.5)
    i = 0
    adc_val = [0]
    while True:
        time.sleep(0.001)
        ind = 0
        wait_bytes = p.in_waiting
        coming_pack = ''
        crc_pack = ''
        if wait_bytes >= 7:
            f_byte = p.read(1)
            while chr(f_byte[0]).encode('utf-8') != '\x06':
                f_byte = p.read(1)

            s_byte = p.read(1)
            if s_byte == '\x85':
                coming_pack = p.read(3)
                crc_pack = p.read(2)
                calc_crc = crc16.crc(coming_pack)
                rec_crc = struct.unpack('H', crc_pack[0:2])
                if calc_crc == rec_crc[0]:
                    adc_val = struct.unpack('h', coming_pack[:2])
                    mySrc.data_signal.emit(-adc_val[0] * SCALE_GRAPH_VAL)
                    writeData.append((time.time() - start_time, -adc_val[0] * SCALE_GRAPH_VAL))
                    if int(-adc_val[0] * SCALE_GRAPH_VAL) > MAX_FORCE_VALUE:
                        MAX_FORCE_VALUE = -adc_val[0] * SCALE_GRAPH_VAL


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    myGUI = CustomMainWindow()
    myGUI.show()
    sys.exit(app.exec_())
# okay decompiling /home/workingcloud/asd/TestRealTimePlot1.cpython-35.pyc
