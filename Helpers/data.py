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
        self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)

class Verify_Element:
    def __init__(self, match=None, figure_of_merit=None):
        self.img_match = match
        self.min_merit_value = figure_of_merit

cadence_menu = Click_Match()
cadence_menu.click_cen_x = 4             #click x loc relative to top left of image
cadence_menu.click_cen_y = 5             #click y loc relative to top left of image
cadence_menu.img_match = "../img/click_elements/cadence_menu.png" 

cadence_menu2 = Click_Match()
cadence_menu2.click_cen_x = 4             #click x loc relative to top left of image
cadence_menu2.click_cen_y = 8             #click y loc relative to top left of image
cadence_menu2.img_match = "../img/click_elements/cadence_menu2.png" 

capture_unchecked = Click_Match()
capture_unchecked.click_cen_x = 5             #click x loc relative to top left of image
capture_unchecked.click_cen_y = 7             #click y loc relative to top left of image
capture_unchecked.img_match = "../img/click_elements/capture_unchecked.png" 

download_files = Click_Match()
download_files.click_cen_x = 84             #click x loc relative to top left of image
download_files.click_cen_y = 20             #click y loc relative to top left of image
download_files.img_match = "../img/click_elements/download_files.png" 

download_now = Click_Match()
download_now.click_cen_x = 84             #click x loc relative to top left of image
download_now.click_cen_y = 20             #click y loc relative to top left of image
download_now.img_match = "../img/click_elements/download_now.png" 

login_button = Click_Match()
login_button.click_cen_x = 28             #click x loc relative to top left of image
login_button.click_cen_y = 14             #click y loc relative to top left of image
login_button.img_match = "../img/click_elements/login_button.png" 

login_button_main = Click_Match()
login_button_main.click_cen_x = 43             #click x loc relative to top left of image
login_button_main.click_cen_y = 18             #click y loc relative to top left of image
login_button_main.img_match = "../img/click_elements/login_button_main.png" 

login_button_main2 = Click_Match()
login_button_main2.click_cen_x = 42             #click x loc relative to top left of image
login_button_main2.click_cen_y = 22             #click y loc relative to top left of image
login_button_main2.img_match = "../img/click_elements/login_button_main2.png" 

not_a_robot_empty = Click_Match()
not_a_robot_empty.click_cen_x = 11             #click x loc relative to top left of image
not_a_robot_empty.click_cen_y = 13             #click y loc relative to top left of image
not_a_robot_empty.img_match = "../img/click_elements/not_a_robot_empty.png" 

not_a_robot_empty2 = Click_Match()
not_a_robot_empty2.click_cen_x = 11             #click x loc relative to top left of image
not_a_robot_empty2.click_cen_y = 10             #click y loc relative to top left of image
not_a_robot_empty2.img_match = "../img/click_elements/not_a_robot_empty2.png" 

not_a_robot_empty3 = Click_Match()
not_a_robot_empty3.click_cen_x = 26             #click x loc relative to top left of image
not_a_robot_empty3.click_cen_y = 33             #click y loc relative to top left of image
not_a_robot_empty3.img_match = "../img/click_elements/not_a_robot_empty3.png" 

password = Click_Match()
password.click_cen_x = 36             #click x loc relative to top left of image
password.click_cen_y = 16             #click y loc relative to top left of image
password.img_match = "../img/click_elements/password.png" 

pcb_unchecked = Click_Match()
pcb_unchecked.click_cen_x = 4             #click x loc relative to top left of image
pcb_unchecked.click_cen_y = 7             #click y loc relative to top left of image
pcb_unchecked.img_match = "../img/click_elements/pcb_unchecked.png" 

pcb_unchecked2 = Click_Match()
pcb_unchecked2.click_cen_x = 7             #click x loc relative to top left of image
pcb_unchecked2.click_cen_y = 11             #click y loc relative to top left of image
pcb_unchecked2.img_match = "../img/click_elements/pcb_unchecked2.png" 

search_bar = Click_Match()
search_bar.click_cen_x = 30             #click x loc relative to top left of image
search_bar.click_cen_y = 20             #click y loc relative to top left of image
search_bar.img_match = "../img/click_elements/search_bar.png" 

step_unchecked = Click_Match()
step_unchecked.click_cen_x = 4             #click x loc relative to top left of image
step_unchecked.click_cen_y = 5             #click y loc relative to top left of image
step_unchecked.img_match = "../img/click_elements/step_unchecked.png" 

threeD_menu = Click_Match()
threeD_menu.click_cen_x = 3             #click x loc relative to top left of image
threeD_menu.click_cen_y = 5             #click y loc relative to top left of image
threeD_menu.img_match = "../img/click_elements/threeD_menu.png" 

url_bar = Click_Match()
url_bar.click_cen_x = 265             #click x loc relative to top left of image
url_bar.click_cen_y = 22             #click y loc relative to top left of image
url_bar.img_match = "../img/click_elements/url_bar.png" 

url_bar2 = Click_Match()
url_bar2.click_cen_x = 113             #click x loc relative to top left of image
url_bar2.click_cen_y = 13             #click y loc relative to top left of image
url_bar2.img_match = "../img/click_elements/url_bar2.png" 

username = Click_Match()
username.click_cen_x = 26             #click x loc relative to top left of image
username.click_cen_y = 15             #click y loc relative to top left of image
username.img_match = "../img/click_elements/username.png" 

Cadence_Menu = MatchList(cadence_menu)
Cadence_Menu.Add(cadence_menu2)

Capture_Unchecked = MatchList(capture_unchecked)

Download_Files = MatchList(download_files)

Download_Now = MatchList(download_now)

Login_Button = MatchList(login_button)

Login_Button_Main = MatchList(login_button_main)
Login_Button_Main.Add(login_button_main2)

Not_A_Robot_Empty = MatchList(not_a_robot_empty)
Not_A_Robot_Empty.Add(not_a_robot_empty2)
Not_A_Robot_Empty.Add(not_a_robot_empty3)

Password = MatchList(password)

Pcb_Unchecked = MatchList(pcb_unchecked)
Pcb_Unchecked.Add(pcb_unchecked2)

Search_Bar = MatchList(search_bar)

Step_Unchecked = MatchList(step_unchecked)

ThreeD_Menu = MatchList(threeD_menu)

Url_Bar = MatchList(url_bar)
Url_Bar.Add(url_bar2)

