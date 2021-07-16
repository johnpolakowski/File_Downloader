from bs4 import BeautifulSoup
import os
import csv
import re
import requests
import urllib.request
from .IC_type import Find_IC_Type
import PyPDF2

debug_prnt = False

def clean_string(str):
    for i in range(0, len(str)):
        try:
            #str[i].encode("ascii")
            str[i].encode("utf-8")
        except:
            #means it's non-ASCII
            print(str[i])
            str = str.replace(str[i]," ") #replacing it with a single space
    for character in ['\r', '\t', '\n', '\"']:
        str = str.replace(character, '')
    return str.strip()


# this method is for package strings, such as "0402". str.strip() in clean_string method removes the leading 0, thus annoying "402" result
# here rstrip is used which elimnates trailing whitespace
def clean_package_string(str):
    for i in range(0, len(str)):
        try:
            str[i].encode("utf-8")
        except:
            #means it's non-ASCII
            str = str.replace(str[i]," ") #replacing it with a single space

    for char in ['\r', '\t', '\n', '\"']:
        str = str.replace(char, '')

    return str.rstrip()

#easy method for debug printing. To print the output set the variable 'debug_prnt' declared above to true
def debug_print(str):
    if debug_prnt == True:
        print(str)

class Component:
    def __init__(self, dk_component_url):
        # Common properties to all components#
        self.manufacturer = None
        self.manufacturer_part_num = None
        self.description = None
        self.dk_component_url = dk_component_url
        self.dk_search_url = None
        self.dk_part_num = None
        self.dk_status = None
        self.dk_unit_price = None
        self.qty_in_stock = None
        self.mfg_name = None
        self.mfg_part_num = None
        self.datasheet_link = None
        self.height = None
        self.operating_temp = None
        self.storage_temp = None
        self.value = None
        self.footprint = None
        self.symbol = None
        self.soup = None
    
    def scrape(self):
        html = requests.get(self.dk_component_url).text
        if html:
           self.soup = BeautifulSoup(html, "lxml")
        else:
            return 
        if self.soup:
            temp = self.soup.find("h1", {"itemprop": "model"})
            if temp:
                self.mfg_part_num = temp.text.strip()
                debug_print(self.mfg_part_num)
            
            temp = self.soup.find("td", {"id": "reportPartNumber"})
            if temp:
                self.dk_part_num = temp.text.strip()
                debug_print(self.dk_part_num)

            temp = self.soup.find("span", {"itemprop": "price"})
            if temp:
                self.dk_unit_price = temp.text.strip()
                debug_print(self.dk_unit_price)

            temp = self.soup.find("span", {"itemprop": "name"})
            if temp:
                self.mfg_name = temp.text.strip()
                debug_print(self.mfg_name)

            temp = self.soup.find("td", {"itemprop": "description"})
            if temp:
                self.description = temp.text.strip()
                debug_print(self.description)

            temp = self.soup.find("span", {"id": "dkQty"})
            if temp:
                self.qty_in_stock = temp.text.strip()
                debug_print(self.qty_in_stock)

            table_rows = self.soup.find_all("tr")      # grab all table rows #
            for row in table_rows:              
                if 'Height' in row.text and not '-' in row.text:
                    self.height = None if row.find('td') is None else row.find('td').text.strip()
                    if self.height == '-':
                        self.height = None
                    debug_print(self.height)

                if 'Operating Temperature' in row.text:
                    self.operating_temp = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.operating_temp)
                if 'Part Status' in row.text:
                    self.dk_status = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.dk_status)
                
            temp = self.soup.find("a", {"class": "lnkDatasheet"})
            if temp:
                self.datasheet_link = temp.get('href')
                debug_print(self.datasheet_link)
                    #self.datasheet = temp.text.strip()

            datasheet_tag = self.soup.find("a", {"class": "lnkDatasheet"})
            if datasheet_tag:
                self.datasheet_link = datasheet_tag.get('href')
                if self.datasheet_link:
                    if self.datasheet_link.startswith('//media'):
                        self.datasheet_link = 'https:'

    def get_description(self):
        if self.description:
            return clean_string(self.description)
        else:
            return ''
    
    def get_dk_component_url(self):
        if self.dk_component_url:
            return clean_string(self.dk_component_url)
        else:
            return ''
    
    def get_dk_search_url(self):
        if self.description:
            return clean_string(self.dk_search_url)
        else:
            return ''

    def get_dk_part_num(self):
        if self.dk_part_num:
            return clean_string(self.dk_part_num)
        else:
            return ''

    def get_dk_status(self):
        if self.dk_status:
            return clean_string(self.dk_status)
        else:
            return ''

    def get_dk_unit_price(self):
        if self.dk_unit_price:
            return clean_string(self.dk_unit_price)
        else:
            return ''

    def get_dk_qty_in_stock(self):
        if self.qty_in_stock:
            return clean_string(self.qty_in_stock)
        else:
            return ''

    def get_mfg_name(self):
        if self.mfg_name:
            return clean_string(self.mfg_name)
        else:
            return ''

    def get_mfg_part_num(self):
        if self.mfg_part_num:
            return clean_string(self.mfg_part_num)
        else:
            return ''

    def get_datasheet_link(self):
        if self.datasheet_link:
            return clean_string(self.datasheet_link)
        else:
            return ''

    def get_height(self):
        if self.height:
            return clean_string(self.height)
        else:
            return ''                      

    def get_operating_temp(self):
        if self.operating_temp:
            return clean_string(self.operating_temp)
        else:
            return ''                      
    def get_storage_temp(self):
        if self.storage_temp:
            return clean_string(self.storage_temp)
        else:
            return ''                      
    def get_value(self):
        if self.value:
            return clean_string(self.value)
        else:
            return ''                      
    def get_footprint(self):
        if self.height:
            return clean_string(self.footprint)
        else:
            return ''                      

    def get_symbol(self):
        if self.symbol:
            return clean_string(self.symbol)
        else:
            return ''  

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

    def save_datasheet(self):
        if self.datasheet_link:
            print(self.datasheet_link)
            local_filename ="datasheets\\" + self.mfg_part_num + ".pdf"
            r = requests.get(self.datasheet_link, stream=True, allow_redirects = True)
            with open(local_filename,'wb') as pypdf2:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: 
                        pypdf2.write(chunk)
            
            #urllib.request.urlretrieve(self.datasheet_link, local_filename)
            
class Resistor(Component):
    def __init__(self, dk_component_url):
        # Resistor parameters #
        self.package = None
        self.power = None
        self.tolerance = None
        self.temperature_coefficient = None
        self.size_dimension = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table_rows = self.soup.find_all("tr")      # grab all table rows #
            for row in table_rows:
                if 'Supplier Device Package' in row.text:
                    self.package = None if row.find('td') is None else row.find('td').text
                    debug_print(self.package)

                if not self.package or ("-" in self.package):
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                if 'Temperature Coefficient' in row.text:
                    self.temperature_coefficient = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.temperature_coefficient)

                if 'Power (Watts)' in row.text:
                    self.power= None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.power)

                if 'Tolerance' in row.text:
                    self.tolerance = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.tolerance)
                
                if 'Resistance' in row.text:
                    self.value = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.value)

                if not self.height or (self.height == '-'):
                    if 'Thickness (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                    
                    elif 'Height' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)

                if 'Size / Dimension' in row.text:
                    self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.size_dimension)

    def Get_New_Row(self, oldRow):
        #['item_number', 'item_name', 'item_category', 'mfg', 'mfg_pn', 'digikey desc', 'digikey URL', 'datasheet', 'dk status', 'dk price', 'AECQ', 'ASIL', 'Height', 'OperatingTemperature', 'Value', 'Tolerance', 'Power', 'Package', 'Size/Dimension', 'TempCoeff', 'Footprint', 'Symbol'  ]
        newRow = [oldRow[0], oldRow[1], oldRow[2], oldRow[3], oldRow[4], self.get_description(), self.get_dk_component_url(), self.get_datasheet(), self.get_dk_status(), self.get_dk_unit_price(), 
                '', self.get_height(), self.get_operating_temp(), self.get_value(), self.get_tolerance(), self.get_power(), self.get_package(),  self.get_size(), self.get_temperature_coefficient(), '', '']
        return newRow

    def get_package(self):
        if self.package and not self.package == '-':
            return clean_package_string(self.package)
        else:
            return '' 

    def get_power(self):
        if self.power and not self.power == '-':
            return clean_string(self.power)
        else:
            return '' 

    def get_tolerance(self):
        if self.tolerance and not self.tolerance == '-':
            return clean_string(self.tolerance)
        else:
            return '' 

    def get_temperature_coefficient(self):
        if self.temperature_coefficient and not self.temperature_coefficient == '-':
            return clean_string(self.temperature_coefficient)
        else:
            return '' 

    def get_size(self):
        if self.size_dimension:
            return clean_string(self.size_dimension)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Capacitor(Component):
    def __init__(self, dk_component_url):
        # Capacitor parameters #
        self.package = None
        self.tolerance = None
        self.esr = None
        self.current = None
        self.voltage_rating = None
        self.dielectric = None
        self.size_dimension = None
        self.capacitor_type = None
        self.lifetime = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table_rows = self.soup.find_all("tr")      # grab all table rows #
            for row in table_rows:
                if 'Package / Case' in row.text:
                    self.package = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.package)
                
                if not self.package or ("-" in self.package):
                    if 'Supplier Device Package' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)
                
                if 'Temperature Coefficient' in row.text:
                    self.dielectric = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.dielectric)

                if 'Voltage - Rated' in row.text:
                    self.voltage_rating= None if row.find('td') is None else row.find('td').text.strip()
                    if self.voltage_rating == '-':
                        self.voltage_rating = None
                    debug_print(self.voltage_rating)

                if 'Tolerance' in row.text:
                    self.tolerance = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.tolerance)
                
                if 'Capacitance' in row.text:
                    self.value = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.value)
                
                if not self.height or ("-" in self.height):
                    if 'Thickness (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                
                if 'Size / Dimension' in row.text:
                    self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.size_dimension)
               
                if 'ESR (Equivalent Series Resistance)' in row.text:
                    self.esr = None if row.find('td') is None else row.find('td').text.strip()
                    if "-" in self.esr:
                        self.esr = None

                if 'Lifetime @ Temp.' in row.text:
                    self.lifetime = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.lifetime)
                
                category_link = row.find_all("td", {"class": "attributes-td-categories-link"})
                if category_link:
                    for item in category_link:
                        if item:
                            category_text = item.find("a", {"style": "margin-left:10px"})
                            if category_text:
                                regex = re.compile(r'>[^<]+[^<>]')   # regular expression to grab the text after the link
                                text_g = re.search(regex, str(category_text) )           # execute the regular expression on the tag
                                text = text_g.group()                            # gets the string representation of the link
                                if text:
                                    clean_text = text.replace('>', '')
                                    self.capacitor_type = clean_text.replace('Capacitors', '')

    def Get_New_Row(self):
        #['capacitor_type', 'description', 'manufacturer', manufacturer_part_number', digikey URL', 'datasheet', 'dk status', 'dk price', 'Height', 'OperatingTemperature', 'Value', 'Tolerance', 'VoltageRating', 'ESR', 'Lifetime@Temp', 'Package', 'Dielectric', 'Size/Dimension', 'Footprint', 'Symbol'  ]
        newRow = [self.get_capacitor_type(),  self.get_description(), self.get_manufacturer(), self.get_manufacturer_part_number(), self.get_dk_component_url(), self.get_datasheet(), self.get_dk_status(), self.get_dk_unit_price(), 
                self.get_height(), self.get_operating_temp(), self.get_value(), self.get_tolerance(), self.get_voltage_rating(), self.get_esr(), self.get_lifetime(), self.get_package(),  self.get_dielectric(), self.get_size(), '', '']
        return newRow

    def get_size(self):
        if self.size_dimension:
            return clean_package_string(self.size_dimension)
        else:
            return '' 

    def get_capacitor_type(self):
        if self.capacitor_type:
            return clean_package_string(self.capacitor_type)
        else:
            return ''

    def get_manufacturer(self):
        return super().get_mfg_name()

    def get_manufacturer_part_number(self):
        return super().get_mfg_part_num()

    def get_esr(self):
        if self.esr:
            return clean_package_string(self.esr)
        else:
            return ''

    def get_lifetime(self):
        if self.lifetime:
            return clean_package_string(self.lifetime)
        else:
            return ''

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_dielectric(self):
        if self.dielectric:
            return clean_string(self.dielectric)
        elif self.capacitor_type:
            if 'Electrolytic' in self.capacitor_type:
                return 'Electrolytic'
            elif 'Film' in self.capacitor_type:
                return 'Film'
            elif 'Tantalum' in self.capacitor_type:
                return 'Tantalum'
            elif 'Polymer' in self.capacitor_type:
                return 'Polymer'
        else:
            return '' 

    def get_tolerance(self):
        if self.tolerance:
            return clean_string(self.tolerance)
        else:
            return '' 

    def get_voltage_rating(self):
        if self.voltage_rating:
            return clean_string(self.voltage_rating)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Connector(Component):
    def __init__(self, dk_component_url):
        # Capacitor parameters #
        self.pin_pitch = None
        self.positions = None
        self.rows = None
        self.speed = None
        self.current_rating = None
        self.connector_type = None
        self.package = None
        self.mated_stacking_height = None
        self.contact_finish = None
        self.voltage_rating = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table_rows = self.soup.find_all("tr")      # grab all table rows #
            for row in table_rows:
                if 'Package / Case' in row.text:
                    self.package = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.package)
                
                if not self.package or ("-" in self.package):
                    if 'Supplier Device Package' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                if 'Connector Type' in row.text:
                    self.connector_type = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.connector_type)

                if not self.connector_type or ("-" == self.connector_type):
                    if 'Flat Flex Type' in row.text:
                        self.connector_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.connector_type)
                
                if not self.connector_type and not 'Mounting' in row.text and not 'Fastening' in row.text:
                    if 'Type' in row.text:
                        self.connector_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.connector_type)

                if 'Contact Finish - Mating' in row.text:
                        self.contact_finish = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.contact_finish)

                if not self.contact_finish or ("-" in self.contact_finish):
                    if 'Contact Finish' in row.text and not 'Thickness' in row.text and not 'Post' in row.text:
                        self.contact_finish = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.contact_finish)

                if 'Pitch - Mating' in row.text:
                    self.pin_pitch= None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.pin_pitch)
                
                if not self.pin_pitch:
                    if 'Pitch' in row.text:
                        self.pin_pitch = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.pin_pitch)

                if 'Number of Positions' in row.text:
                    self.positions = None if row.find('td') is None else row.find('td').text.strip()
                    if 'All' in self.positions:
                        self.positions = None
                        debug_print(self.positions)
                
                if 'Number of Rows' in row.text and not 'All' in row.text:
                    self.rows = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.rows)
                
                if 'Current Rating (Amps)' in row.text:
                    self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                    if self.current_rating.strip() == '-':
                        self.current_rating = None
                    debug_print(self.current_rating)

                if not self.current_rating:
                    if 'Current Rating' in row.text:
                        self.current_rating  = None if row.find('td') is None else row.find('td').text.strip()
                        if self.current_rating == '-':
                            self.current_rating = None
                            debug_print(self.current_rating )

                if 'Voltage Rating' in row.text:
                    self.voltage_rating = None if row.find('td') is None else row.find('td').text.strip()
                    if self.voltage_rating.strip() == '-':
                        self.voltage_rating = None
                    debug_print(self.voltage_rating)
                
                if not self.voltage_rating:
                    if 'Voltage' in row.text and not 'MLCC' in row.text and not 'Character' in row.text:
                        self.voltage_rating = None if row.find('td') is None else row.find('td').text.strip()
                        if self.voltage_rating.strip() == '-':
                            self.voltage_rating = None
                        debug_print(self.voltage_rating)

                if 'Mated Stacking Height' in row.text:
                    self.mated_stacking_height = None if row.find('td') is None else row.find('td').text.strip()
                    if self.mated_stacking_height == '-':
                        self.mated_stacking_height = None
                    debug_print(self.mated_stacking_height)
                
                if not self.mated_stacking_height:
                    if 'Contact Length - Mating' in row.text:
                        self.mated_stacking_height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.mated_stacking_height)

                if not self.height or (self.height == '-'):
                    if 'Insulation Height' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                
                if self.height:
                    if len(self.height) > 35:
                        self.height = None

    def get_mated_height(self):
        if self.mated_stacking_height:
            return clean_package_string(self.mated_stacking_height)
        else:
            return '' 


    def get_contact_finish(self):
        if self.contact_finish:
            return clean_package_string(self.contact_finish)
        else:
            return '' 
    
    def get_voltage_rating(self):
        if self.voltage_rating:
            return clean_package_string(self.voltage_rating)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_connector_type(self):
        if self.connector_type:
            return clean_string(self.connector_type)
        else:
            return '' 

    def get_rows(self):
        if self.rows:
            return clean_string(self.rows)
        else:
            return '' 

    def get_positions(self):
        if self.positions:
            return clean_string(self.positions)
        else:
            return '' 

    def get_current_rating(self):
        if self.current_rating:
            return clean_string(self.current_rating)
        else:
            return '' 

    def get_pitch(self):
        if self.pin_pitch:
            return clean_string(self.pin_pitch)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Crystal(Component):
    def __init__(self, dk_component_url):
        # Crystal parameters #
        self.frequency = None
        self.crystal_type = None
        self.tolerance = None
        self.current = None
        self.output = None
        self.package = None
        self.size_dimension = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table_rows = self.soup.find_all("tr")      # grab all table rows #
            for row in table_rows:
                if 'Package / Case' in row.text:
                    self.package = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.package)
                
                if not self.package or ("-" in self.package):
                    if 'Supplier Device Package' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                    self.crystal_type = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.crystal_type)

                if 'Frequency' in row.text and not 'Tolerance' in row.text and not 'Stability' in row.text:
                    self.frequency = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.frequency)

                if 'Frequency Tolerance' in row.text:
                    self.tolerance = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.tolerance)
                
                if not self.tolerance or ("-" in self.tolerance):
                    if 'Frequency Stability' in row.text:
                        self.tolerance = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.tolerance)
                
                if 'Height - Seated (Max)' in row.text:
                    self.height = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.height)
                
                if not self.height or ("-" in self.height):
                    if 'Height' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                    
                    elif 'Thickness' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                
                if 'Size / Dimension' in row.text:
                    self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                    debug_print(self.size_dimension)



    def get_size(self):
        if self.size_dimension:
            return clean_package_string(self.size_dimension)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_crystal_type(self):
        if self.crystal_type:
            return clean_string(self.crystal_type)
        else:
            return '' 

    def get_frequency(self):
        if self.frequency:
            return clean_string(self.frequency)
        else:
            return '' 

    def get_tolerance(self):
        if self.tolerance:
            return clean_string(self.tolerance)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Diode(Component):
    def __init__(self, dk_component_url):
        # Diode parameters #
        self.package = None
        self.max_reverse_voltage = None
        self.forward_voltage = None
        self.power = None
        self.diode_type = None
        self.forward_current = None
        self.leakage_current = None
        self.speed = None
        super().__init__(dk_component_url)


    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'Diode Type' in row.text:
                        self.diode_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.diode_type)

                    if not self.diode_type or ("-" in self.diode_type):
                        if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.diode_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.diode_type)

                    if 'Current - Average Rectified (Io)' in row.text:
                        self.forward_current = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.forward_current)

                    if not self.forward_current or ("-" in self.forward_current):
                        if 'Current - Peak Pulse' in row.text and not ('Reverse' in row.text or 'Leakage' in row.text):
                            self.forward_current = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.forward_current)
                        elif 'Current' in row.text and not ('Reverse' in row.text or 'Leakage' in row.text):
                            self.forward_current = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.forward_current)

                    if 'Voltage - Forward (Vf) (Max) @ If' in row.text:
                        self.forward_voltage= None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.forward_voltage)
                
                    if not self.forward_voltage  or ("-" in self.forward_voltage ):
                        if 'Voltage' in row.text and 'Forward' in row.text:
                            self.forward_voltage  = None if row.find('td') is None else row.find('td').text.strip()

                    if 'Voltage - DC Reverse (Vr) (Max)' in row.text:
                        self.max_reverse_voltage = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.max_reverse_voltage)

                    if not self.max_reverse_voltage  or ("-" in self.max_reverse_voltage ):
                        if 'Voltage' in row.text and 'Reverse' in row.text:
                            self.max_reverse_voltage  = None if row.find('td') is None else row.find('td').text.strip()

                    if 'Power - Peak Pulse' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)
                    
                    if not self.power  or ("-" in self.power ):
                        if 'Power' in row.text:
                            self.power  = None if row.find('td') is None else row.find('td').text.strip()
                            if self.power == "-":
                                self.power = None
                    
                    if 'Speed' in row.text:
                        self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.speed)

                    if 'Current - Reverse Leakage @ Vr' in row.text:
                        self.leakage_current = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.leakage_current)


    def get_speed(self):
        if self.speed:
            return clean_package_string(self.speed)
        else:
            return '' 

    def get_leakage_current(self):
        if self.leakage_current:
            return clean_package_string(self.leakage_current)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_diode_type(self):
        if self.diode_type:
            return clean_string(self.diode_type)
        else:
            return '' 

    def get_forward_voltage(self):
        if self.forward_voltage:
            return clean_string(self.forward_voltage)
        else:
            return '' 

    def get_reverse_voltage(self):
        if self.max_reverse_voltage:
            return clean_string(self.max_reverse_voltage)
        else:
            return '' 

    def get_power(self):
        if self.power:
            return clean_string(self.power)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Electro_Optical(Component):
    def __init__(self, dk_component_url):
        # Electro-Optical parameters #
        self.package = None
        self.power = None
        self.electro_optical_type = None
        self.wavelength = None
        self.size_dimension = None
        self.color = None
        super().__init__(dk_component_url)
        
       
    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'LED' in row.text:
                        self.electro_optical_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.electro_optical_type)

                    if not self.electro_optical_type:
                        if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.electro_optical_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.electro_optical_type)
                
                    if self.electro_optical_type == 'LED Indication - Discrete':
                        self.electro_optical_type = 'LED Discrete'

                    elif self.electro_optical_type == 'LEDs - Circuit Board Indicators, Arrays, Light Bars, Bar Graphs':
                        self.electro_optical_type = 'LEDs'
                    
                    if 'Power' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)

                    if not self.power or ("-" in self.power):
                        if 'Millicandela Rating' in row.text:
                            self.power = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.power)
                
                    if 'Height - Seated (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)

                    if not self.height or ("-" in self.height):
                        if 'Height (Max)' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)
                        elif 'Height' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)
                        elif 'Thickness (Max)' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)
                                            
                    if 'Size / Dimension' in row.text:
                        self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.size_dimension)

                    if 'Wavelength - Dominant' in row.text:
                        self.wavelength = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.wavelength)

                    if not self.wavelength or ("-" in self.wavelength):
                        if 'Wavelength - Peak' in row.text:
                            self.wavelength = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.wavelength)
                        elif 'Wavelength' in row.text:
                            self.wavelength = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.wavelength)
                    
                    if 'Color' in row.text:
                        self.color = None if row.find('td') is None else row.find('td').text.strip()
                        if self.color == '-':
                            self.color = None
                        debug_print(self.color)

    def get_wavelength(self):
        if self.wavelength:
            return clean_package_string(self.wavelength)
        else:
            return '' 

    def get_size(self):
        if self.size_dimension:
            return clean_package_string(self.size_dimension)
        else:
            return '' 

    def get_color(self):
        if self.color:
            return clean_package_string(self.color)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_electro_optical_type(self):
        if self.electro_optical_type:
            return clean_string(self.electro_optical_type)
        else:
            return '' 

    def get_power(self):
        if self.power:
            return clean_string(self.power)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class Fuse(Component):
    def __init__(self, dk_component_url):
        # Fuse parameters #
        self.package = None
        self.power = None
        self.current_rating = None
        self.voltage_rating = None
        self.fuse_type = None
        self.resistance = None
        self.size_dimension = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'Fuse Type' in row.text:
                        self.fuse_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.fuse_type)

                    if not self.fuse_type:
                        if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.fuse_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.fuse_type)
                
                    if 'Power' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)
                    
                    if 'Voltage Rating' in row.text:
                        self.voltage_rating = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.voltage_rating)
                    
                    if not self.current_rating or ("-" in self.current_rating):
                        if 'Current - Hold (Ih) (Max)' in row.text:
                            self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)
                        elif 'Current - Trip (It)' in row.text:
                            self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)
                        elif 'Current' in row.text:
                            self.current_rating= None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)

                    if 'Current Rating (Amps)' in row.text:
                        self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.current_rating)
                    
                    if not self.current_rating or ("-" in self.current_rating):
                        if 'Current - Hold (Ih) (Max)' in row.text:
                            self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)
                        elif 'Current - Trip (It)' in row.text:
                            self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)
                        elif 'Current' in row.text:
                            self.current_rating= None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)

                    if 'DC Cold Resistance' in row.text:
                        self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.resistance)
                    
                    if not self.resistance or ("-" in self.resistance):
                        if 'Resistance - Initial (Ri) (Min)' in row.text:
                            self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.resistance)

                        elif 'Resistance - Post Trip (R1) (Max)' in row.text:
                            self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.resistance)
                        elif 'Resistance' in row.text:
                            self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.resistance)

                    if 'Height - Seated (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                    
                    if not self.height or ("-" in self.height):
                        if 'Height' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)
                        elif 'Thickness (Max)' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)

                    if 'Size / Dimension' in row.text:
                        self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.size_dimension)


    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_size(self):
        if self.size_dimension:
            return clean_package_string(self.size_dimension)
        else:
            return '' 

    def get_resistance(self):
        if self.resistance:
            return clean_package_string(self.resistance)
        else:
            return '' 

    def get_fuse_type(self):
        if self.fuse_type:
            return clean_string(self.fuse_type)
        else:
            return '' 

    def get_power(self):
        if self.power:
            return clean_string(self.power)
        else:
            return '' 
    
    def get_current_rating(self):
        if self.current_rating:
            return clean_string(self.current_rating)
        else:
            return '' 

    def get_voltage_rating(self):
        if self.voltage_rating:
            return clean_string(self.voltage_rating)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

class IC(Component):
    def __init__(self, dk_component_url):
       # IC parameters #
        self.package = None
        self.pin_pitch = None
        self.speed = None
        self.IC_type = None
        self.current_output = None
        self.PSRR = None
        self.voltage_input_max = None
        self.voltage_output_max = None
        self.voltage_output_min_or_fixed = None
        self.voltage_dropout = None
        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'Speed' in row.text:
                        self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.speed)
                    
                    if not self.speed:
                        if 'Frequency - Switching' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()

                    if not self.speed:
                        if 'Frequency' in row.text and not 'Synthesizer' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Data Rate' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Max Propagation Delay @ V, Max CL' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Delay Time tpd(1) Max' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Access Time' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Rise / Fall Time (Typ)' in row.text:
                            self.speed = None if row.find('td') is None else row.find('td').text.strip()

                    if 'Power' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)

                    if 'Height - Seated (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)
                    
                    if 'Voltage - Input (Max)' in row.text:
                        self.voltage_input_max = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.voltage_input_max)

                    if not self.voltage_input_max:
                        if 'Voltage - Input' in row.text and not 'Offset' in row.text:
                            self.voltage_input_max = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Voltage - Supply' in row.text:
                            self.voltage_input_max = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Voltage - Supply, Single/Dual (±)' in row.text:
                            self.voltage_input_max = None if row.find('td') is None else row.find('td').text.strip()
                        
                        elif 'Voltage - VCCA' in row.text:
                            self.voltage_input_max = None if row.find('td') is None else row.find('td').text.strip()

                    if 'Voltage - Output (Max)' in row.text:
                        self.voltage_output_max = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.voltage_output_max)
                    
                    if 'Voltage - Output (Min/Fixed)' in row.text:
                        self.voltage_output_min_or_fixed = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.voltage_output_min_or_fixed)
                    
                    if 'Voltage Dropout (Max)' in row.text:
                        self.voltage_dropout = None if row.find('td') is None else row.find('td').text.strip()
                        self.IC_type = 'LDO'
                        debug_print(self.voltage_dropout)
                    if not self.voltage_dropout:
                        if 'Voltage' in row.text and 'Dropout' in row.text:
                            self.voltage_dropout = None if row.find('td') is None else row.find('td').text.strip()
                            self.IC_type = 'LDO'

                    if 'Current - Output' in row.text:
                        self.current_output = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.current_output)
                    
                    if 'PSRR' in row.text:
                        self.PSRR = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.PSRR)

                    if 'Non-Isolated PoL Module' in row.text:
                        self.IC_type = 'DC-DC Conv.'
                        debug_print(self.IC_type)

                    if 'Buck' in row.text and 'Topology' in row.text:
                        self.IC_type = 'DC-DC Buck'
                        debug_print(self.IC_type)
                    
                    if 'Boost' in row.text and 'Topology' in row.text:
                        self.IC_type = 'DC-DC Boost'
                        debug_print(self.IC_type)

                    if not self.IC_type:
                        category_link = row.find_all("td", {"class": "attributes-td-categories-link"})
                        if category_link:
                            for item in category_link:
                                if item:
                                    category_text = item.find("a", {"style": "margin-left:10px"})
                                    if category_text:
                                        regex = re.compile(r'>[^<]+[^<>]')   # regular expression to grab the text after the link
                                        text_g = re.search(regex, str(category_text) )           # execute the regular expression on the tag
                                        text = text_g.group()                            # gets the string representation of the link
                                        if text:
                                            print("text: ", text)
                                            self.IC_type = Find_IC_Type( text )
                                            print("IC type: " + self.IC_type + "\n")

            datasheet_tag = self.soup.find("a", {"class": "lnkDatasheet"})
            if datasheet_tag:
                datasheet_link = datasheet_tag.get('href') 

    def get_voltage_in_max(self):
        if self.voltage_input_max:
            return clean_package_string(self.voltage_input_max)
        else:
            return '' 

    def get_datasheet(self):
        if self.datasheet_link:
            return clean_package_string(self.datasheet_link)
        else:
            return '' 

    def get_voltage_out_max(self):
        if self.voltage_output_max:
            return clean_package_string(self.voltage_output_max)
        else:
            return '' 

    def get_Vout_min_or_fixed(self):
        if self.voltage_output_min_or_fixed:
            return clean_package_string(self.voltage_output_min_or_fixed)
        else:
            return '' 

    def get_voltage_dropout(self):
        if self.voltage_dropout:
            return clean_package_string(self.voltage_dropout)
        else:
            return '' 

    def get_current_output(self):
        if self.current_output:
            return clean_package_string(self.current_output)
        else:
            return '' 

    def get_PSRR(self):
        if self.PSRR:
            return clean_package_string(self.PSRR)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_IC_type(self):
        if self.IC_type:
            return clean_string(self.IC_type)
        else:
            return '' 
    
    def get_speed(self):
        if self.speed:
            return clean_string(self.speed)
        else:
            return '' 

    
    def get_pin_pitch(self):
        if self.pin_pitch:
            return clean_string(self.pin_pitch)
        else:
            return '' 

class Inductor(Component):
    def __init__(self, dk_component_url):
       # Inductor parameters #
        self.package = None
        self.power = None
        self.resistance= None
        self.frequency = None
        self.inductor_type = None
        self.current_rating = None
        self.tolerance = None
        self.shielding = None
        self.size_dimension = None
        self.core_material = None
        self.current_saturation = None

        super().__init__(dk_component_url)

    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'Frequency' in row.text:
                        self.frequency = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.frequency)
                    
                    if not self.frequency:
                        if 'Speed' in row.text:
                            self.frequency = None if row.find('td') is None else row.find('td').text.strip()
             
                    if 'Power' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)
                    
                    if 'Inductor Type' in row.text:
                        self.inductor_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.inductor_type)

                    if not self.inductor_type:
                        if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.inductor_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.inductor_type)

                    if 'Current' in row.text:
                        self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.current_rating)

                    if 'Tolerance' in row.text:
                        self.tolerance = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.tolerance)

                    if 'Resistance' in row.text:
                        self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.resistance)

                    if 'Height - Seated (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        if self.height == '-':
                            self.height == None
                        debug_print(self.height)

                    if not self.height:
                        if 'Thickness (Max)' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)


                    if 'Material - Core' in row.text:
                        self.core_material = None if row.find('td') is None else row.find('td').text.strip()
                        if self.core_material == '-':
                            self.core_material == None
                        debug_print(self.core_material)

                    if 'Shielding' in row.text:
                        self.shielding = None if row.find('td') is None else row.find('td').text.strip()
                        if self.shielding == '-':
                            self.shielding == None
                        debug_print(self.shielding)

                    if 'Current - Saturation' in row.text:
                        self.current_saturation = None if row.find('td') is None else row.find('td').text.strip()
                        if self.current_saturation == '-':
                            self.current_saturation == None
                        debug_print(self.current_saturation)

                    if 'Size / Dimension' in row.text:
                        self.size_dimension = None if row.find('td') is None else row.find('td').text.strip()
                        if self.size_dimension == '-':
                            self.size_dimension == None
                        debug_print(self.size_dimension)


    def get_core_material(self):
        if self.core_material:
            return clean_package_string(self.core_material)
        else:
            return '' 

    def get_current_saturation(self):
        if self.current_saturation:
            return clean_package_string(self.current_saturation)
        else:
            return '' 

    def get_shielding(self):
        if self.shielding:
            return clean_package_string(self.shielding)
        else:
            return '' 

    def get_size_dimension(self):
        if self.size_dimension:
            return clean_package_string(self.size_dimension)
        else:
            return '' 

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_inductor_type(self):
        if self.inductor_type:
            return clean_string(self.inductor_type)
        else:
            return '' 
    
    def get_frequency(self):
        if self.frequency:
            return clean_string(self.frequency)
        else:
            return '' 

    def get_power(self):
        if self.power:
            return clean_string(self.power)
        else:
            return '' 
    
    def get_resistance(self):
        if self.resistance:
            return clean_string(self.resistance)
        else:
            return '' 

    def get_current_rating(self):
        if self.current_rating:
            return clean_string(self.current_rating)
        else:
            return '' 

    def get_tolerance(self):
        if self.tolerance:
            return clean_string(self.tolerance)
        else:
            return '' 


class Transistor(Component):
    def __init__(self, dk_component_url):
        # Transistor parameters #
        self.package = None
        self.power = None
        self.resistance= None
        self.frequency = None
        self.current_rating = None
        self.V_Drain_Source = None
        self.V_Gate_Source = None
        self.transistor_type = None
        self.threshold_voltage = None
        super().__init__(dk_component_url)


    def scrape(self):
        debug_print(self.dk_component_url)
        super().scrape()

        if self.soup:
            table = self.soup.find("table", {"id": "product-attribute-table"})
            table_rows = None
            if table:
                table_rows = table.find_all("tr")      # grab all table rows #
            
            if table_rows:
                for row in table_rows:
                    if 'Package / Case' in row.text:
                        self.package = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.package)

                    if not self.package:
                        if 'Supplier Device Package' in row.text:
                            self.package = None if row.find('td') is None else row.find('td').text.strip()
                
                    if 'Frequency' in row.text:
                        self.frequency = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.frequency)
                        if self.frequency.strip() == '-':
                            self.frequency == None
                    
                    if not self.frequency:
                        if 'Speed' in row.text:
                            self.frequency = None if row.find('td') is None else row.find('td').text.strip()
             
                    if 'Power Dissipation' in row.text or 'Power - Max' in row.text:
                        self.power = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.power)

                        if not self.power or self.power == '-':
                            if 'Power - Max' in row.text:
                                self.power = None if row.find('td') is None else row.find('td').text.strip()
                                if self.power == '-':
                                    self.power = None
                    
                    if 'Transistor Type' in row.text:
                        self.transistor_type = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.transistor_type)
                    
                    if not self.transistor_type:
                        if 'FET Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.transistor_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.transistor_type)

                    if not self.transistor_type:
                        if 'Type' in row.text and ( (not 'Mounting' in row.text) and (not 'Description' in row.text) ):
                            self.transistor_type = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.transistor_type)

                    if 'Current - Continuous Drain' in row.text:
                        self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.current_rating)
                    
                    if not self.current_rating:
                        if 'Current - Collector' in row.text:
                            self.current_rating = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.current_rating)

                    if 'Rds On' in row.text:
                        self.resistance = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.resistance)

                    if 'Height - Seated (Max)' in row.text:
                        self.height = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.height)

                    if not self.height:
                        if 'Thickness (Max)' in row.text:
                            self.height = None if row.find('td') is None else row.find('td').text.strip()
                            debug_print(self.height)

                    if 'Drain to Source Voltage' in row.text or 'Vdss' in row.text:
                        self.V_Drain_Source = None if row.find('td') is None else row.find('td').text.strip()
                        debug_print(self.V_Drain_Source)      
                    
                    #if not self.voltage:
                        #if 'Voltage - Collector Emitter Breakdown' in row.text:
                            #self.voltage = None if row.find('td') is None else row.find('td').text.strip()
                            #debug_print(self.voltage)



                    if 'Vgs(th) (Max) @ Id' in row.text or 'Vgs' in row.text:
                        self.V_Gate_Source = None if row.find('td') is None else row.find('td').text.strip()
                        if self.V_Gate_Source == '-':
                            self.V_Gate_Source = None
                        debug_print(self.V_Gate_Source)    
                    

    def get_package(self):
        if self.package:
            return clean_package_string(self.package)
        else:
            return '' 

    def get_datasheet(self):
        return super().get_datasheet()
    
    def get_transistor_type(self):
        if self.transistor_type:
            return clean_string(self.transistor_type)
        else:
            return '' 
    
    def get_drain_source_voltage(self):
        if self.V_Drain_Source:
            return clean_string(self.V_Drain_Source)
        else:
            return ''

    def get_gate_source_voltage(self):
        if self.V_Gate_Source:
            return clean_string(self.V_Gate_Source)
        else:
            return ''

    def get_frequency(self):
        if self.frequency:
            return clean_string(self.frequency)
        else:
            return '' 

    def get_power(self):
        if self.power:
            return clean_string(self.power)
        else:
            return '' 
    
    def get_resistance(self):
        if self.resistance:
            return clean_string(self.resistance)
        else:
            return '' 

    def get_current(self):
        if self.current_rating:
            return clean_string(self.current_rating)
        else:
            return '' 














