from santorini import board

COLOURS = "red", "yellow"
NUM_PLAYERS = 2
GAME_NAME = "Santorini"


def play(players):
    """

    Coordinates the game.

    Args:
        players: Contains two PlayerWrapper classes which needs to be initialised

    Returns: A string indicating who won/ a tie

    """
    game = Game()
    for player, colour in zip(players, COLOURS):
        player.init(colour)
    current_player, next_player = players
    while not game.check_won():
        game.board.display_board()
        print(current_player.colour + "'s turn")
        player_actions = current_player.action()
        # referee update
        if not game.update(player_actions):
            print("That is not a valid move. Please try again.")
            continue
        # players update
        for player in players:
            player.update(player_actions)
        # check win/draw
        if game.check_won():
            game.board.display_board()
            return current_player.colour + " won!"
        # TODO: check if there is a tie

        current_player, next_player = next_player, current_player


class Game:
    def __init__(self):
        self.board = board.Board()

    def update(self, player_actions):
        return self.board.move_and_build(player_actions)

    def check_won(self):
        for key in self.board.players_locations:
            if self.board.board_dict[key][0] == 3:
                return True
        return False
