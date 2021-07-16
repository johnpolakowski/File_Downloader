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
       
cadence_menu = Click_Match()
cadence_menu.click_cen_x = 4             #click x loc relative to top left of image
cadence_menu.click_cen_y = 5             #click y loc relative to top left of image
cadence_menu.img_match = "./img/click_elements/cadence_menu.png" 

cadence_menu2 = Click_Match()
cadence_menu2.click_cen_x = 4             #click x loc relative to top left of image
cadence_menu2.click_cen_y = 8             #click y loc relative to top left of image
cadence_menu2.img_match = "./img/click_elements/cadence_menu2.png" 

cadence_menu3 = Click_Match()
cadence_menu3.click_cen_x = 5             #click x loc relative to top left of image
cadence_menu3.click_cen_y = 8             #click y loc relative to top left of image
cadence_menu3.img_match = "./img/click_elements/cadence_menu3.png" 

capture_unchecked = Click_Match()
capture_unchecked.click_cen_x = 5             #click x loc relative to top left of image
capture_unchecked.click_cen_y = 7             #click y loc relative to top left of image
capture_unchecked.img_match = "./img/click_elements/capture_unchecked.png" 

capture_unchecked2 = Click_Match()
capture_unchecked2.click_cen_x = 11             #click x loc relative to top left of image
capture_unchecked2.click_cen_y = 9             #click y loc relative to top left of image
capture_unchecked2.img_match = "./img/click_elements/capture_unchecked2.png" 

capture_unchecked3 = Click_Match()
capture_unchecked3.click_cen_x = 9             #click x loc relative to top left of image
capture_unchecked3.click_cen_y = 9             #click y loc relative to top left of image
capture_unchecked3.img_match = "./img/click_elements/capture_unchecked3.png" 

download_files = Click_Match()
download_files.click_cen_x = 84             #click x loc relative to top left of image
download_files.click_cen_y = 20             #click y loc relative to top left of image
download_files.img_match = "./img/click_elements/download_files.png" 

download_files2 = Click_Match()
download_files2.click_cen_x = 116             #click x loc relative to top left of image
download_files2.click_cen_y = 27             #click y loc relative to top left of image
download_files2.img_match = "./img/click_elements/download_files2.png" 

download_files3 = Click_Match()
download_files3.click_cen_x = 113             #click x loc relative to top left of image
download_files3.click_cen_y = 28             #click y loc relative to top left of image
download_files3.img_match = "./img/click_elements/download_files3.png" 

download_files4 = Click_Match()
download_files4.click_cen_x = 100             #click x loc relative to top left of image
download_files4.click_cen_y = 25             #click y loc relative to top left of image
download_files4.img_match = "./img/click_elements/download_files4.png" 

download_files5 = Click_Match()
download_files5.click_cen_x = 100             #click x loc relative to top left of image
download_files5.click_cen_y = 25            #click y loc relative to top left of image
download_files5.img_match = "./img/click_elements/download_files5.png" 

download_now = Click_Match()
download_now.click_cen_x = 84             #click x loc relative to top left of image
download_now.click_cen_y = 20             #click y loc relative to top left of image
download_now.img_match = "./img/click_elements/download_now.png" 

download_now2 = Click_Match()
download_now2.click_cen_x = 91             #click x loc relative to top left of image
download_now2.click_cen_y = 21             #click y loc relative to top left of image
download_now2.img_match = "./img/click_elements/download_now2.png" 

download_now3 = Click_Match()
download_now3.click_cen_x = 122             #click x loc relative to top left of image
download_now3.click_cen_y = 29             #click y loc relative to top left of image
download_now3.img_match = "./img/click_elements/download_now3.png" 

download_now4 = Click_Match()
download_now4.click_cen_x = 122             #click x loc relative to top left of image
download_now4.click_cen_y = 29             #click y loc relative to top left of image
download_now4.img_match = "./img/click_elements/download_now4.png" 

login_button = Click_Match()
login_button.click_cen_x = 28             #click x loc relative to top left of image
login_button.click_cen_y = 14             #click y loc relative to top left of image
login_button.img_match = "./img/click_elements/login_button.png" 

login_button_main = Click_Match()
login_button_main.click_cen_x = 43             #click x loc relative to top left of image
login_button_main.click_cen_y = 18             #click y loc relative to top left of image
login_button_main.img_match = "./img/click_elements/login_button_main.png" 

login_button_main2 = Click_Match()
login_button_main2.click_cen_x = 42             #click x loc relative to top left of image
login_button_main2.click_cen_y = 22             #click y loc relative to top left of image
login_button_main2.img_match = "./img/click_elements/login_button_main2.png" 

not_a_robot_empty = Click_Match()
not_a_robot_empty.click_cen_x = 11             #click x loc relative to top left of image
not_a_robot_empty.click_cen_y = 13             #click y loc relative to top left of image
not_a_robot_empty.img_match = "./img/click_elements/not_a_robot_empty.png" 

not_a_robot_empty2 = Click_Match()
not_a_robot_empty2.click_cen_x = 11             #click x loc relative to top left of image
not_a_robot_empty2.click_cen_y = 10             #click y loc relative to top left of image
not_a_robot_empty2.img_match = "./img/click_elements/not_a_robot_empty2.png" 

not_a_robot_empty3 = Click_Match()
not_a_robot_empty3.click_cen_x = 26             #click x loc relative to top left of image
not_a_robot_empty3.click_cen_y = 33             #click y loc relative to top left of image
not_a_robot_empty3.img_match = "./img/click_elements/not_a_robot_empty3.png" 

not_a_robot_empty4 = Click_Match()
not_a_robot_empty4.click_cen_x = 26             #click x loc relative to top left of image
not_a_robot_empty4.click_cen_y = 34             #click y loc relative to top left of image
not_a_robot_empty4.img_match = "./img/click_elements/not_a_robot_empty4.png" 

not_a_robot_empty5 = Click_Match()
not_a_robot_empty5.click_cen_x = 23             #click x loc relative to top left of image
not_a_robot_empty5.click_cen_y = 35             #click y loc relative to top left of image
not_a_robot_empty5.img_match = "./img/click_elements/not_a_robot_empty5.png" 

password = Click_Match()
password.click_cen_x = 36             #click x loc relative to top left of image
password.click_cen_y = 16             #click y loc relative to top left of image
password.img_match = "./img/click_elements/password.png" 

pcb_unchecked = Click_Match()
pcb_unchecked.click_cen_x = 4             #click x loc relative to top left of image
pcb_unchecked.click_cen_y = 7             #click y loc relative to top left of image
pcb_unchecked.img_match = "./img/click_elements/pcb_unchecked.png" 

pcb_unchecked2 = Click_Match()
pcb_unchecked2.click_cen_x = 7             #click x loc relative to top left of image
pcb_unchecked2.click_cen_y = 11             #click y loc relative to top left of image
pcb_unchecked2.img_match = "./img/click_elements/pcb_unchecked2.png" 

pcb_unchecked3 = Click_Match()
pcb_unchecked3.click_cen_x = 9             #click x loc relative to top left of image
pcb_unchecked3.click_cen_y = 10             #click y loc relative to top left of image
pcb_unchecked3.img_match = "./img/click_elements/pcb_unchecked3.png" 

pcb_unchecked4 = Click_Match()
pcb_unchecked4.click_cen_x = 10             #click x loc relative to top left of image
pcb_unchecked4.click_cen_y = 11             #click y loc relative to top left of image
pcb_unchecked4.img_match = "./img/click_elements/pcb_unchecked4.png" 

search_bar = Click_Match()
search_bar.click_cen_x = 30             #click x loc relative to top left of image
search_bar.click_cen_y = 20             #click y loc relative to top left of image
search_bar.img_match = "./img/click_elements/search_bar.png" 

step_unchecked = Click_Match()
step_unchecked.click_cen_x = 5             #click x loc relative to top left of image
step_unchecked.click_cen_y = 6             #click y loc relative to top left of image
step_unchecked.img_match = "./img/click_elements/step_unchecked.png" 

step_unchecked2 = Click_Match()
step_unchecked2.click_cen_x = 9             #click x loc relative to top left of image
step_unchecked2.click_cen_y = 10             #click y loc relative to top left of image
step_unchecked2.img_match = "./img/click_elements/step_unchecked2.png"

step_unchecked3 = Click_Match()
step_unchecked3.click_cen_x = 9             #click x loc relative to top left of image
step_unchecked3.click_cen_y = 10             #click y loc relative to top left of image
step_unchecked3.img_match = "./img/click_elements/step_unchecked3.png"

step_unchecked4 = Click_Match()
step_unchecked4.click_cen_x = 9             #click x loc relative to top left of image
step_unchecked4.click_cen_y = 10             #click y loc relative to top left of image
step_unchecked4.img_match = "./img/click_elements/step_unchecked4.png"

step_unchecked5 = Click_Match()
step_unchecked5.click_cen_x = 8             #click x loc relative to top left of image
step_unchecked5.click_cen_y = 8             #click y loc relative to top left of image
step_unchecked5.img_match = "./img/click_elements/step_unchecked5.png"

threeD_menu = Click_Match()
threeD_menu.click_cen_x = 3             #click x loc relative to top left of image
threeD_menu.click_cen_y = 5             #click y loc relative to top left of image
threeD_menu.img_match = "./img/click_elements/threeD_menu.png" 

threeD_menu2 = Click_Match()
threeD_menu2.click_cen_x = 5             #click x loc relative to top left of image
threeD_menu2.click_cen_y = 9             #click y loc relative to top left of image
threeD_menu2.img_match = "./img/click_elements/threeD_menu2.png" 

threeD_menu3 = Click_Match()
threeD_menu3.click_cen_x = 6             #click x loc relative to top left of image
threeD_menu3.click_cen_y = 12             #click y loc relative to top left of image
threeD_menu3.img_match = "./img/click_elements/threeD_menu3.png" 

threeD_menu4 = Click_Match()
threeD_menu4.click_cen_x = 5             #click x loc relative to top left of image
threeD_menu4.click_cen_y = 9             #click y loc relative to top left of image
threeD_menu4.img_match = "./img/click_elements/threeD_menu4.png" 

threeD_menu5 = Click_Match()
threeD_menu5.click_cen_x = 4             #click x loc relative to top left of image
threeD_menu5.click_cen_y = 7             #click y loc relative to top left of image
threeD_menu5.img_match = "./img/click_elements/threeD_menu5.png" 

url_bar = Click_Match()
url_bar.click_cen_x = 265             #click x loc relative to top left of image
url_bar.click_cen_y = 22             #click y loc relative to top left of image
url_bar.img_match = "./img/click_elements/url_bar.png" 

url_bar2 = Click_Match()
url_bar2.click_cen_x = 113             #click x loc relative to top left of image
url_bar2.click_cen_y = 13             #click y loc relative to top left of image
url_bar2.img_match = "./img/click_elements/url_bar2.png" 

url_bar3 = Click_Match()
url_bar3.click_cen_x = 190             #click x loc relative to top left of image
url_bar3.click_cen_y = 15             #click y loc relative to top left of image
url_bar3.img_match = "./img/click_elements/url_bar3.png" 

url_bar4 = Click_Match()
url_bar4.click_cen_x = 190             #click x loc relative to top left of image
url_bar4.click_cen_y = 16             #click y loc relative to top left of image
url_bar4.img_match = "./img/click_elements/url_bar4.png" 

url_bar5 = Click_Match()
url_bar5.click_cen_x = 251             #click x loc relative to top left of image
url_bar5.click_cen_y = 19             #click y loc relative to top left of image
url_bar5.img_match = "./img/click_elements/url_bar5.png" 

username = Click_Match()
username.click_cen_x = 26             #click x loc relative to top left of image
username.click_cen_y = 15             #click y loc relative to top left of image
username.img_match = "./img/click_elements/username.png" 

Cadence_Menu = MatchList(cadence_menu)
Cadence_Menu.Add(cadence_menu2)
Cadence_Menu.Add(cadence_menu3)

Capture_Unchecked = MatchList(capture_unchecked)
Capture_Unchecked.Add(capture_unchecked3)
Capture_Unchecked.Add(capture_unchecked2)

Download_Files = MatchList(download_files)
Download_Files.Add(download_files4)
Download_Files.Add(download_files5)
Download_Files.Add(download_files2)
Download_Files.Add(download_files3)

Download_Now = MatchList(download_now)
Download_Now.Add(download_now4)
Download_Now.Add(download_now3)
Download_Now.Add(download_now2)


Login_Button = MatchList(login_button)

Login_Button_Main = MatchList(login_button_main)
Login_Button_Main.Add(login_button_main2)

Recaptcha_Checkbox = MatchList(not_a_robot_empty)
Recaptcha_Checkbox.Add(not_a_robot_empty2)
Recaptcha_Checkbox.Add(not_a_robot_empty3)
Recaptcha_Checkbox.Add(not_a_robot_empty4)
Recaptcha_Checkbox.Add(not_a_robot_empty5)

Password = MatchList(password)

Pcb_Unchecked = MatchList(pcb_unchecked)
Pcb_Unchecked.Add(pcb_unchecked4)
Pcb_Unchecked.Add(pcb_unchecked3)
Pcb_Unchecked.Add(pcb_unchecked2)

Search_Bar = MatchList(search_bar)

Step_Unchecked = MatchList(step_unchecked)
Step_Unchecked.Add(step_unchecked5)
Step_Unchecked.Add(step_unchecked4)
Step_Unchecked.Add(step_unchecked3)
Step_Unchecked.Add(step_unchecked2)

ThreeD_Menu = MatchList(threeD_menu)
ThreeD_Menu.Add(threeD_menu4)
ThreeD_Menu.Add(threeD_menu5)
ThreeD_Menu.Add(threeD_menu2)
ThreeD_Menu.Add(threeD_menu3)

Url_Bar = MatchList(url_bar)
Url_Bar.Add(url_bar3)
Url_Bar.Add(url_bar2)
Url_Bar.Add(url_bar4)
Url_Bar.Add(url_bar5)
