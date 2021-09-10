import math
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class Browser:

    CLICK_DISTANCE = 200

    def __init__(self, full_screen=False):
        options = Options()
        options.headless = False
        self.driver = webdriver.Firefox(executable_path="../res/geckodriver.exe",
                                        service_log_path="nul",
                                        options=options)

        if full_screen:
            self.driver.fullscreen_window()

        self._body: WebElement = None
        self._map_div: WebElement = None
        self._map_img_bg: WebElement = None
        self._map_img_pos: WebElement = None
        self._map_canvas_players: WebElement = None
        self._login_block: WebElement = None
        self._quality_img: WebElement = None

        self._refresh()

    def _refresh(self):
        self.driver.get("http://slither.io/")
        self._get_elements()
        self._modify_game_once()

    def _get_elements(self):
        self._body = self.driver.find_element_by_tag_name("body")
        self._map_div = self.driver.find_element_by_xpath("//div[./canvas[@height='80']]")
        self._map_img_bg, self._map_img_pos = self._map_div.find_elements_by_tag_name("img")
        self._map_canvas_players = self._map_div.find_element_by_tag_name("canvas")

        self._login_block = self.driver.find_element_by_id("login")
        self._quality_img = self.driver.find_element_by_id("grqi")

    def _modify_game_once(self):
        self.driver.execute_script("arguments[0].style.background = 'black'", self._map_div)
        self.driver.execute_script("arguments[0].style.opacity = '0'", self._map_img_bg)
        self.driver.execute_script("arguments[0].style.opacity = '1'", self._map_canvas_players)
        self.driver.execute_script("arguments[0].src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAAMSURBVBhXY3growIAAycBLhVrvukAAAAASUVORK5CYII='", self._map_img_pos)
        self.driver.execute_script("arguments[0].style.margin = '0px'", self._body)

    def _modify_game_after_start(self):
        self.driver.execute_script("arguments[0].style.display = 'none'", self._stats_div)
        elements = self.driver.find_elements_by_xpath("//body/canvas[contains(@class, 'nsi')]/following::div[position() < 5]")
        for element in elements:
            self.driver.execute_script("arguments[0].style.display = 'none'", element)
        self._set_minimap_visibility(False)

    def start_game(self, nick, quality="low"):
        self.set_quality(quality)
        self.driver.find_element_by_id("nick").send_keys(Keys.BACKSPACE*100, nick)
        self.driver.find_element_by_xpath("//div[contains(text(), 'Play')]").click()
        while self.is_login_screen_visible():
            continue
        sleep(6)
        self._modify_game_after_start()

    def move_mouse_to_angle(self, angle):
        w = self.driver.execute_script("return window.innerWidth")
        h = self.driver.execute_script("return window.innerHeight")

        dw = self.CLICK_DISTANCE * math.cos(angle)
        dh = self.CLICK_DISTANCE * math.sin(angle)

        x = w/2 + dw
        y = h/2 + dh

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element_with_offset(self._body, x, y)
        action_chains.perform()

    def set_space_pressed(self, is_pressed):
        self._set_key_pressed(Keys.SPACE, is_pressed)

    def set_left_pressed(self, is_pressed):
        self._set_key_pressed(Keys.ARROW_LEFT, is_pressed)

    def set_right_pressed(self, is_pressed):
        self._set_key_pressed(Keys.ARROW_RIGHT, is_pressed)

    def _set_key_pressed(self, key, is_pressed):
        if is_pressed:
            ActionChains(self.driver).key_down(key).perform()
        else:
            ActionChains(self.driver).key_up(key).perform()

    def is_login_screen_visible(self):
        display = self.driver.execute_script("return arguments[0].style.display", self._login_block)
        return display != "none"

    def get_length(self):
        try:
            text = self.driver.execute_script("return arguments[0].children[0].children[1].innerText", self._stats_div)
            return int(text)
        except NoSuchElementException:
            return None

    def get_position(self):
        try:
            position = self.driver.execute_script("return arguments[0].children[3].innerText", self._stats_div)
            return int(position)
        except NoSuchElementException:
            return None

    def get_players_count(self):
        try:
            players = self.driver.execute_script("return arguments[0].children[5].innerText", self._stats_div)
            return int(players)
        except NoSuchElementException:
            return None

    @property
    def _stats_div(self):
        return self.driver.find_element_by_xpath("//body/div[./span/span[contains(text(), 'Your length')]]")

    def get_quality(self):
        src = self._quality_img.get_property("src")
        return "low" if src == "/s/lowquality.png" else "high"

    def set_quality(self, new_quality):
        current = self.get_quality()
        if current == "low" and new_quality == "high" or current == "high" and new_quality == "low":
            self._quality_img.click()

    def get_minimap_image(self):
        self._set_minimap_visibility(True)
        self._map_canvas_players.screenshot("../res/minimap.png")
        print("save")
        image = self._map_canvas_players.screenshot_as_base64
        self._set_minimap_visibility(False)
        return image

    def get_map_image(self):
        self.driver.save_screenshot("../res/map.png")

    def _set_minimap_visibility(self, visible):
        value = "block" if visible else "none"
        self.driver.execute_script(f"arguments[0].style.display = '{value}'", self._map_div)
