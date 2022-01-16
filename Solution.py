import Element4_2D
import GlobalData
import Grid
import HbcMatrix
import Agregation
from Matrixes import Matrixes, HMatrix, Cmatrix
import numpy as np
import time


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
        self.jacobian = Matrixes()
        self.h_matrix = HMatrix()
        self.c_matrix = Cmatrix()

    def solveProblem(self):
        solve = None
        self.solveMatrixes()
        agg = Agregation.Agregation()
        agg.sumHwithHbc(self.grid)
        iterations = int(GlobalData.simulation_time/GlobalData.simultaion_step_time)
        print(f"it {iterations}")
        for i in range(iterations):
            self.aggregatedH, self.aggregatedC, self.aggregatedSum = agg.aggregateMatrix(grid=self.grid)
            if i == 0:
                self.aggregatedP = agg.aggregatePvector(self.grid, self.aggregatedC,[GlobalData.initial_temperature for _ in range(self.grid.nN)])
            else:
                self.aggregatedP = agg.aggregatePvector(grid, self.aggregatedC, solve)

            # print(self.aggregatedP)
            solve = np.linalg.solve(self.aggregatedSum, self.aggregatedP)
            print(f"\033[38;5;160m {i} \033[38;5;51m \t min: {min(solve): .5f}\t \033[38;5;200m max: {max(solve): .5f} \033[0m")

    def solveMatrixes(self):
        for i in range(self.grid.nE):
            self.grid.elements[i].H = [[0 for _ in range(4)] for _ in range(4)]
            self.grid.elements[i].C = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(pow(self.element.npc, 2)):
                self.jacobian.solveJacobian(i, j, self.grid, self.element)
                self.h_matrix.count_h_matrix(j, self.jacobian.jacobianInverse, self.element)
                self.h_matrix.solve_H_matrix(self.grid.elements[i].H, self.element, self.jacobian, j)
                self.c_matrix.solveCmatrix(self.grid.elements[i].C, self.element, self.jacobian, j)
        a = HbcMatrix.HbcSolver(self.grid, self.npc)
        for i in range(self.grid.nE):
            a.solveHbc(self.grid.elements[i])


def dataLoader(file):
    global a
    nodes_points = []
    elements_ids = []
    boundary_condition = []
    nN = 0
    nE = 0
    with open(file) as data_file:
        data = data_file.readlines()
        GlobalData.simulation_time = int(data[0].split()[1])
        GlobalData.simultaion_step_time = int(data[1].split()[1])
        GlobalData.conductivity = int(data[2].split()[1])
        GlobalData.alpha = int(data[3].split()[1])
        GlobalData.temperature = int(data[4].split()[1])
        GlobalData.initial_temperature = int(data[5].split()[1])
        GlobalData.density = int(data[6].split()[1])
        GlobalData.specific_heat = int(data[7].split()[1])
        nN = int(data[8].split()[2])
        nE = int(data[9].split()[2])
        temp = []
        a = 0
        for i in range(10, len(data)):
            if "*" in data[i]:
                if a == 1:
                    nodes_points = temp
                    temp = []
                if a == 2:
                    elements_ids = temp
                    temp = []
                a += 1
                continue
            if i == len(data)-1:
                boundary_condition = data[i].split()
            else:
                temp.append(data[i].split()[1:])
    data_file.close()

    for i in range(len(boundary_condition)):
        boundary_condition[i] = int(boundary_condition[i].rstrip(","))
    for i in range(len(nodes_points)):
        x,y = nodes_points[i]
        nodes_points[i] = [float(x.rstrip(",")),float(y.rstrip(","))]

    print(len(elements_ids))
    for i in range(len(elements_ids)):
        temp = []
        for id in elements_ids[i]:
            temp.append(int(id.rstrip(",")))
        elements_ids[i] = temp

    return Grid.Grid.load_from_file(Grid.Grid,nN, nE, nodes_points, elements_ids, boundary_condition)


if __name__ == "__main__":
    start_time = time.time()
    npc = 2
    grid = dataLoader("Test2_4_4_MixGrid.txt")
    GlobalData.printGlobalData()
    solution = Solution(npc, grid)
    # solution.grid.print_elements(grid)
    # solution.grid.print_nodes(grid)
    print(solution.grid.nE)
    print(solution.grid.nN)
    # solution.dataLoader("Test1_4_4.txt")
    # solution.grid.print_nodes()
    # print()
    # print()
    # solution.grid.print_elements()
    solution.solveProblem()
    print(f"{time.time()-start_time} s")

