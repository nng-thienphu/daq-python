from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow(self)
        self._ui.label_status.setText(self._model.status)
        self._ui.setupUi(self)

        self._ui.pushButton_update.clicked.connect(lambda: self.btn_update_clicked())

    def btn_update_clicked(self): 
        print("Button Clicked...")
        self._main_controller.update_start(self._ui.spinBox_start.value())
        self._main_controller.update_end(self._ui.spinBox_end.value())
        self._main_controller.update_time(self._ui.spinBox_time.value())
        self._main_controller.update_signal_analog(self._ui.checkBox_alog.isChecked())
        self._main_controller.update_port(self._ui.spinBox_port.value())
        self._main_controller.update_shape(self._ui.comboBox_shape.currentText())
        # self._main_controller.update_status("Running...")
        # self._ui.label_status.setText(self._model.status)

        print("Checking...")
        print("V. Start Value: {}".format(self._model.start))
        print("V. End Value: {}".format(self._model.end))
        print("Time Value : {}".format(self._model.time))
        print("Analog Signal? : {}".format(self._model.signal_analog))
        print("Digital Signal? : {}".format(self._model.signal_digital))
        print("Port: {}".format(self._model.port))
        print("Shape : {}".format(self._model.shape))

        # main function here
        print("Working on sampling...")
        self._model.sample_line_shape()
        self._ui.label_status.setText("Running Completed")

    @pyqtSlot(int) 
    def on_amplitude_changed(self, value): 
        # self._ui.spinBox_amount2.setValue(value)
        print(self._model.amplitude())
