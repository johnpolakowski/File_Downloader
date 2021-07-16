

class Click_Match:
    def __init__(self):
        self.click_cen_x = None         # relative to coordinates returned by match (upper left hand corner)
        self.click_cen_y = None         # relative to coordinates returned by match (upper left hand corner)
        self.click_width = None
        self.click_height = None
        self.img_match = None

class MatchList:
    def __init__(self, match=None):
        self.matches = []         # relative to coordinates returned by match (upper left hand corner)
        self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)

class Verify_Element:
    def __init__(self, match=None, figure_of_merit=None):
        self.img_match = match
        self.min_merit_value = figure_of_merit

UltraLibrarian_main_page = Verify_Element("./img/verify_page/Main_Page.png", 1500)
UltraLibrarian_search_page = Verify_Element("./img/verify_page/02_Logged_In_Page.png", 100)
UltraLibrarian_component_page = Verify_Element("./img/verify_page/component_page.png", 30)
UltraLibrarian_download_page = Verify_Element("./img/verify_page/select_downloads_page.png", 300)

UltraLibrarian_cadence_expanded = Verify_Element("./img/verify_page/cadence_menu_expanded.png", 200)
UltraLibrarian_step_expanded = Verify_Element("./img/verify_elements/Step_expanded.png", 100)
UltraLibrarian_captcha_checked = Verify_Element("./img/verify_page/captcha_completed.png", 25)
UltraLibrarian_captcha_unchecked = Verify_Element("./img/verify_elements/not_a_robot_unchecked.png", 20)
UltraLibrarian_download_complete = Verify_Element("./img/verify_elements/download_complete.png", 100)


UL_Main_Page   = "./img/verify_page/Main_Page.png"
UL_Search_Page = "./img/verify_page/search_page.png"
UL_Component_Page = "./img/verify_page/component_page.png"
UL_Download_Page = "./img/verify_page/select_downloads_page.png"
Cadence_Expanded_Menu = "./img/verify_page/cadence_menu_expanded.png"
Captcha_Completed = "./img/verify_page/captcha_completed.png"
Download_Complete = "./img/verify_page/download_complete.png"

threeD_menu = Click_Match()
threeD_menu.click_cen_x = 4             #relative to top left of clickable area
threeD_menu.click_cen_y = -7            #relative to top left of clickable area
threeD_menu.click_width = 8            #clickable width
threeD_menu.click_height = 8           #clickable height
threeD_menu.img_match = "./img/match_elements/3D_menu.png"

step_unchecked = Click_Match()
step_unchecked.click_cen_x = 5             #relative to top left of clickable area
step_unchecked.click_cen_y = -6            #relative to top left of clickable area
step_unchecked.click_width = 8            #clickable width
step_unchecked.click_height = 8           #clickable height
step_unchecked.img_match = "./img/match_elements/step_unchecked.png"

cadence_menu2 = Click_Match()
cadence_menu2.click_cen_x = 5             #relative to top left of clickable area
cadence_menu2.click_cen_y = -8            #relative to top left of clickable area
cadence_menu2.click_width = 8            #clickable width
cadence_menu2.click_height = 8           #clickable height
cadence_menu2.img_match = "./img/match_elements/Cadenc_menu2.png"

cadence_menu = Click_Match()
cadence_menu.click_cen_x = 5             #relative to top left of clickable area
cadence_menu.click_cen_y = -7            #relative to top left of clickable area
cadence_menu.click_width = 8            #clickable width
cadence_menu.click_height = 8           #clickable height
cadence_menu.img_match = "./img/match_elements/Cadenc_menu.png"

login = Click_Match()
login.click_cen_x =  44            #relative to top left of image
login.click_cen_y =  -20           #relative to top left of iamge
login.click_width =  65           #clickable width
login.click_height = 30           #clickable height
login.img_match = "./img/match_elements/UL_login.png"

login2 = Click_Match()
login2.click_cen_x = 30            #relative to top left of image
login2.click_cen_y = -17           #relative to top left of iamge
login2.click_width = 52           #clickable width
login2.click_height = 28           #clickable height
login2.img_match = "./img/match_elements/login_button.png"

username = Click_Match()
username.click_cen_x = 28            #relative to top left of clickable area
username.click_cen_y = -17           #relative to top left of clickable area
username.click_width = 42            #clickable width
username.click_height = 24           #clickable height
username.img_match = "./img/match_elements/username.png"

password = Click_Match()
password.click_cen_x = 40            #relative to top left of image
password.click_cen_y = -17           #relative to top left of iamge
password.click_width = 65           #clickable width
password.click_height = 25           #clickable height
password.img_match = "./img/match_elements/password.png"



urlbar = Click_Match()
urlbar.click_cen_x = 160            #relative to top left of image
urlbar.click_cen_y = -17           #relative to top left of iamge
urlbar.click_width = 30           #clickable width
urlbar.click_height = 10           #clickable height
urlbar.img_match = "./img/match_elements/url_bar.png"

urlbar2 = Click_Match()
urlbar2.click_cen_x = 160            #relative to top left of image
urlbar2.click_cen_y = -15           #relative to top left of iamge
urlbar2.click_width = 30           #clickable width
urlbar2.click_height = 10           #clickable height
urlbar2.img_match = "./img/match_elements/url_bar2.png"

urlbar3 = Click_Match()
urlbar3.click_cen_x = 165            #relative to top left of image
urlbar3.click_cen_y = -15           #relative to top left of iamge
urlbar3.click_width = 30           #clickable width
urlbar3.click_height = 10           #clickable height
urlbar3.img_match = "./img/match_elements/url_bar3.png"

pcb_footprint = Click_Match()
pcb_footprint.click_cen_x = 5            #relative to top left of image
pcb_footprint.click_cen_y = -7           #relative to top left of iamge
pcb_footprint.click_width = 9           #clickable width
pcb_footprint.click_height = 9           #clickable height
pcb_footprint.img_match = "./img/match_elements/pcb_unchecked.png"

capture_symbol = Click_Match()
capture_symbol.click_cen_x = 5            #relative to top left of image
capture_symbol.click_cen_y = -7           #relative to top left of iamge
capture_symbol.click_width = 9           #clickable width
capture_symbol.click_height = 9           #clickable height
capture_symbol.img_match = "./img/match_elements/capture_unchecked.png"

recaptcha_checkbox = Click_Match()
recaptcha_checkbox.click_cen_x = 15            #relative to top left of image
recaptcha_checkbox.click_cen_y = -16           #relative to top left of iamge
recaptcha_checkbox.click_width = 22           #clickable width
recaptcha_checkbox.click_height = 22           #clickable height
recaptcha_checkbox.img_match = "./img/match_elements/not_a_robot_empty2.png"

recaptcha_checkbox2 = Click_Match()
recaptcha_checkbox2.click_cen_x = 15            #relative to top left of image
recaptcha_checkbox2.click_cen_y = -15           #relative to top left of iamge
recaptcha_checkbox2.click_width = 22           #clickable width
recaptcha_checkbox2.click_height = 22           #clickable height
recaptcha_checkbox2.img_match = "./img/match_elements/not_a_robot_empty.png"

download_now_button = Click_Match()
download_now_button.click_cen_x = 88            #relative to top left of image
download_now_button.click_cen_y = -20           #relative to top left of iamge
download_now_button.click_width = 40           #clickable width
download_now_button.click_height = 20           #clickable height
download_now_button.img_match = "./img/match_elements/download_now.png"

download_files_button = Click_Match()
download_files_button.click_cen_x = 90            #relative to top left of image
download_files_button.click_cen_y = -20           #relative to top left of iamge
download_files_button.click_width = 40           #clickable width
download_files_button.click_height = 20           #clickable height
download_files_button.img_match = "./img/match_elements/download_files.png"


ThreeD_Menu = MatchList(threeD_menu)
Orcad_Symbol_Checkbox = MatchList(capture_symbol)
Recaptcha_Checkbox = MatchList(recaptcha_checkbox)
Recaptcha_Checkbox.Add(recaptcha_checkbox2)
Allegro_Footprint_Checkbox = MatchList(pcb_footprint)
STEP_Checkbox = MatchList(step_unchecked)

URL_Address_Bar = MatchList(urlbar3)
URL_Address_Bar.Add(urlbar2)

Password_box = MatchList(password)
Username_Box = MatchList(username)
Login_Page_Button = MatchList(login)
Cadence_Menu = MatchList(cadence_menu)
Cadence_Menu.Add(cadence_menu2)
Submit_Login_Button = MatchList(login2)
Download_Now_Button = MatchList(download_now_button)
Download_Files_Button = MatchList(download_files_button)



