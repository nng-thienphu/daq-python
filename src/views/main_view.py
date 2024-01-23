from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QThread, QObject
from views.main_view_ui import Ui_MainWindow
from controllers.main_ctrl import ControllerSample


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow(self)
        self._ui.label_status.setText(self._model.status)
        self._ui.setupUi(self)
        self._ui.pushButton_update.clicked.connect(lambda: self.btn_update_clicked())

        # self.thread_sample_initialize()
        self.thread_galvo_initialize()
    
    def thread_galvo_initialize(self): 
        self._controller_galvo = ControllerSample(self._model)
        self.thread_galvo = QThread()
        self._controller_galvo.moveToThread(self.thread_galvo)

        self.thread_galvo.started.connect(self._controller_galvo.sampling_galvo)
        self.thread_galvo.finished.connect(
            lambda: self._ui.pushButton_update.setEnabled(True)
        )
        self.thread_galvo.finished.connect(lambda: self._ui.label_status.setText("Running Completed"))
        # self.thread_sample.finished.connect(self.thread_sample.deleteLater)

        self._controller_galvo.sampling_finish.connect(self.thread_galvo.quit)
        self._controller_galvo.sampling_progress.connect(lambda: print("working on sampling...")) 


    def thread_sample_initialize(self) : 
        # Create a QThread object and move controller to new thread
        self._controller_sample = ControllerSample(self._model)
        self.thread_sample = QThread()
        self._controller_sample.moveToThread(self.thread_sample)

        self.thread_sample.started.connect(self._controller_sample.sampling)
        self.thread_sample.finished.connect(
            lambda: self._ui.pushButton_update.setEnabled(True)
        )
        self.thread_sample.finished.connect(lambda: self._ui.label_status.setText("Running Completed"))
        # self.thread_sample.finished.connect(self.thread_sample.deleteLater)

        self._controller_sample.sampling_finish.connect(self.thread_sample.quit)
        self._controller_sample.sampling_progress.connect(lambda: print("working on sampling..."))
        # self._controller_sample.sampling_finish.connect(self._controller_sample.deleteLater)

    def btn_update_clicked(self): 
        self._ui.label_status.setText("Working on sampling...")  # Reset the label text here
        self._main_controller.update_start(self._ui.spinBox_start.value())
        self._main_controller.update_end(self._ui.spinBox_end.value())
        self._main_controller.update_time(self._ui.spinBox_time.value())
        self._main_controller.update_signal_analog(self._ui.checkBox_alog.isChecked())
        self._main_controller.update_port(self._ui.spinBox_port.value())
        self._main_controller.update_shape(self._ui.comboBox_shape.currentText())
        # self._main_controller.update_status("Running...")
        # self._ui.label_status.setText(self._model.status)

        # main function here
        print("Working on sampling...")
        # self.run_thread_sample()
        self.run_thread_galvo()

    @pyqtSlot(int) 
    def on_amplitude_changed(self, value): 
        # self._ui.spinBox_amount2.setValue(value)
        print(self._model.amplitude())
    
    def run_thread_sample(self):
        self.thread_sample.start()
        self._ui.pushButton_update.setEnabled(False) 

    def run_thread_galvo(self): 
        self.thread_galvo.start() 
        self._ui.pushButton_update.setEnabled(False) 
        

