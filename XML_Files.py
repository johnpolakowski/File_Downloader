from Stat_File import FileHelper
from Footprint_Parser.Footprint_Parser import Footprint_Parser

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


class XML_File:
    def __init__(self, source_filepath, report_directory):
        self.read_filepath = source_filepath.replace(os.sep, '/')     # replace '\' with '/'
        self.base_file = FileHelper.Get_Filename_No_Extension(self.read_filepath)   #gets "SOT-23_DIO" from C:/Users/poppy/Documents/Cadence/Libraries/XML/Parts/SOT-23_DIO.xml
        self.read_filename = self.base_file + ".xml"                           # SOT-23_DIO.xml
        self.write_filepath  = self.read_filepath 
        self.report_filepath = report_directory + "Report.txt"

        print("\t\t", self.read_filename, "\t\t", "[{}]".format(self.read_filepath) )


class XML_Parser:
    def __init__(self):
        self = self

    def Process_Allegro_XML_File(self, XML_file):
        with open(XML_file, 'r') as footprint_xml:
            print("=====================================================")
            parse_file = XML_File(footprint_xml.name, reports_directory)
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


    def Create_Batch_File_Script(self, XML_File, STEP_filepath = None):
        dir_path = FileHelper.Get_Directory(XML_File)
        filename = FileHelper.Get_Filename_No_Extension(XML_File)
        
        script_name = "create_" + filename + ".script"
        script_path = dir_path + "/" + script_name
        print("script name: ", script_name)
        print("script path: ", script_path)


        batch_file = open(script_path, 'w')
        string = 'skill changeWorkingDir "{}"\n'.format(dir_path)
        batch_file.write(string)

        string = 'skill LB_createFootprint "{}"\n'.format(XML_File) 
        batch_file.write(string)

        batch_file.write('scriptmode +i +n\n')

        if STEP_filepath is not None:
            STEP_file = FileHelper.Get_Base_Filename(STEP_filepath)
            batch_file.write('step pkg map\n')
            batch_file.write('setwindow form.pkgmap3d\n')

            string = 'FORM pkgmap3d stplist {}\n'.format(STEP_file)
            batch_file.write(string)
        
            batch_file.write('FORM pkgmap3d rotation_x 0\n')
            batch_file.write('FORM pkgmap3d save_current\n')
            batch_file.write('FORM pkgmap3d done\n')
            batch_file.write('setwindow pcb\n')
            batch_file.write('save\n')
            batch_file.write('fillin yes\n')

        batch_file.write('exit\n')
        batch_file.flush()
        batch_file.close()
        return script_path


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