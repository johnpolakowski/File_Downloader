
UltraLibrarian Footprints/padstacks should be put in base direcory, along with step file
separate folder for snapeda, other download sites
    -change orcad capture filename
    -write report file of component, schem symbol, footprint, 3D file
    -copy footprint and padstacks and 3D file to the proper locations






rename file in Orcad Capture folder to the name of the part being processed  



#figure out type of component being searched, get manufacturer
    - if on a list of manufacturers, get simulation file from manufacturer


Strong To Do:

    if mil to mm, change padstack names
    must get component type, to search digikey if it is a capacitor or diode, this comes from parent list
        - if it is, we add the appropriate layer
    name footprint correctly




________________________________________________________________________________

Extraction of dimensions from pdf

________________________________________________________________________________
Part Grabbing:
    store local copy of Digikey Database in SQL
    have gui that searches parts
    have section that allows for comparison of parts by different parameters
    datasheets automatically downloaded for popular parts and categories


Datasheet Parsing:
    get mechanical outline dimensions
    get package height dimensions


Footprint Creation GUI:
    have general models for part archetypes
    adjust with a GUI: number of pads, pad width, dimensions, etc
    pullup datasheet and scroll to pages with dimension info


    Footprint Manipulation:
            - package geo / place bound top     ( w/ package height- 1:1 mechanical outline)
            - package geo / dfa bound top       ( courtyard, mech outline oversized by min 0.125 mm)
        
        ( later ) if there is Etch/Top layer that overlaps pads, it should be integrated into padstack

        write results for each function to report file
            - include new section for each file
            - 



Workflow:
    pull part numbers from schematic

        add PIN_ID layer, place pin one indicator, as well as polarity info on this layer. Pin ID Layer is RED. (Or black for cathode)
            - if more than 2 pins, && not diode or cap, PIN_ID becomes pin 1 indicator

        make sure to pair a schematic symbol with it, add schematic symbol to library
            -make sure it is of same type as symbol i.e. : opamp, clock, ADC, FPGA, microproccessor, dig isolator, cap, choke
        make sure all directory references use forward slash

        
        
        keep some kind of spreadsheet or html table that lists components by type
            - keeps track of schem symbol, footprint, padstacks, 3D file, 
            - keeps track of availabilities of schem symbol, footprint, 3D files


        if standard footprint, modify in Allegro:
            remove unnecessary layers
            size text appropriately
            keep dimensions but turn off visibility

STEP Files:
    get part name, search it and verify package type

    Step file( if paired with component):
        check if we already have it
        open in FreeCad or Solidworks, check dimensions, check colors, 
    Step files (if not paired with footprint):
        if passive: check if we already have it





