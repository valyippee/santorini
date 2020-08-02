import argparse
from referee.game import GAME_NAME, NUM_PLAYERS, COLOURS

DESCRIP = \
f"conducts a game of {GAME_NAME} between {NUM_PLAYERS} Player classes"

def get_options():
    """
    Parse and return command-line arguments
    """

    parser = parser = argparse.ArgumentParser(description=DESCRIP)

    positionals = parser.add_argument_group(
        title="player package and class specifications (positional arguments)")
    for num, col in enumerate(COLOURS, 1):
        positionals.add_argument(f"player{num}_loc", metavar=col, action=PackageSpecAction,
                                 help=f"location of player {col}'s class")

    args = parser.parse_args()

    return args


class PackageSpecAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pkg_spec = values

        # detect alternative class:
        if ":" in pkg_spec:
            pkg, cls = pkg_spec.split(':', maxsplit=1)
        else:
            pkg = pkg_spec
            cls = "Player"

        # try to convert path to module name
        mod = pkg.strip("/\\").replace("/", ".").replace("\\", ".")
        if mod.endswith(".py"):  # NOTE: Assumes submodule is not named `py`.
            mod = mod[:-3]

        # save the result in the arguments namespace as a tuple
        setattr(namespace, self.dest, (mod, cls))