class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class AgentBoard:
    BOARD_WIDTH = 5

    def __init__(self):
        """

        Initialises board_dict, a dictionary where the key is (column, row) of the board and
        the value is (levels, player colour) and players_locations, a dictionary to store players' locations,
        where key is (column, row) and value is the player's colour

        """
        self.board_dict = dict()
        for i in range(self.BOARD_WIDTH):
            for j in range(self.BOARD_WIDTH):
                self.board_dict[i, j] = 0, None

        self.players_locations = dict()
        self.last_moved = None

    def move_and_build(self, player_actions):
        """

        Args:
            player_actions: Three tuples. First tuple indicates the player's current location (assume valid),
                            second tuple indicates the location to be moved to,
                            third tuple indicates the location to build on

        Returns: True when the player moved successfully, False otherwise

        """

        current_location = player_actions[0]
        move_location = player_actions[1]
        current_player = self.board_dict[current_location][1]
        # check that move location is within reach of the current position and there is a player at current position
        if abs(current_location[0] - move_location[0]) <= 1 and \
                abs(current_location[1] - move_location[1]) <= 1 and \
                move_location != current_location and \
                current_player is not None:
            # check that the move location is available
            if self.board_dict[move_location][1] is None:
                current_level = self.board_dict[current_location][0]
                new_level = self.board_dict[move_location][0]
                # check that the move location is at most one level higher than the current level and move
                if new_level - current_level <= 1:
                    # check if build action is valid and build OR player won
                    if new_level == 3 or self.build(player_actions):
                        # current_level may change due to build()
                        current_level = self.board_dict[current_location][0]
                        self.board_dict[current_location] = current_level, None
                        self.board_dict[move_location] = new_level, current_player
                        del self.players_locations[current_location]
                        self.players_locations[move_location] = current_player
                        self.last_moved = current_player
                        return True
        return False

    def build(self, player_actions):
        """

        A function that is called by move_and_build(self, player_actions)

        Args:
            player_actions: Three tuples. First tuple indicates the player's current location,
                            second tuple indicates the location to be moved to,
                            third tuple indicates the location to build on

        Returns: True when the player built successfully, False otherwise

        """

        move_location = player_actions[1]
        build_location = player_actions[2]
        Level_before_build = self.board_dict[build_location][0]
        # check if build location is current location (build is valid since player will move away)
        if build_location == player_actions[0]:
            self.board_dict[build_location] = Level_before_build + 1, None
            return True
        # check that build location is within reach of moved to location
        if abs(build_location[0] - move_location[0]) <= 1 and \
                abs(build_location[1] - move_location[1]) <= 1 and \
                move_location != build_location:
            # check that no. of levels is at most 3 at build location
            if self.board_dict[build_location][0] <= 3:
                # check that there are no players at build location and build
                if self.board_dict[build_location][1] is None:
                    self.board_dict[build_location] = Level_before_build + 1, None
                    return True
        return False

    def generate_starting_loc(self):
        loc = []
        for key in self.board_dict.keys():
            if self.board_dict[key][1] is not None:
                continue
            elif 0 < key[0] < 4 and 0 < key[1] < 4:
                loc.append(key)
        return loc

    def generate_surrounding_squares(self, curr_square):
        surrounding_squares = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                square = (curr_square[0] + i, curr_square[1] + j)
                if i == 0 and j == 0:
                    continue
                else:
                    if 0 <= square[0] <= 4:
                        if 0 <= square[1] <= 4:
                            surrounding_squares.append(square)
        return surrounding_squares

    def generate_all_actions(self, colour):
        all_moves = []
        all_actions = []
        player_positions = []
        for key in self.board_dict.keys():
            if self.board_dict[key][1] == colour:
                player_positions.append(key)
        for position in player_positions:
            surrounding_squares = self.generate_surrounding_squares(position)
            for square in surrounding_squares:
                if self.board_dict[square][0] == 4:
                    continue
                if self.board_dict[square][0] <= self.board_dict[position][0] + 1 and self.board_dict[square][1] is None:
                    all_moves.append((position, square))
        for move in all_moves:
            surrounding_squares = self.generate_surrounding_squares(move[1])
            for square in surrounding_squares:
                if move[0] == square:
                    all_actions.append((move[0], move[1], square))
                elif self.board_dict[square][0] == 4 or self.board_dict[square][1] is not None:
                    continue
                else:
                    all_actions.append((move[0], move[1], square))

        return all_actions

    def game_over(self):
        for coord in self.board_dict.keys():
            if self.board_dict[coord][0] == 3:
                if self.board_dict[coord][1] is not None:
                    return True
        return False

    def check_win(self, colour):
        for coord in self.board_dict.keys():
            if self.board_dict[coord][0] == 3:
                if self.board_dict[coord][1] == colour:
                    return True
        return False

    def man_distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def total_man_distance(self):
        red = []
        yellow = []
        total = float('inf')
        for key in self.board_dict.keys():
            if self.board_dict[key] == "red":
                red.append(key)
            else:
                yellow.append(key)
        for coord in red:
            curr = self.man_distance(coord, yellow[0]) + self.man_distance(coord, yellow[1])
            if curr < total:
                total = curr
        return total

    def surrounding_tiles(self, coord):
        directions = [(1, 1), (1, 0), (0, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (0, 1)]
        surrounding = []
        for i in directions:
            coordinate = (coord[0] + i[0], coord[1] + i[1])
            if 0 <= coordinate[0] <= 4 and 0 <= coordinate[1] <= 4:
                surrounding.append(coordinate)
        return surrounding

    def movable_count(self, colour):
        coord = []
        total = 0
        for key in self.board_dict.keys():
            if self.board_dict[key] == colour:
                coord.append(key)
        for i in coord:
            curr_level = self.board_dict[i][0]
            for j in self.surrounding_tiles(i):
                if self.board_dict[j][1] is None and curr_level >= (self.board_dict[j][0] - 1):
                    total += (curr_level ** 2 + self.board_dict[j][0] ** 2)
        return total

    # def breadthFirstSearch(self):
    #     """Search the shallowest nodes in the search tree first."""
    #     myqueue = Queue()
    #     startNode = (problem.getStartState(), '', 0, [])
    #     myqueue.push(startNode)
    #     visited = set()
    #     while myqueue:
    #         node = myqueue.pop()
    #         state, action, cost, path = node
    #         if state not in visited:
    #             visited.add(state)
    #             if problem.isGoalState(state):
    #                 path = path + [(state, action)]
    #                 break
    #             succNodes = problem.expand(state)
    #             for succNode in succNodes:
    #                 succState, succAction, succCost = succNode
    #                 newNode = (succState, succAction, cost + succCost, path + [(state, action)])
    #                 myqueue.push(newNode)
    #     actions = [action[1] for action in path]
    #     del actions[0]
    #     return actions

    def moves_from_winning(self, colour):
        coord = []
        moves_to_win = []

        for key in self.board_dict.keys():
            if self.board_dict[key][1] == colour:
                coord.append(key)

        for i in coord:
            curr_level = self.board_dict[i][0]
            for j in self.surrounding_tiles(i):
                if curr_level == 0:
                    if self.board_dict[j][0] <= 3:
                        moves_to_win.append(5)
                    else:
                        moves_to_win.append(6)
                elif curr_level == 1:
                    if self.board_dict[j][0] <= 2:
                        moves_to_win.append(5 - self.board_dict[j][0])
                    elif self.board_dict[j][0] == 3:
                        moves_to_win.append(4)
                    else:
                        moves_to_win.append(5)
                elif curr_level == 2:
                    if self.board_dict[j][0] == 0:
                        moves_to_win.append(5)
                    elif self.board_dict[j][0] == 1:
                        moves_to_win.append(4)
                    elif self.board_dict[j][0] == 2:
                        moves_to_win.append(2)
                    else:
                        moves_to_win.append(5)

        return min(moves_to_win)


    def heuristic(self, colour):
        opp_level_sum = 0
        my_level_sum = 0
        if colour == "red":
            opp_colour = "yellow"
        else:
            opp_colour = "red"
        if self.check_win(colour):
            return 100000
        elif self.check_win(opp_colour):
            return -100000
        for coord in self.board_dict.keys():
            if self.board_dict[coord][1] == colour:
                my_level_sum += (self.board_dict[coord][0]) ** 2
            if self.board_dict[coord][1] == opp_colour:
                opp_level_sum += (self.board_dict[coord][0]) ** 2
        score = my_level_sum - opp_level_sum + (self.movable_count(colour) - self.movable_count(opp_colour)) * 0.2

        return self.moves_from_winning(opp_colour) - self.moves_from_winning(colour)

    def display_board(self):
        template = """# {}
        #  +-----------+-----------+-----------+-----------+-----------+
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # 4|   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  +-----------+-----------+-----------+-----------+-----------+
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # 3|   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  +-----------+-----------+-----------+-----------+-----------+
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # 2|   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  +-----------+-----------+-----------+-----------+-----------+
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # 1|   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  +-----------+-----------+-----------+-----------+-----------+
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # 0|   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        #  +-----------+-----------+-----------+-----------+-----------+
        # y/x    0           1           2           3           4"""
        cells = []
        coords = [(x, 4 - y, 4 - z) for y in range(5) for z in range(4) for x in range(5)]
        for xy in coords:
            value = self.board_dict[(xy[0], xy[1])]
            if value[1] is not None and value[0] + 1 == xy[2]:
                if value[1] == "red":
                    cells.append("\033[91m  X  \033[0m".center(5))
                if value[1] == "yellow":
                    cells.append("\033[93m  X  \033[0m".center(5))
            else:
                if value[0] == 0:
                    cells.append("     ")
                elif xy[2] <= value[0]:
                    if xy[2] == 4:
                        cells.append("M".center(5))
                    if xy[2] == 3:
                        cells.append('O'.center(5))
                    if xy[2] == 2:
                        cells.append('OOO'.center(5))
                    if xy[2] == 1:
                        cells.append('OOOOO'.center(5))
                else:
                    cells.append("     ")


        print(template.format("", *cells))


if __name__ == '__main__':
    board = AgentBoard()
    board.display_board()
    board.generate_all_actions("red")