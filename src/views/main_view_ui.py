from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def __init__(self, MainWindow): 
        self.widget_init(MainWindow) 
        self.layout_init(MainWindow)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(301, 249)
 
    def setupUi(self, MainWindow):
        self.horizontalLayout_1.addWidget(self.label_volStart)
        self.horizontalLayout_1.addWidget(self.spinBox_start)

        self.horizontalLayout_2.addWidget(self.label_volEnd)
        self.horizontalLayout_2.addWidget(self.spinBox_end)

        self.horizontalLayout_3.addWidget(self.label_time)
        self.horizontalLayout_3.addWidget(self.spinBox_time)

        self.horizontalLayout_4.addWidget(self.label_signal)
        self.horizontalLayout_4.addWidget(self.checkBox_alog)
        self.horizontalLayout_4.addWidget(self.checkBox_dig)

        self.horizontalLayout_5.addWidget(self.label_port)
        self.horizontalLayout_5.addWidget(self.spinBox_port)

        self.horizontalLayout_6.addWidget(self.label_shape)
        self.horizontalLayout_6.addWidget(self.comboBox_shape)

        # Layout Finalize
        self.vboxlayout.addLayout(self.verticalLayout)
        self.vboxlayout.addLayout(self.horizontalLayout_1)
        self.vboxlayout.addLayout(self.horizontalLayout_2)
        self.vboxlayout.addLayout(self.horizontalLayout_3)
        self.vboxlayout.addLayout(self.horizontalLayout_4)
        self.vboxlayout.addLayout(self.horizontalLayout_5)
        self.vboxlayout.addLayout(self.horizontalLayout_6)
        
        self.vboxlayout.addWidget(self.pushButton_update)
        self.vboxlayout.addWidget(self.label_status)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def widget_init(self, MainWindow): 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.pushButton_update = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton_update.setEnabled(True)
        self.pushButton_update.setObjectName("pushButton_run")

        self.spinBox_start =  QtWidgets.QDoubleSpinBox(self.centralwidget) 
        self.spinBox_start.setMaximum(10)
        self.spinBox_start.setMinimum(0)
        self.spinBox_start.setObjectName("spinBox_start")

        self.spinBox_end =  QtWidgets.QDoubleSpinBox(self.centralwidget) 
        self.spinBox_end.setMaximum(10)
        self.spinBox_end.setMinimum(0)
        self.spinBox_end.setObjectName("spinBox_end")

        self.spinBox_time =  QtWidgets.QSpinBox(self.centralwidget) 
        self.spinBox_time.setMaximum(5000)
        self.spinBox_time.setObjectName("spinBox_time")

        self.checkBox_alog = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_alog.setObjectName('checkBox_analog')
        self.checkBox_alog.setChecked(True)
        self.checkBox_dig = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_dig.setObjectName('checkBox_digital')
        self.checkBox_dig.setEnabled(False)

        self.spinBox_port= QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_port.setObjectName('spinBox_port') 

        self.comboBox_shape = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_shape.setObjectName("comboBox_shape")
        self.comboBox_shape.addItem('Line') 
        # self.comboBox_shape.addItem('Square')
    
        # self.label_samplerate = QtWidgets.QLabel("Sample Rate")
        self.label_volStart = QtWidgets.QLabel("V. Start**:")
        self.label_volEnd = QtWidgets.QLabel("V. End**:")
        self.label_time = QtWidgets.QLabel("Time (sec)**:")
        self.label_signal = QtWidgets.QLabel("T.of signal:")
        self.label_port = QtWidgets.QLabel("Port:")
        self.label_shape = QtWidgets.QLabel("Shape:")
        self.label_status = QtWidgets.QLabel(self.centralwidget)

    def layout_init(self, MainWindow): 
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_update.setText(_translate("MainWindow", "Run"))
        self.checkBox_alog.setText(_translate("MainWindow", "Analog"))
        self.checkBox_dig.setText(_translate("MainWindow", "Digital"))

