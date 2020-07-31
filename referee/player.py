import importlib


class PlayerWrapper:
    def __init__(self, name, player_location):
        self.name = name
        self.Player = self.load_class(player_location)

    def init(self, colour):
        self.colour = colour
        self.player = self.Player(colour)

    def load_class(self, player_location):
        package_name, class_name = player_location
        module = importlib.import_module(package_name)
        player_class = getattr(module, class_name)
        return player_class

    def action(self):
        player_actions = self.player.action()
        return player_actions

    def update(self, player_actions):
        self.player.update(player_actions)