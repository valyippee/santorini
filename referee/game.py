from referee.board import Board

COLOURS = "red", "yellow"
NUM_PLAYERS = 2
GAME_NAME = "Santorini"


def play(players):
    """

    Coordinates the game.

    Args:
        players: Contains two PlayerWrapper classes which needs to be initialised

    Returns: A string indicating who won

    """
    game = Game()
    for player, colour in zip(players, COLOURS):
        player.init(colour)
    current_player, next_player = players

    game.initialise_starting_loc(game, current_player, next_player)

    while not game.check_won():
        game.board.display_board()
        print(game.board.players_locations)

        # no available moves for current player
        if not game.check_available_moves(current_player.colour):
            return current_player.colour + " has no available moves. " + next_player.colour + " won!"

        print(current_player.colour + "'s turn")
        player_actions = current_player.action()

        # check if move is valid + referee update if valid
        if len(player_actions) != 3:
            print("Invalid move. Please try again.")
            continue
        if player_actions[0] not in game.board.players_locations or \
                game.board.players_locations[player_actions[0]] != current_player.colour:
            print("You did not select your game piece correctly. Please try again.")
            continue
        if not game.update(player_actions):
            print("Invalid move. Please try again.")
            continue
        # players update
        for player in players:
            player.update(player_actions)

        print("Player's action: move from " + str(player_actions[0]) + " to " + str(player_actions[1]))
        print("Build at " + str(player_actions[2]))

        # check win/draw
        if game.check_won():
            game.board.display_board()
            return current_player.colour + " won!"

        current_player, next_player = next_player, current_player


class Game:
    def __init__(self):
        self.board = Board()

    def update(self, player_actions):
        return self.board.move_and_build(player_actions)

    def update_starting_loc(self, player_colour, starting_loc):
        for location in starting_loc:
            self.board.players_locations[location] = player_colour
            location_level = self.board.board_dict[location][0]
            self.board.board_dict[location] = location_level, player_colour

    def check_won(self):
        for key in self.board.players_locations:
            if self.board.board_dict[key][0] == 3:
                return True
        return False

    def check_available_moves(self, player_colour):
        """
        Returns true if the player has available moves, false otherwise
        """

        for player_location in self.board.players_locations:
            if self.board.players_locations[player_location] == player_colour:
                x_location = player_location[0]
                y_location = player_location[1]
                current_level = self.board.board_dict[player_location][0]
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if (x_location + i, y_location + j) in self.board.board_dict:
                            # check if the adjacent location is available (no other players on it)
                            if self.board.board_dict[(x_location + i, y_location + j)][1] is None:
                                # check if that location is reachable
                                if self.board.board_dict[(x_location + i, y_location + j)][0] - current_level <= 1:
                                    return True
        return False

    def initialise_starting_loc(self, game, current_player, next_player):
        initialised = False
        while not initialised:
            game.board.display_board()
            print(current_player.colour + "'s turn")
            chosen_locations = current_player.choose_starting_loc()
            # check if locations are valid
            if len(chosen_locations) != 2:
                print("Those are not valid locations. Please try again.")
                continue
            if chosen_locations[0] == chosen_locations[1]:
                print("You cannot pick the same location twice. Please try again.")
                continue
            if chosen_locations[0] in game.board.players_locations or \
                    chosen_locations[1] in game.board.players_locations:
                print("The location(s) is/are chosen already. Please try again.")
                continue
            out_of_range = False
            for i in range(2):
                for j in range(2):
                    if chosen_locations[i][j] > 4 or chosen_locations[i][j] < 0:
                        out_of_range = True
            if out_of_range:
                print("Coordinate(s) is/are out of range. Please try again.")
                continue

            # update locations (referee and players)
            game.update_starting_loc(current_player.colour, chosen_locations)
            for player in [current_player, next_player]:
                player.update_starting_loc(current_player.colour, chosen_locations)

            if current_player.colour == "yellow":
                initialised = True

            current_player, next_player = next_player, current_player
