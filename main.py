import argparse
from src.cubik import Cubik
from src.solver import Solver

parser = argparse.ArgumentParser(description="Takes a combination of movement to shuffle a Rubik's cube and solve it")
parser.add_argument("commands", type=str, help="The list of command which must be computed before resolving the Rubik's")
parser.add_argument("--verbosity", help="Increase the amount of information during the solving process", action="store_true")
args = parser.parse_args()

cubik = Cubik()
solver = Solver(cubik, args.commands, args.verbosity)
print(solver.solve())