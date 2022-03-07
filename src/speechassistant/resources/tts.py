import logging
import time
import traceback
from pathlib import Path
from threading import Thread

import pyperclip

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


class TTS:

    def __init__(self) -> None:
        self.driver = None
        self.action = None
        self.text_area = None
        self.play_button = None
        self.display = None
        self.to_say = []
        self.stopped = False
        self.is_reading = False
        self.gender = 'male'

    def start(self, gender: str) -> None:
        tts_thread: Thread = Thread(target=self.run(gender))
        tts_thread.daemon = True
        tts_thread.start()

    def run(self, gender: str) -> None:
        logging.info("[ACTION] Load Speechmodule")
        self.display: Display = Display(size=(800, 600))
        self.display.start()
        self.gender: str = gender
        # start browser
        self.__start_driver()

    def __start_driver(self) -> None:
        # toDo: change following path
        # driver_path: str = str(Path(__file__).parent) + '/webdriver/chromedriver'
        driver_path: str = '/home/pi/Desktop/chromedriver'
        print(driver_path)
        self.driver: webdriver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=self.get_opt())
        self.action: ActionChains = ActionChains(self.driver)
        # self.start_vpn()
        time.sleep(2)
        self.get_website_inf()

    def say(self, text: str) -> None:
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
        print(self.text_area)
        self.driver.find_element_by_id('downshift-0-toggle-button').click()
        self.driver.find_element_by_id('downshift-0-item-6').click()

    def select_voice(self, gender):
        if gender == "male":
            voice = 'Dieter'
        else:
            voice = 'Erika'
        elements = self.driver.find_elements_by_class_name('bx--list-box__label')
        for element in elements:
            if element.text == voice:
                element.click()

    def play_audio(self):
        self.play_button.click()

    def get_website_inf(self):
        url: str = 'https://www.ibm.com/demos/live/tts-demo/self-service/home'
        self.driver.get(url)
        self.text_area = self.driver.find_element_by_id('text-area')
        time.sleep(3)
        self.play_button = self.driver.find_element_by_id('btn')
        self.select_german()
        self.select_voice(self.gender)

    def get_opt(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("no-default-browser-check")
        opt.add_argument("no-first-run")
        #relPath = str(Path(__file__).parent) + "/webdriver/"
        #opt.add_extension(relPath + "vpn.crx")
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", chrome_prefs)
        return opt

    def stop(self):
        self.stopped = True
        self.driver.quit()
        self.display.stop()


if __name__ == "__main__":
    tts = TTS()
    tts.start("male")
    time.sleep(3)
    tts.say('Hallo Welt')