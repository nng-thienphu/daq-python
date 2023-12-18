from PyQt5.QtCore import QObject, pyqtSignal
import nidaqmx
import nidaqmx.system
import numpy as np
from nidaqmx import constants
from nidaqmx import stream_writers 
import time
from nidaqmx.stream_writers import DigitalSingleChannelWriter
import numpy as np

class Model(QObject): 
    run_activated = pyqtSignal(bool)

    def __init__(self):
        super().__init__()     
        self._start = 0
        self._end = 0 
        self._time = 0
        self._sigAnalog = False 
        self._sigDigital = False
        self.port = 0
        self._shape = "None"
        self._run = False

        self._numpoints = 10000
        
        self._status = "Welcom to the app"
    
    @property
    def start(self): 
        return self._start

    @start.setter 
    def start(self,value): 
        self._start = value

    @property
    def end(self): 
        return self._end

    @end.setter 
    def end(self, value): 
        self._end = value

    @property
    def time(self): 
        return self._time

    @time.setter 
    def time(self, value): 
        self._time = value

    @property
    def signal_analog(self): 
        return self._sigAnalog

    @signal_analog.setter 
    def signal_analog(self, value): 
        self._sigAnalog = value
    
    @property
    def signal_digital(self): 
        return self._sigDigital

    @signal_digital.setter 
    def signal_digital(self, value): 
        self._sigDigital = value
    
    @property
    def port(self): 
        return self._port
    
    @port.setter
    def port(self, value):  # value = string ? 
        self._port = value

    @property
    def shape(self): 
        return self._shape
    
    @shape.setter
    def shape(self, value):  # value = string
        self._shape = value
    
    @property
    def status(self): 
        return self._status
    
    @status.setter
    def status(self, value):  # value = string
        self._status = value

    def run(self, value): 
        self._run = value
        self.run_activated.emit(value)
    
    def sample(self): 
        if(self._sigAnalog == True) and (self._shape == True): 
            try: 
                self.sample_line_shape()
            except ZeroDivisionError:
                self.status = "Error: Division by zero occurred" 
                print(self.status)
            except Exception as e: 
                self.status = "An unexpected error occurred: {e}"

    def sample_line_shape(self): 
        # if(self._shape == "Square"): 
        #     samples = np.append(self._amplitude*np.ones(50), np.zeros(50))
        #     samples_mode = constants.AcquisitionType.CONTINUOUS
        samples = np.linspace(self._start, self._end, self._numpoints)
        samples_mode = constants.AcquisitionType.FINITE
        
        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao0')
        try: 
            task.timing.cfg_samp_clk_timing(rate= self._numpoints/self._time, sample_mode= samples_mode, samps_per_chan= self._numpoints)
        except ZeroDivisionError: 
            print("Error: Division by zero in calculating rate") 
            return
        
        print("Configure !")

        test_Writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(task.out_stream, auto_start=True)
        test_Writer.write_many_sample(samples)
        print("Wave output...")

        time.sleep(self._time+3)
        task.stop()
        task.close()
        print("Done")