import time

from browser import Browser
import math
from time import sleep

browser = Browser()

while True:
    if browser.is_login_screen_visible():
        browser.start_game("klima7")
        sleep(6)
        browser.get_map_image()

    print(browser.get_length(), browser.get_position(), browser.get_players_count())
    browser.get_minimap_image()

    # sleep()
    # browser.move_mouse_to_angle(0)
    # sleep(2)
    # browser.move_mouse_to_angle(math.pi/2)
    # sleep(2)
    # browser.move_mouse_to_angle(math.pi)
    # sleep(2)
    # browser.move_mouse_to_angle(3.0/2*math.pi)
    # sleep(20)
    # browser.set_space_pressed(True)

