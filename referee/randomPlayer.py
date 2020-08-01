import random

from agentBoard import AgentBoard


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.board = AgentBoard()

    def update(self, player_actions):
        self.board.move_and_build(player_actions)

    def action(self):
        all_actions = self.board.generate_all_actions(self.colour)
        action = random.choice(all_actions)
        print(action)
        return action

    def choose_starting_loc(self):
        locs = self.board.generate_starting_loc()
        chosen = random.sample(locs, 2)
        return chosen[0], chosen[1]

    def update_starting_loc(self, player_colour, starting_loc):
        for location in starting_loc:
            self.board.players_locations[location] = player_colour
            location_level = self.board.board_dict[location][0]
            self.board.board_dict[location] = location_level, player_colour