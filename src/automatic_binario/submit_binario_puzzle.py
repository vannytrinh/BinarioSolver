import numpy as np
from binario_solvers import EasyBinarioSolver
from binario_submitters import PuzzleBinarioSubmitter

if __name__ == "__main__":
    API_TOKEN = "API-TOKEN HERE"

    solver = EasyBinarioSolver()
    submitter = PuzzleBinarioSubmitter(API_TOKEN)

    puzzle = "binairo-8x8-easy/"
    rows = 8
    cols = 8

    submitter.run(solver, puzzle, rows, cols)