import numpy as np
import time
import pymmcore_plus
import os.path
import matplotlib.pyplot as plt
from useq import MDASequence, MDAEvent
from pymmcore_plus.mda.handlers import OMEZarrWriter
from pymmcore_plus.mda import mda_listeners_connected
from configuration.cam_config import CamConfig
from pymmcore_plus import TaggedImages

class Camera():
    # change adpter name
    def __init__(self, adapterName, deviceName, labelName): 
        
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
    
   
    # def take_image(self): 
    #     try: 
    #         self.mmc.snapImage()
    #         image = self.mmc.getImage()
    #         plt.imshow(image, cmap='gray')
    #         plt.show()

    #     except Exception as e: 
    #         print("An error occured while snapping image by taking name!")
    
    def snap_image(self): 
        # easy snap img method
        # snap_easy = MDAEvent(
        #     channel= CamConfig.channel, 
        #     exposure=CamConfig.exposure, 
        # )

        sequence = MDASequence(
            channels = [CamConfig.channel, # preset group
            {"config": CamConfig.config, 
             "exposure": CamConfig.exposure } 
            ], 
        
        time_plan= {
            "interval": CamConfig.time_plan, 
            "loops": CamConfig.loops
            },
        
        z_plan = {
            "range": CamConfig.z_plan_range, 
            "step": CamConfig.z_plan_step,
        },

        axis_order= CamConfig.axis_order
            )
        
        writer = OMEZarrWriter(
            "file.zarr", 
            overwrite= True, 
            minify_attrs_metadata= True
        )

        with mda_listeners_connected(writer): 
            self.mmc.run_mda(sequence)

    def pop_image(self): # check this again
        # block until the image is done
        images: list[TaggedImages] = []

        while self.mmc.isSequenceRunning(): 
            if self.mmc.getRemainingImageCount(): 
                images.append(self.mmc.popNextTaggedImage()) 
            else: 
                time.sleep(0.001)
        
        if self.mmc.isBufferOverflowed(): 
            raise MemoryError
        
        while self.mmc.getRemainingImageCount(): 
            images.append(self.mmc.popNextTaggedImage())
        


    
