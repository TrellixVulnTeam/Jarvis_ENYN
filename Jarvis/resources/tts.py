import time
import traceback
from pathlib import Path
from threading import Thread

import pyperclip
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Text_to_Speech:

    def __init__(self, ):
        self.driver = None
        self.text_area = None
        self.play_button = None
        self.display = None
        self.to_say = []
        self.stopped = False
        self.is_reading = False
        self.gender = 'male'

    def start(self, gender):
        tts_thread = Thread(target=self.run(gender))
        tts_thread.daemon = True
        tts_thread.start()

    def run(self, gender):
        print("[LOADING] Speechmodule")
        self.display = Display(size=(800, 600))
        self.display.start()
        self.gender = gender
        # start browser
        self.start_driver()

    def say(self, text):
        try:
            # output the entered text as audio
            self.is_reading = True
            self.push_text(text)
            # wait until the text has been changed
            while self.text_area.get_attribute('value') != text:
                time.sleep(0.1)
            time.sleep(0.25)
            self.play_audio()
            # wait until the text starts to say
            while self.state_of_button() == 'creating' or self.state_of_button() == 'waiting':
                time.sleep(0.1)
            # wait until the text was said
            while self.state_of_button() == 'playing':
                time.sleep(0.1)
            self.is_reading = False
        except:
            traceback.print_exc()

    def state_of_button(self):
        if 'M7,28a1,1,0,0,1-1-1V5a1,1,0,0,1,.5-.87,1,1,0,0,1,1,0l19,11a1,1,0,0,1,0,1.74l-19,11A1,1,0,0,1,7,28ZM8,6.73V25.27L24,16Z' in self.play_button.get_attribute(
                'innerHTML'):
            return 'waiting'
        elif 'M24,8V24H8V8H24m0-2H8A2,2,0,0,0,6,8V24a2,2,0,0,0,2,2H24a2,2,0,0,0,2-2V8a2,2,0,0,0-2-2Z' in self.play_button.get_attribute(
                'innerHTML'):
            return 'playing'
        else:
            return 'creating'

    def push_text(self, text):
        self.text_area.clear()
        pyperclip.copy(text)
        self.text_area.send_keys(Keys.CONTROL, 'v')
        # script = "var element = arguments[0], txt = arguments[1]; element.value = txt; element.dispatchEvent(new Event('change'));"
        # self.driver.execute_script(script, self.text_area, text)

    def select_german(self):
        self.driver.find_element_by_id('downshift-0-toggle-button').click()
        # self.driver.find_element_by_xpath("//div[@aria-activedescendant='downshift-0-item-5' and @id='downshift-0-menu']").click()
        # self.driver.find_element_by_xpath("//div[text() = 'German]").click()
        elements = self.driver.find_elements_by_class_name('bx--list-box__label')
        print(elements)
        for element in elements:
            print(element.text)
            if element.text == 'German':
                element.click()

    def select_voice(self, gender):
        if gender == "male":
            voice = 'Dieter'
        else:
            voice = 'Erika'
        self.driver.find_element_by_id('downshift-2-toggle-button').click()
        el = self.driver.find_element_by_xpath(f"//div[contains(text(), '{voice}')]")
        hover = ActionChains(self.driver).move_to_element(el)
        hover.perform()
        el.click()
        # self.driver.find_element_by_xpath(f"//div[@aria-activedescendant='downshift-2-item-{index}']").click()
        """elements = self.driver.find_elements_by_class_name('bx--list-box__label')
        for element in elements:
            if element.text == voice:
                element.click()"""

    def play_audio(self):
        self.play_button.click()

    def start_driver(self):
        driver_Path = str(Path(__file__).parent) + '/webdriver/chromedriver'
        self.driver = webdriver.Chrome(driver_Path, chrome_options=self.get_opt())
        # self.start_vpn()
        self.get_website_inf()

    def get_website_inf(self):
        URL = "https://www.ibm.com/demos/live/tts-demo/self-service/home"
        self.driver.get(URL)
        self.text_area = self.driver.find_element_by_id('text-area')
        time.sleep(1)
        self.play_button = self.driver.find_element_by_id('btn')
        # self.select_german()
        self.select_voice(self.gender)

    def get_opt(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("no-default-browser-check")
        opt.add_argument("no-first-run")
        relPath = str(Path(__file__).parent) + "/webdriver/"
        opt.add_extension(relPath + "vpn.crx")
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", chrome_prefs)
        return opt

    def stop(self):
        self.stopped = True
        self.driver.quit()
        self.display.stop()
