import Element4_2D
import GlobalData
import Grid
import HbcMatrix
import Agregation
from Matrixes import Jacobian, HMatrix, Cmatrix
import numpy as np


class Solution:
    aggregatedP = []
    aggregatedH = []
    aggregatedC = []
    aggregatedSum = []
    npc = None
    grid = None
    element = None
    jacobian= None
    h_matrix = None
    c_matrix = None
    def __init__(self, npc, grid):
        self.npc = npc
        self.grid = grid
        self.element = Element4_2D.Element4_2D(npc)
        self.jacobian = Jacobian()
        self.h_matrix = HMatrix()
        self.c_matrix = Cmatrix()

    def solveProblem(self):
        solve = None
        self.solveMatrixes()
        agg = Agregation.Agregation()
        agg.sumHwithHbc(self.grid)

        for i in range(GlobalData.GlobalData.iterations):
            if i == 0:
                self.aggregatedH, self.aggregatedC, self.aggregatedSum = agg.aggregateMatrix(grid=self.grid)
                self.aggregatedP = agg.aggregatePvector(self.grid, self.aggregatedC,[100 for _ in range(self.grid.nN)])
                print(self.aggregatedP)
                print()
            else:
                self.aggregatedP = agg.aggregatePvector(grid, self.aggregatedC, solve)

            solve = np.linalg.solve(self.aggregatedSum, self.aggregatedP)
            print(f"\033[38;5;160m {i} \033[38;5;51m \t min: {min(solve): .5f}\t \033[38;5;200m max: {max(solve): .5f} \033[0m")

    def solveMatrixes(self):
        for i in range(self.grid.nE):
            self.grid.elements[i].H = [[0 for _ in range(4)] for _ in range(4)]
            self.grid.elements[i].C = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(pow(self.element.npc, 2)):
                self.jacobian.solveJacobian(0, j, self.grid, self.element)
                self.h_matrix.count_h_matrix(j, self.jacobian.jacobianInverse, self.element)
                self.grid.elements[i].H = self.h_matrix.solve_H_matrix(self.grid.elements[i].H, self.element, self.jacobian, j)
                self.grid.elements[i].C = self.c_matrix.solveCmatrix(self.grid.elements[i].C, self.element, self.jacobian, j)
        a = HbcMatrix.HbcSolver(self.grid, self.npc)
        for i in range(self.grid.nE):
            a.solveHbc(self.grid.elements[i])


if __name__ == "__main__":
    npc = 2
    grid = Grid.Grid(0.1, 0.1, 4, 4)
    solution = Solution(npc, grid)
    solution.solveProblem()

