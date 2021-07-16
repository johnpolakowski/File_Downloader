import os
import csv
import glob


from Search_Online import Search_Engine




footprint_write_directory   = 'C:/Users/poppy/Documents/Cadence/Libraries/Footprints/'

capture_write_directory     = 'C:/Users/poppy/Documents/Cadence/Libraries/Capture/'
datasheets_directory        = 'C:/Users/poppy/Downloads/datasheets/'

XML_search_path             = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Parts/'
XML_create_directory        = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Create/'
reports_directory           = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Reports/'
STEP_search_path            = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/STEP/'
Allegro_STEP_directory      = 'C:/Users/poppy/Documents/Cadence/Libraries/3D_Files/01AA_3D_Files/'
Download_Directory          = 'C:/Users/poppy/Documents/Cadence/Libraries/XML/Downloads/'







Engine = Search_Engine('download_links.csv')
"""
Engine.Search_Digikey('MCU60P06-TP')
print()
Engine.Search_Digikey('2N7002K-T1-E3')
print()
Engine.Search_Digikey('IRLML2402TRPBF')
print()
Engine.Search_Digikey('AD8531AKSZ-REEL7')
"""
#Engine.Test_Detected()
Engine.Search('2N7002K-T1-E3', True, True, True, True)
#Engine.Downloaded_Parts.append("C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/2N7002K-T1-E3")
Engine.Process_Downloads()



#if part is in particular category, attempt to find simulation model

# if manufacturer is ti or analog devices, go to their sites
# otherwise go to google search 
# if simulatino model is already in LTSpice, dont worry about it

# for footprints on snap eda, be wary of footprints submitted by user. see in upper right hand corner

# create CSV FIle
# [part#] [link to vendor part]  [link to manufacturer page] [links to download footprint]  [links to download STEP file] [links to simulation model]  [links to datasheet]


#get datasheet link in upper right hand corner of DG part
# may be multiple datasheets in Media Section [datasheet, drawing, etc]
# may be multiple CAD files
# download picture of part  