import random
import math
import copy

from players.korkor.agentBoard import AgentBoard


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

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.game_over():
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

    def action(self):
        all_actions = self.board.generate_all_actions(self.colour)
        depth = 2
        action_score = []
        alpha = -math.inf
        # alpha = (-math.inf, -math.inf)
        beta = math.inf
        # beta = (math.inf, math.inf)
        for action in all_actions:
            resulting_board = copy.deepcopy(self.board)
            resulting_board.move_and_build(action)
            if resulting_board.check_win(self.colour):
                return action
            score = self.minimax(resulting_board, depth, alpha, beta, False)
            action_score.append((score, action))
        sorted_action_score = sorted(action_score, reverse=True)

        best_action = sorted_action_score[0]
        best_action_list = []
        for i in action_score:
            if i[0] == best_action[0]:
                best_action_list.append(i)
        print(best_action_list)
        chosen_move = random.choice(best_action_list)

        return chosen_move[1]

    def choose_starting_loc(self):
        locs = self.board.generate_starting_loc()
        chosen = random.sample(locs, 2)
        return chosen[0], chosen[1]

    def update_starting_loc(self, player_colour, starting_loc):
        for location in starting_loc:
            self.board.players_locations[location] = player_colour
            location_level = self.board.board_dict[location][0]
            self.board.board_dict[location] = location_level, player_colour