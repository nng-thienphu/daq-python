import numpy as np
import pymmcore_plus
import os.path
import matplotlib.pyplot as plt

class Camera():
    # change adpter name
    def __init__(self, adapterName="", deviceName="Camera-1", labelName="Camera-1"): 
        
        self.adapter_name = adapterName 
        self.device_name = deviceName
        self.label_name = labelName
        
        self.mmc = pymmcore_plus.CMMCorePlus()  

        #change variable here
        self.mmc.loadDevice(label = labelName, deviceName= deviceName, moduleName= adapterName) 
        self.mmc.initializeDevice(deviceName)  
        self.mmc.setCameraDevice(deviceName)

    def set_property(self, trigger_mode = None, exposed_out_mode = None, scan_mode = None): 
        #change the name of property
        if(trigger_mode is not None): 
            self.mmc.setProperty(self.device_name, 'TriggerMode', trigger_mode)
        if(exposed_out_mode is not None): 
            self.mmc.setProperty(self.device_name, 'ExposeOutMode', exposed_out_mode)
        if(scan_mode is not None): 
            self.mmc.setProperty(self.device_name, 'ScanMode', trigger_mode)
    
   
    def take_image(self): 
        try: 
            self.mmc.snapImage()
            image = self.mmc.getImage()
            plt.imshow(image, cmap='gray')
            plt.show()

        except Exception as e: 
            print("An error occured while snapping image by taking name!")



    
