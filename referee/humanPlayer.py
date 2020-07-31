from board import Board


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.board = Board()

    def update(self, player_actions):
        self.board.move_and_build(player_actions)

    def action(self):
        chosen_move = input("Please enter move: ")
        return chosen_move

    def init_starting_loc(self):
        chosen_move = input("Please enter starting locations: ")
        return chosen_move
