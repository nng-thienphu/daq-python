from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
    
    @pyqtSlot(int) 
    def update_start(self, value): 
        self._model.start = value

    @pyqtSlot(int) 
    def update_end(self, value): 
        self._model.end = value
    
    @pyqtSlot(int) 
    def update_time(self, value): 
        self._model.time = value
    
    @pyqtSlot(int) 
    def update_signal_analog(self, value): 
        self._model.signal_analog = value
    
    @pyqtSlot(int) 
    def update_signal_digital(self, value): 
        self._model.signal_analog = value
    
    @pyqtSlot(int) 
    def update_port(self, value): 
        self._model.port = value
    
    @pyqtSlot(int) 
    def update_shape(self, value): 
        self._model.shape = value
    
    @pyqtSlot(str) 
    def update_status(self, value): 
        self._model.status = value
    
        
class ControllerSample(MainController):  
    sampling_finish = pyqtSignal()
    sampling_progress = pyqtSignal()    
    def sampling(self): 
        self.sampling_progress.emit()
        print("Checking...")
        print("V. Start Value: {}".format(self._model.start))
        print("V. End Value: {}".format(self._model.end))
        print("Time Value : {}".format(self._model.time))
        print("Analog Signal? : {}".format(self._model.signal_analog))
        print("Digital Signal? : {}".format(self._model.signal_digital))
        print("Port: {}".format(self._model.port))
        print("Shape : {}".format(self._model.shape))
        self._model.sample_line_shape() 
        self.sampling_finish.emit()
    
    def sampling_galvo(self): 
        self.sampling_progress.emit()
        print("Checking...")
        print("V. Start Value: {}".format(self._model.start))
        print("V. End Value: {}".format(self._model.end))
        print("Time Value : {}".format(self._model.time))
        print("Analog Signal? : {}".format(self._model.signal_analog))
        print("Digital Signal? : {}".format(self._model.signal_digital))
        print("Port: {}".format(self._model.port))
        print("Shape : {}".format(self._model.shape))
        self._model.generate_two_signals4() 
        self.sampling_finish.emit()