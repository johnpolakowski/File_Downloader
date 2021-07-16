class Click_Match:
    def __init__(self):
        self.click_cen_x = None         
        self.click_cen_y = None         
        self.click_width = None
        self.click_height = None
        self.img_match = None

class MatchList:
    def __init__(self, match=None):
        self.matches = []         # relative to coordinates returned by match (upper left hand corner)
        if match is not None:
            self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)

download_files2 = Click_Match()
download_files2.click_cen_x = 116             #click x loc relative to top left of image
download_files2.click_cen_y = 27             #click y loc relative to top left of image
download_files2.img_match = "../img/click/download_files2.png" 

download_files3 = Click_Match()
download_files3.click_cen_x = 113             #click x loc relative to top left of image
download_files3.click_cen_y = 28             #click y loc relative to top left of image
download_files3.img_match = "../img/click/download_files3.png" 

