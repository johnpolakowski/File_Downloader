import xml.etree.ElementTree as ET

import os
import glob
import ntpath
import xml.dom.minidom
import sys
import re

import sys
import io
import itertools as IT

StringIO = io.StringIO

LAYERS_TO_DELETE = ['DEVICE TYPE/SILKSCREEN_TOP', 'DEVICE TYPE/ASSEMBLY_TOP', 'USER PART NUMBER/SILKSCREEN_TOP',  
        'COMPONENT VALUE/SILKSCREEN_TOP', 'TOLERANCE/SILKSCREEN_TOP', 'MANUFACTURING/NO_PROBE_TOP', 'PACKAGE KEEPOUT/TOP', 
        'ROUTE KEEPOUT/TOP' ]

VERIFY_LAYERS_PRESENT = ['PACKAGE GEOMETRY/ASSEMBLY_TOP', 'PACKAGE GEOMETRY/PLACE_BOUND_TOP', 'PACKAGE GEOMETRY/DFA_BOUND_TOP',
                        'REF DES/ASSEMBLY_TOP', 'REF DES/SILKSCREEN_TOP','PACKAGE GEOMETRY/SILKSCREEN_TOP']

ALERT_IF_PRESENT = ['ETCH/TOP', 'ETCH/BOTTOM']

mil_to_mm_XPATH = ['Extents', 'Padstack/Layers/Layer/Pad', 'TextBlocks/TextBlock', 'Pins/Pin', 'Layers/Layer', 'Layers/Layer/Path/Point', 'Layers/Layer/Path', 'Layers/Layer/Label', 'Layers/Layer/Circle']
mil_to_mm_TAGS = ['Extents', 'Pad', 'TextBlock', 'Pin', 'Layer', 'Point', 'Path', 'Label', 'Circle']
mil_to_mm_ATTRIBUTES = ['minX', 'minY', 'width', 'height', 'lineSpacing', 'characterSpacing', 'originX', 'originY', 'x', 'y', 'packageHeight', 'packageHeightMin', 'lineWidth', 'radius', 'diameter', 'cornerRadius', 'centerX', 'centerY', 'radius', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3',   ]
SELF_TERMINATING_TAGS = ['Units', 'Extents', 'Pad', 'TextBlock', 'Pin', 'Point', 'Label', 'Circle', 'Arc']

TEXTBLOCK_TAGS = ['TextBlocks', 'Textblocks', 'Text_Blocks', 'TEXTBLOCKS']
LINEWIDTH_TAGS = ['Path', 'Circle', 'Arc']

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

class Footprint_Parser:
    def __init__(self, parse_file):
        self.tree = None
        self.root = None
        self.Is_Valid_XML_File(parse_file)
        self.results = []
        #self.Is_Valid_XML_File(read_filepath)

    def Is_Valid_XML_File(self, parse_file):
        self.Fix_XML_File(parse_file.read_filepath)
        try:
            self.tree = ET.parse(parse_file.read_filepath)
            self.root = self.tree.getroot()
            print("...")
            print("parsing " + parse_file.read_filename + ":")
            return True
        except xml.etree.ElementTree.ParseError as error:
            error.msg = '{}'.format(error)
            print("\tException:", error.msg)
        return False

    
    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def Get_XML_Design_Units(self):
        Units = ''
        if self.root is None:
            return None
        for child in self.root:
        #print(child.tag, child.attrib, child.text)
            if child.tag == 'Units':
                Units = child.get('type')
                precision = child.get('precision')
                print("\tUnits:", Units, "  Precision:", precision, "decimal places" )
        return Units

    #figure out how to change padstack name as well
    def Change_XML_Design_Units(self):
        if self.root is None:
            return None
        for child in self.root:
            if child.tag == 'Units':    # changes the design units at top of XML file from mil to mm
                child.set('type', 'mm')
                child.set('precision', '4')
                print("\tConverted units to mm, 4 decimal places\n")

        # Search through XML file to find attributes which have values in mils, and convert them to mm
        #print("\tConverting to mm:\n\t[XML Path] \t[XML attribute]\t[mil dim]\t[mm dim]")
        for tag_search_path in mil_to_mm_XPATH:       # loop through list of possible tags containing values in mils
            for tag in self.root.findall(tag_search_path):    # for each path, execute a find on the xml tree to see if there are any matches
                for attribute in mil_to_mm_ATTRIBUTES:   # loop through all possible attributes which need dimension changed
                    mil_dimension = tag.get(attribute)     # see if matching tag also has an attribute which requires dimension change
                    if mil_dimension is not None:
                        mil_value = float(mil_dimension)    # converting string to double
                        mm_value = mil_value * 0.0254       # convert mil to mm
                        if mil_dimension == '6':
                            print("mm dimension:", mm_value)
                        mm_dimension = "{:.4f}".format(mm_value) # convert float to string with 4 decimal precision
                        tag.set(attribute, mm_dimension)

    def Remove_Undesired_Layers(self):
        if self.root is None:
            return None
        layer_block = self.root.find('Layers')
        layers = layer_block.findall('Layer')
        for layer in layers:
            layer_name = layer.get('name')
            if layer_name in LAYERS_TO_DELETE:
                layer_block.remove(layer)
                print("\tRemoved Layer: ", layer_name)

    def Check_Layer_Present(self, check_layer):
        if self.root is None:
            return None
        layer_block = self.root.find('Layers')
        layers = layer_block.findall('Layer')
        for layer in layers:
            layer_name = layer.get('name')
            if layer_name == check_layer:
                return True
        return False

    def Execute_Layer_Checks(self, report_file):
        if self.root is None:
            return None
        print()
        for layer in VERIFY_LAYERS_PRESENT:
            result = self.Check_Layer_Present(layer)
            if result == False:
                print('\tLayer \'{}\' is not present'.format(layer))

    def Get_Text_Blocks(self):
        if self.root is None:
            return None
        for tag in TEXTBLOCK_TAGS:
            block = self.root.find(tag)
            if block is not None:
                text_blocks = block.findall('TextBlock')
                return text_blocks

    def Parse_Text_Blocks(self):
        if self.root is None:
            return None
        TBlock_List = []
        blocklist = self.Get_Text_Blocks()
        print("\n\ttextblocks:")
        for text_block in blocklist:
            print("\t\t", text_block.attrib)
            attributes = text_block.attrib
            name = attributes['name']
            width = attributes['width']
            height = attributes['height']
            lineSpacing = attributes['lineSpacing']
            characterSpacing = attributes['characterSpacing']
            if 'photoplotWidth' in attributes.keys():
                photoplotWidth = attributes['photoplotWidth']
            else:
                photoplotWidth = None
            new_text_block = Text_Block(name, width,height, lineSpacing, characterSpacing, photoplotWidth)
            TBlock_List.append(new_text_block)
        return TBlock_List

    def Remove_Text_Block(self, remove_name):
        if self.root is None:
            return
        for tag in TEXTBLOCK_TAGS:
            textblocks = self.root.find(tag)
            if textblocks is not None:
                blocks = textblocks.findall('TextBlock')
                for block in blocks:
                    name = block.get('name')
                    if name is not None and name == remove_name:
                        textblocks.remove(block)

    def Add_Text_Block(self, add_block):
        if self.root is None:
            return
        for tag in TEXTBLOCK_TAGS:
            textblocks = self.root.find(tag)
            if textblocks is not None:
                new_block = ET.SubElement(textblocks, 'TextBlock')
                new_block.set('name', add_block.name)
                new_block.set('width', add_block.width)
                new_block.set('height', add_block.height)
                new_block.set('lineSpacing', add_block.lineSpacing)
                new_block.set('characterSpacing', add_block.characterSpacing)

    def indent(self):
        if self.root is None:
            return
        self.indent_recursive(self.root)

    def indent_recursive(self, elem, level=0, more_sibs=False):
        i = "\n"
        if level:
            i += (level-1) * '  '
        num_kids = len(elem)
        if num_kids:
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
                if level:
                    elem.text += '  '
            count = 0
            for kid in elem:
                self.indent_recursive(kid, level+1, count < (num_kids - 1) )
                count += 1
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
                if more_sibs:
                    elem.tail += '  '
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
                if more_sibs:
                    elem.tail += '  '


    def Check_LineWidth(self):
        if self.root is None:
            return
        print("\n\tChecking lineWidth property is nonzero")
        for tag in LINEWIDTH_TAGS:
            for line_object in self.root.iter(tag):
                if line_object is not None:
                    lineWidth_attrib = line_object.get('lineWidth')
                    if lineWidth_attrib is not None:
                        value = float(lineWidth_attrib)
                        if value == 0:
                            line_object.set('lineWidth', '0.1')
                    #print(line_object.attrib)

    def Write_to_File(self, write_filepath):
        if self.tree is None:
            return
        print("\n\twriting updated XML to file: ", write_filepath, "\n")
        self.tree.write(write_filepath)
    
    
    def Fix_XML_File(self, file):
        outfile = open('out.txt', 'w')
        with open(file, 'r') as fix_file:
            for line in fix_file:
                tagname = self.Get_Tag_Name(line)

                if self.Item_in_List(tagname, SELF_TERMINATING_TAGS):
                    result = self.Tag_is_Terminated(line)
                    if result == False:
                        print("\tnot terminated: ", line.strip() )
                        line = self.Add_Termination(line)
                outfile.write(line)

        outfile.close()
        fix_file.close()
        os.remove(file)
        os.rename(outfile.name, file)

    
    def Get_Tag_Name(self, line):
        pattern = re.compile(r'^\s*<(\w+)')
        result = pattern.findall(line)
        if len(result) == 1:
            return result[0]

    def Item_in_List(self, target_item, list):
        for item in list:
            if item == target_item:
                return True
        return False

    def Tag_is_Terminated(self, line):
        pattern = re.compile(r'(/>)')
        result = pattern.findall(line)
        if len(result) == 0:
            return False
        else:
            return True

    def Add_Termination(self, line):
        newline = re.sub('>', '/>', line)
        print("\t         fixed: ", newline.strip(), "\n" )
        return newline

