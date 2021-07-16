from Stat_File import FileHelper
from Footprint_Parser import Footprint_Parser
from Footprint_Structures import XML_File
import os

footprint_write_directory   = 'C:/Users/poppy/Documents/Cadence/Libraries/Footprints/'

capture_write_directory     = 'C:/Users/poppy/Documents/Cadence/Libraries/Capture/'
datasheets_directory        = 'C:/Users/poppy/Downloads/datasheets/'

XML_search_path             = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Parts/'
XML_create_directory        = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Create/'
reports_directory           = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Reports/'
STEP_search_path            = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/STEP/'
Allegro_STEP_directory      = 'C:/Users/poppy/Documents/Cadence/Libraries/3D_Files/01AA_3D_Files/'
Download_Directory          = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Downloads/'

def Process_XML_Files(XML_files):
    for file in XML_files:
        with open(file, 'r') as footprint_xml:
            print("=====================================================")
            parse_file = XML_File(footprint_xml.name, XML_create_directory, reports_directory)
            footprint_xml.close()

            parser = Footprint_Parser(parse_file)

            design_units = parser.Get_XML_Design_Units()
            if design_units == 'mils':
                parser.Change_XML_Design_Units()                        # converts each dimensional value in footprint to mm

            parser.Remove_Undesired_Layers()                            # removes extra crap thrown in footprints
            parser.Execute_Layer_Checks(parse_file.report_filepath)     # verifies necessary layers are present

            textblocklist = parser.Parse_Text_Blocks()

            parser.indent()             #pretty prints the xml
            parser.Check_LineWidth()    # verifies lineWidth property is nonzero

            parser.Write_to_File(parse_file.write_filepath)




XML_files = FileHelper.Get_XML_Files(XML_search_path)
for file in XML_files:
    print("\t" + FileHelper.Get_Base_Filename(file) )

Process_XML_Files(XML_files)

XML_footprint_files = FileHelper.Get_XML_Files(XML_create_directory)
STEP_files = FileHelper.Get_STEP_Files(STEP_search_path)


#XML_footprint_files = FileHelper.Match_STEP_Files( XML_create_directory, STEP_files)
#for file in XML_footprint_files:
    # if file has paired step file
        # copy step file to Allegro dir
    #write XML file to scr file

#execute scr file
# move footprints (.dra and psm) to Allegro PSM dir
# move padstacks to Allegro padstacks
# move STEP files to Allegro STEP dir
# create list of footprint names created
    # note for each footprint whether STEP needs to be mapped
    # maybe open Allegro to map the STEP file
# clean out create directory
    # move 


path = os.getcwd()
print("Current dir: " + path)


"""
#create script file
    change directory to "create" folder
    copy current dir to variable

    write to scr:
        load ...
        changedir to current dir ..
    for each xml :
        write to scr:
            lb create footprint ...
        if matching step:
            write to scr:
                [step stuff]
    write to scr:
        exit



    """