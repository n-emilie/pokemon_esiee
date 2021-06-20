# -*- coding: mbcs -*-
from . import move
import pandas as pd
import os
import inspect

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
f = pd.read_csv(os.path.join(scriptDIR, 'poke_abilitys.csv'), ';')

ALL_MOVES: dict[str: move.Move] = {}


def loadmoves():
    global ALL_MOVES

    for i in range(0, 122):
        t = f.loc[i]
        test = open(os.path.join(scriptDIR, 'loadmoves.py'), 'a')
        # print(t[0])
        ALL_MOVES[f"{t[0]}"] = move.Move(f"{t[1]}", f"{t[2]}", f"{t[3]}", f"{t[4]}", int(t[5]), int(t[6]), float(t[7]), float(t[8]))

        test.close()


# loadmoves()
# # print(ALL_MOVES)
# print(ALL_MOVES["griffe"])

def get_Move(name: str) -> move.Move:
    global ALL_MOVES
    return ALL_MOVES[name]





