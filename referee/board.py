class Board:
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
                if (i, j) == (2, 2):
                    self.board_dict[i, j] = 3, "red"
                else:
                    self.board_dict[i, j] = 0, None

        self.players_locations = dict()

    def move_and_build(self, player_actions):
        """

        Args:
            player_actions: Two tuples. First tuple indicates the player's current location,
                            second tuple indicates the location to be moved to,
                            third tuple indicates the location to build on

        Returns: True when the player moved successfully, False otherwise

        """

        current_location = player_actions[0]
        move_location = player_actions[1]
        current_player = self.board_dict[current_location][1]
        # check that current_location points to a valid player's location
        if current_location in self.players_locations:
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
                    if new_level - current_level < 1:
                        # check if build action is valid and build OR player won
                        if self.build(player_actions) or new_level == 3:
                            self.board_dict[current_location] = current_level, None
                            self.board_dict[move_location] = new_level, current_player
                            return True
        return False

    def build(self, player_actions):
        """

        A function that is called by move_and_build(self, player_actions)

        Args:
            player_actions: Two tuples. First tuple indicates the player's current location,
                            second tuple indicates the location to be moved to,
                            third tuple indicates the location to build on

        Returns: True when the player built successfully, False otherwise

        """

        move_location = player_actions[1]
        build_location = player_actions[2]
        # check that build location is within reach of moved to location
        if abs(build_location[0] - move_location[0]) <= 1 and \
                abs(build_location[1] - move_location[1]) <= 1 and \
                move_location != build_location:
            # check that no. of levels is at most 3 at build location
            if self.board_dict[build_location][0] <= 3:
                # check that there are no players at build location and build
                if self.board_dict[build_location][1] is None:
                    current_level = self.board_dict[build_location][0]
                    self.board_dict[build_location] = current_level + 1, None
                    return True
        return False

    def display_board(self):
        template = """# {}
        # +-----------+-----------+-----------+-----------+-----------+
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # +-----------+-----------+-----------+-----------+-----------+
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # +-----------+-----------+-----------+-----------+-----------+
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # +-----------+-----------+-----------+-----------+-----------+
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # +-----------+-----------+-----------+-----------+-----------+
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # |   {:}   |   {:}   |   {:}   |   {:}   |   {:}   |
        # +-----------+-----------+-----------+-----------+-----------+"""
        cells = []
        coords = [(x, 4 - y, 4 - z) for y in range(5) for z in range(4) for x in range(5)]
        print(cells)
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
    board = Board()
    board.display_board()