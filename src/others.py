class Controller:

    def __init__(self, game):
        self.game = game

    def play(self):
        ...


class Game:

    def __init__(self):
        self.player = ...
        self.map = ...


class Player:

    def set_angle(self, angle):
        ...

    def turn_left(self):
        ...

    def turn_right(self):
        ...

    def stop_turning(self):
        ...

    def speed_up(self):
        ...

    def slow_down(self):
        ...


class Map:

    def update_image(self, image):
        ...

    def get_player_pos(self):
        ...


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    game = Game()
    controller = Controller(game)
    controller.play()


if __name__ == '__main__':
    main()

# action_chains = ActionChains(driver)
# action_chains.key_down(Keys.ARROW_LEFT)
# action_chains.pause(5)
# action_chains.key_up(Keys.ARROW_LEFT)
# action_chains.perform()
# print("perform finished")

# action_chains = ActionChains(driver)
# action_chains.move_to_element(map_canvas_players)
# action_chains.perform()
