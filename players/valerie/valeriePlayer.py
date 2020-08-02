from players.valerie.agentBoard import AgentBoard
import math
import copy

class Player:
    def __init__(self, colour):
        self.colour = colour
        if colour == "red":
            self.opp_colour = "yellow"
        else:
            self.opp_colour = "red"
        self.board = AgentBoard()

    def update(self, player_actions):
        self.board.move_and_build(player_actions)

    def update_starting_loc(self, player_colour, starting_loc):
        for location in starting_loc:
            self.board.players_locations[location] = player_colour
            location_level = self.board.board_dict[location][0]
            self.board.board_dict[location] = location_level, player_colour

    def action(self):
        chosen_move = input("Please enter move: ")
        try:
            move_list = chosen_move.split(" ")
            for i in range(len(move_list)):
                move_list[i] = int(move_list[i])
            return (move_list[0], move_list[1]), (move_list[2], move_list[3]), (move_list[4], move_list[5])
        except:
            return 0,

    def choose_starting_loc(self):
        chosen_move = input("Please enter starting locations: ")
        try:
            move_list = chosen_move.split(" ")
            for i in range(len(move_list)):
                move_list[i] = int(move_list[i])
            return (move_list[0], move_list[1]), (move_list[2], move_list[3])
        except:
            return 0,

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.game_over():
            score = board.heuristic(self.colour)
            return score

        if maximizingPlayer:
            max_eval = -math.inf
            for action in board.valid_moves():
                resulting_board = copy.deepcopy(board)
                resulting_board.input_piece(self.colour, action)
                eval = self.minimax(resulting_board, depth - 1, alpha, beta, False)
                max_eval = max(eval, max_eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for action in board.valid_moves():
                resulting_board = copy.deepcopy(board)
                resulting_board.input_piece(self.opp_colour, action)
                eval = self.minimax(resulting_board, depth - 1, alpha, beta, True)
                min_eval = min(eval, min_eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval