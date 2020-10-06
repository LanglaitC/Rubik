import argparse
from src.cubik import Cubik
from src.solver import Solver
from tqdm import tqdm
import pandas as pd
import time

def solveRubik(commands, random_commands_number, visual=False, verbosity=False):
    cubik = Cubik(list(range(20)) + 20 * [0], [], True)
    solver = Solver(cubik, commands, verbosity, random_commands_number)
    if commands is None:
        print("Initial commands : {}".format(solver.command_string))
    commands = solver.command_string
    solution = solver.solve()
    if (visual):
        commands = solver.parseCommands("{} {}".format(commands, solution))
        for commandIdx, command in enumerate(commands):
            cubik.rotate(command[0], command[1], command[2])
            print('{}: {} ------------------'.format(commandIdx, solver.moveToMoveString(command)))
            cubik.debug()
    return solution

def getStats(number_of_moves):
    results = {
        'time': [],
        'solution_length': [],
    }
    for _ in tqdm(range(20)):
        startTime = time.time()
        cubik = Cubik()
        solver = Solver(cubik, None, False, number_of_moves)
        solution = solver.solve()
        results['time'].append(time.time() - startTime)
        results['solution_length'].append(len(solution.split(' ')))
    print(pd.DataFrame(results).describe())
    return

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Takes a combination of movement to shuffle a Rubik's cube and solve it. If you give no input a random combination of 30 moves will be created")
    parser.add_argument("commands", nargs='?', type=str, help="The list of command which must be computed before resolving the Rubik's")
    parser.add_argument("--verbosity", help="Increase the amount of information during the solving process", action="store_true")
    parser.add_argument("--visual", help="Shows the states of the cube during the scramble and after the solving", action="store_true")
    parser.add_argument("--stats", help="Shows the statistics of the cube solving process", action="store_true")
    parser.add_argument("--generate", help="Number of commands needed to generate random combination of moves", type=int, default=30)
    args = parser.parse_args()

    try:
        if (args.stats):
            getStats(args.generate)
        else:
            print(solveRubik(args.commands, args.generate, args.visual, args.verbosity))
    except Exception as e:
        print(e)
