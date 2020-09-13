import argparse
from src.cubik import Cubik

parser = argparse.ArgumentParser(description="Takes a combination of movement to shuffle a Rubik's cube and solve it")
parser.add_argument("commands", type=str, help="The list of command which must be computed before resolving the Rubik's")
args = parser.parse_args()

cubik = Cubik(args.commands)
cubik.debug()
