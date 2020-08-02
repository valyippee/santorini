import random

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
        action_scores = []
        alpha = -math.inf
        beta = math.inf
        for action in self.board.generate_all_actions(self.colour):
            resulting_board = copy.deepcopy(self.board)
            resulting_board.move_and_build(action)
            score = self.minimax(resulting_board, 1, alpha, beta, False)
            action_scores.append((score, action))
        sorted_action_score = sorted(action_scores, reverse=True)

        best_score = sorted_action_score[0][0]
        best_action_list = []
        for i in action_scores:
            if i[0] == best_score:
                best_action_list.append(i)
        print(best_action_list)
        chosen_move = random.choice(best_action_list)
        return chosen_move

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
        if depth == 0 or board.check_won():
            score = board.heuristic(self.colour)
            return score

        if maximizingPlayer:
            max_eval = -math.inf
            for action in board.generate_all_actions(self.colour):
                resulting_board = copy.deepcopy(board)
                resulting_board.move_and_build(action)
                eval = self.minimax(resulting_board, depth - 1, alpha, beta, False)
                max_eval = max(eval, max_eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for action in board.generate_all_actions(self.opp_colour):
                resulting_board = copy.deepcopy(board)
                resulting_board.move_and_build(action)
                eval = self.minimax(resulting_board, depth - 1, alpha, beta, True)
                min_eval = min(eval, min_eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

if __name__ == '__main__':
    player = Player("red")
    player.board.display_board()
    player.board.players_locations = {(1, 1): "red", (3, 3): "red", (1, 2): "yellow", (4, 4): "yellow"}
    print(player.action())