from PyQt5.QtCore import QObject, pyqtSignal
import nidaqmx
import nidaqmx.system
import numpy as np
from nidaqmx import constants
from nidaqmx import stream_writers 
import time
from nidaqmx.stream_writers import DigitalSingleChannelWriter
import numpy as np
from devices.camera import Camera
from nidaqmx.constants import LineGrouping, VoltageUnits



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
        task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')
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
    
    def sample_galvo(self): 
        samples = np.linspace(self._start, self._end, self._numpoints)
        samples_mode = constants.AcquisitionType.FINITE
        
        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')
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

    def collection_sample(self): 
        samples = np.linspace(self._start, self._end, self._numpoints)
        samples_mode = constants.AcquisitionType.FINITE
        
        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')

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
    
    def collection_sample2(self): 
        start = self._start  # replace with actual start value
        end = self._end      # replace with actual end value
        numpoints = self._numpoints  # replace with actual number of points

        channel1_data = np.linspace(start, end, numpoints)
        channel2_data = np.linspace(start, end, numpoints)

        sample_data = np.vstack([channel1_data, channel2_data])


        # Create a task for writing to analog output channels
        with nidaqmx.Task() as task:
            # Add analog output channels
            # Here, we're adding two channels: 'Dev1/ao0' and 'Dev1/ao1'
            task.ao_channels.add_ao_voltage_chan("PhyLabDevice/ao1", min_val=-10.0, max_val=10.0)
            task.ao_channels.add_ao_voltage_chan("PhyLabDevice/ao3", min_val=-10.0, max_val=10.0)

            # Configure the timing of the task
            task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=numpoints)

            # Write the data to the channels
            task.write(sample_data, auto_start=True)

            # Wait until the task is done
            task.wait_until_done()

        print("Data generation complete.")

    def collection_sample3(self): 
        duration = self._time
        start = self._start  # replace with actual start value
        end = self._end      # replace with actual end value
        numpoints = 1000  # replace with actual number of points
        sampling_rate = 1000 

        channel1_data = np.linspace(start, end, numpoints)

        time = np.linspace(0, duration, numpoints, endpoint=False)
        frequency = 1  # replace with the desired frequency

        channel2_data = np.sin(2 * np.pi * frequency * time)

        sample_data = np.vstack([channel1_data, channel2_data])

        # Create a task for writing to analog output channels
        with nidaqmx.Task() as task:
            # Add analog output channels
            # Here, we're adding two channels: 'Dev1/ao0' and 'Dev1/ao1'
            task.ao_channels.add_ao_voltage_chan("PhyLabDevice/ao1", min_val=-10.0, max_val=10.0)
            task.ao_channels.add_ao_voltage_chan("PhyLabDevice/ao3", min_val=-10.0, max_val=10.0)

            # Configure the timing of the task
            task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=numpoints)

            # Write the data to the channels
            task.write(sample_data, auto_start=True)

            # Wait until the task is done
            task.wait_until_done()

        print("Data generation complete.")

    def sine_wave_only(self): 
        amp = 4          # Amplitude 4V
        f = 4000        # Frequency 40kHz
        fs = 200000     # Sample Rate 200kHz

        # Efficient Sine Wave Generation
        x = np.arange(fs)
        y = amp * np.sin(2 * np.pi * f * x / fs)

        # Creating a DAQmx task
        with nidaqmx.Task() as test_Task:
            # Adding an analog output channel
            test_Task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')

            # Configuring the sample clock timing
            test_Task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Creating a writer and writing the sine wave data
            test_Writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(test_Task.out_stream, auto_start=True)
            test_Writer.write_many_sample(y)

            # Waiting for the task to be completed
            test_Task.wait_until_done()

            # Stopping and closing the task are handled by the context manager

    def sine_wave_based_on_input(self):
        # Get period T from user input
        T = self._time

        # Calculate frequency based on the period
        f = 1 / T

        # Other parameters
        amp = 2       # Amplitude 4V
        fs = 100000      # Sample Rate 2MHz
        numpoints = int(T * fs)  # Number of points based on the duration and sample rate

        # Generate sine wave
        x = np.linspace(0, T, numpoints, endpoint=False)
        y = amp * np.sin(2 * np.pi * f * x)

        # Create a task for writing to analog output channel
        with nidaqmx.Task() as test_Task:
            # Add analog output channel
            test_Task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')

            # Configure the sample clock timing
            test_Task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Create a writer and write the sine wave data
            test_Writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(test_Task.out_stream, auto_start=True)
            test_Writer.write_many_sample(y)

            # Wait for the task to be completed
            time.sleep(5)
            test_Task.stop()

        print("Sine wave generation complete.")
    
    def continuous_ramp_signal(self): 
        numpoints = 1000*10
        T = self._time
        samples = np.linspace(self._start, self._end, numpoints)
        larger_buffer = np.tile(samples, 10)  
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')

            # Set the rate based on the period and number of points
            rate = numpoints / T

            try:
                task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=numpoints)
            except ZeroDivisionError:
                print("Error: Division by zero in calculating rate")
                return

            print("Configure !")

            # Writing the ramp signal continuously
            test_Writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(task.out_stream, auto_start=True)
            while True:  # Loop to continuously write the signal
                test_Writer.write_many_sample(larger_buffer)
                time.sleep(T * 10)  
    
    def generate_two_signals1(self):
    # Sine Wave Parameters
        T = self._time  # Period for sine wave
        fs = 100000     # Sample Rate for both signals
        numpoints = int(T * fs)  
        
        #sine_wave 
        f = 1 / T       # Frequency for sine wave
        amp = 2         # Amplitude for sine wave

        x_sine = np.linspace(0, T, numpoints, endpoint=False)
        sine_wave = amp * np.sin(2 * np.pi * f * x_sine)

        # Ramp Signal Parameters
        # numpoints_ramp = 1000 * 10
        ramp_start = self._start
        ramp_end = self._end
        ramp = np.linspace(ramp_start, ramp_end, numpoints)
        # larger_buffer_ramp = np.tile(ramp, 10)

        # Ensure both signals have the same length
        # sine_wave = np.interp(np.linspace(0, T, len(larger_buffer_ramp), endpoint=False), x_sine, sine_wave)

        # Create a task for writing to analog output channels
        with nidaqmx.Task() as task:
            # Add analog output channels for both sine wave and ramp
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')

            # Configure the sample clock timing
            task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Create a writer for multi-channel
            test_Writer = nidaqmx.stream_writers.AnalogMultiChannelWriter(task.out_stream, auto_start=True)

            # Stack both signals for output
            combined_data = np.vstack([sine_wave, ramp])

            # Write the data to the channels
            test_Writer.write_many_sample(combined_data)

            # Run the task for a specified duration then stop
            time.sleep(10)
            task.stop()

        print("Sine wave and ramp signal generation complete.")

    def generate_two_signals2(self): 
        # Sine Wave Parameters
        T = self._time  # Period for sine wave
        f = 1 / T       # Frequency for sine wave
        amp = 2         # Amplitude for sine wave
        fs = 100000     # Sample Rate for both signals

        # Generate Sine Wave
        numpoints_sine = int(T * fs)
        x_sine = np.linspace(0, T, numpoints_sine, endpoint=False)
        sine_wave = amp * np.sin(2 * np.pi * f * x_sine)

        # Ramp Signal Parameters
        numpoints_ramp = 1000 * 10
        ramp_start = self._start
        ramp_end = self._end
        ramp = np.linspace(ramp_start, ramp_end, numpoints_ramp)
        larger_buffer_ramp = np.tile(ramp, 10)

        # Ensure both signals have the same length
        sine_wave = np.interp(np.linspace(0, T, len(larger_buffer_ramp), endpoint=False), x_sine, sine_wave)

        # Create a task for writing to analog output channels
        with nidaqmx.Task() as task:
            # Add analog output channels for both sine wave and ramp
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')

            # Configure the sample clock timing
            task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Create a writer for multi-channel
            test_Writer = nidaqmx.stream_writers.AnalogMultiChannelWriter(task.out_stream, auto_start=True)

            # Stack both signals for output
            combined_data = np.vstack([sine_wave, larger_buffer_ramp])

            # Write the data to the channels
            test_Writer.write_many_sample(combined_data)

            # Run the task for a specified duration then stop
            time.sleep(5)
            task.stop()
    
    def generate_two_signals3(self):
    # Sine Wave Parameters
        T = self._time  # Period for sine wave
        fs = 100000     # Sample Rate for both signals
        numpoints = int(T * fs)  
        
        #sine_wave 
        f = 1 / T       # Frequency for sine wave
        amp = 2         # Amplitude for sine wave

        x_sine = np.linspace(0, T, numpoints, endpoint=False)
        sine_wave = amp * np.sin(2 * np.pi * f * x_sine)

        # Ramp Signal Parameters
        # numpoints_ramp = 1000 * 10
        ramp_start = self._start
        ramp_end = self._end
        single_ramp_cycle = np.linspace(ramp_start, ramp_end, int(fs/f))
        ramp = np.tile(single_ramp_cycle, int(T * f))
        # larger_buffer_ramp = np.tile(ramp, 10)

        ramp = ramp[:len(sine_wave)]

        # Ensure both signals have the same length
        # sine_wave = np.interp(np.linspace(0, T, len(larger_buffer_ramp), endpoint=False), x_sine, sine_wave)

        # Create a task for writing to analog output channels
        with nidaqmx.Task() as task:
            # Add analog output channels for both sine wave and ramp
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')
            task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')

            # Configure the sample clock timing
            task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Create a writer for multi-channel
            test_Writer = nidaqmx.stream_writers.AnalogMultiChannelWriter(task.out_stream, auto_start=True)

            # Stack both signals for output
            combined_data = np.vstack([sine_wave, ramp])

            # Write the data to the channels
            test_Writer.write_many_sample(combined_data)

            # Run the task for a specified duration then stop
            time.sleep(10)
            task.stop()

        print("Sine wave and ramp signal generation complete.")
    
    def generate_two_signals4(self):
        # change these two line
        # iris = Camera(adapterName= "Fill in here", deviceName="Camera-1", labelName="Camera-1") 
        # iris.set_property(trigger_mode = "Edge Triggering", exposed_out_mode= "Any Row", scan_mode = "Scan Width")

        #digital signal
        digital_signal = [False, False, False, False, False, True, False, False, False, False, False]
        digital_line = "/PhyLabDevice/port0/line0"  

        # Sine Wave Parameters
        T = self._time  # Period for sine wave
        fs = 100000     # Sample Rate for both signals
        numpoints = int(T * fs)  
        
        #sine_wave 
        f = 1 / T       # Frequency for sine wave
        amp = 2         # Amplitude for sine wave

        x_sine = np.linspace(0, T, numpoints, endpoint=False)
        sine_wave = amp * np.sin(2 * np.pi * f * x_sine)

        # Ramp Signal Parameters
        # numpoints_ramp = 1000 * 10
        ramp_start = self._start
        ramp_end = self._end
        single_ramp_cycle = np.linspace(ramp_start, ramp_end, int(fs/f))
        ramp = np.tile(single_ramp_cycle, int(T * f))
        # larger_buffer_ramp = np.tile(ramp, 10)

        ramp = ramp[:len(sine_wave)]

        # Ensure both signals have the same length
        # sine_wave = np.interp(np.linspace(0, T, len(larger_buffer_ramp), endpoint=False), x_sine, sine_wave)

        # Create a task for writing to analog output channels
        with nidaqmx.Task() as analog_task, nidaqmx.Task() as digital_task:
            # Add analog output channels for both sine wave and ramp
            digital_task.do_channels.add_do_chan(
                digital_line,
                line_grouping=LineGrouping.CHAN_PER_LINE
            )
            analog_task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao1')
            analog_task.ao_channels.add_ao_voltage_chan('PhyLabDevice/ao3')

            for signal in digital_signal: 
                digital_task.write(signal) 
                if signal: 
                    # iris.take_image()
                    # Configure the sample clock timing
                    analog_task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

                    # Create a writer for multi-channel
                    test_Writer = nidaqmx.stream_writers.AnalogMultiChannelWriter(analog_task.out_stream, auto_start=True)

                    # Stack both signals for output
                    combined_data = np.vstack([sine_wave, ramp])

                    # Write the data to the channels
                    test_Writer.write_many_sample(combined_data)

                    # Run the task for a specified duration then stop
                    time.sleep(self._time)
                    # analog_task.stop()
                time.sleep(0.1)

        print("Sine wave and ramp signal generation complete.")
  