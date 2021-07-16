
#from Stat_File import FileHelper
import os

class CAD_Data_Object:
    def __init__(self):
        self.mfr_part_number = None
        self.vendor_part_number = None
        self.manufacturer_links = []
        self.footprint_links = []
        self.STEP_links = []
        self.SIM_model_links = []
        self.datasheet_links = []
        # [part#] [link to vendor part]  [link to manufacturer page] [links to download footprint]  [links to download STEP file] [links to simulation model]  [links to datasheet]
        