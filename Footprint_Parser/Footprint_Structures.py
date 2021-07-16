
from Stat_File import FileHelper
import os

class Text_Block:
    def __init__(self, name, width, height, lineSpacing, characterSpacing, photoPlotWidth):
        self.name = name
        self.width = width
        self.height = height
        self.lineSpacing = lineSpacing
        self.characterSpacing = characterSpacing
        self.photoPlotWidth = photoPlotWidth

    def printBlock(self):
        print("name: {}".format(self.name))
        print("width: {}".format(self.width))
        print("height: {}".format(self.height))
        print("lineSpacing: {}".format(self.lineSpacing))
        print("charSpacing: {}".format(self.characterSpacing))
        print("photoWidth: {}".format(self.photoPlotWidth))

class XML_Footprint_Create:
    def __init__(self, XML_source, STEP_file = None):
        self.XML_source = XML_source
        self.STEP_file = STEP_file



class XML_File:
    def __init__(self, source_filepath, XML_write_directory, report_directory):
        self.read_filepath = source_filepath.replace(os.sep, '/')     # replace '\' with '/'
        self.base_file = FileHelper.Get_Filename_No_Extension(self.read_filepath)   #gets "SOT-23_DIO" from C:/Users/poppy/Documents/Cadence/Libraries/XML/Parts/SOT-23_DIO.xml
        self.read_filename = self.base_file + ".xml"                           # SOT-23_DIO.xml
        self.write_filepath  = XML_write_directory + self.read_filename   
        self.report_filepath = report_directory + "Report.txt"

        
        print("\t\t", self.read_filename, "\t\t", "[{}]".format(self.read_filepath) )

    

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
        