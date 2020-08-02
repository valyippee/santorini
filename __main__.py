from referee.game import play
from referee.player import PlayerWrapper
from referee.options import get_options


def main():

    options = get_options()

    p1 = PlayerWrapper("red", options.player1_loc)
    p2 = PlayerWrapper("yellow", options.player2_loc)
    result = play([p1, p2])
    print(result)


if __name__ == '__main__':
    main()