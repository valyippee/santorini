from board import Board


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.board = Board()

    def update(self, player_actions):
        self.board.move_and_build(player_actions)

    def action(self):
        chosen_move = input("Please enter move: ")
        move_list = chosen_move.split(" ")
        for i in range(len(move_list)):
            move_list[i] = int(move_list[i])
        return (move_list[0], move_list[1]), (move_list[2], move_list[3]), (move_list[4], move_list[5])

    def choose_starting_loc(self):
        chosen_move = input("Please enter starting locations: ")
        move_list = chosen_move.split(" ")
        for i in range(len(move_list)):
            move_list[i] = int(move_list[i])
        return (move_list[0], move_list[1]), (move_list[2], move_list[3])

    def update_starting_loc(self, player_colour, starting_loc):
        for location in starting_loc:
            self.board.players_locations[location] = player_colour
            location_level = self.board.board_dict[location][0]
            self.board.board_dict[location] = location_level, player_colour
