from PyQt5.QtCore import QObject, pyqtSlot


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
    

    