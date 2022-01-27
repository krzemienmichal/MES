import Element4_2D
import GlobalData
import Grid
import BoundaryConditions
import Aggregation
from Matrices import TransformationJacobian, HMatrix, CMatrix
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.collections
import matplotlib.tri as tri
# matplotlib.use("Agg") #uncomment if you want to save to file more than 372 pictures
# testfile = "Podstawa\Test2"

class Solution:
    aggregatedP = []
    aggregatedH = []
    aggregatedC = []
    aggregatedSum = []
    npc = None
    grid = None
    element = None
    jacobian = None
    h_matrix = None
    c_matrix = None

    def __init__(self, npc, grid):
        self.npc = npc
        self.grid = grid
        self.element = Element4_2D.Element4_2D(npc)
        self.jacobian = TransformationJacobian()
        self.h_matrix = HMatrix()
        self.c_matrix = CMatrix()

    def solve_problem(self):
        self.solve_matrices()
        agg = Aggregation.Aggregation()
        agg.sum_H_with_Hbc(self.grid)
        iterations = int(GlobalData.SIMULATION_TIME / GlobalData.SIMULATION_STEP_TIME)
        if self.grid.elements[0].Alpha:
            solve = initTemp(self.grid)
        else:
            solve = [GlobalData.INITIAL_TEMPERATURE for _ in range(self.grid.nN)]

        self.plot_fem_mesh(np.array([self.grid.nodes[x].getPoint() for x in range(self.grid.nN)]),
                           np.array([self.grid.elements[x].getID() for x in range(self.grid.nE)]),
                           solve, 0)

        # f = open(f"E:\Studia\SemestrV\MES\Sprawozdanie\TestySprawozdanie\{testfile}\s.txt","w")
        # f.write(f"Po: {0}s\tmin: {min(solve): .5f}\tmax: {max(solve): .5f}\n")
        print(f"it {iterations}")
        for i in range(iterations):
            self.aggregatedH, self.aggregatedC, self.aggregatedSum = agg.aggregate_matrices(grid=self.grid)
            if i == 0:
                self.aggregatedP = agg.aggregate_p_vector(self.grid, self.aggregatedC,
                                                          solve)
            else:
                self.aggregatedP = agg.aggregate_p_vector(grid, self.aggregatedC, solve)

            solve = np.linalg.solve(self.aggregatedSum, self.aggregatedP)
            print(
                f"\033[38;5;160m Iteracja: {i+1} \033[38;5;51m \t min: {min(solve): .5f}\t \033[38;5;200m max: {max(solve): .5f} \033[0m")

            # f.write(f"Po: {(i+1) * GlobalData.SIMULATION_STEP_TIME}s\tmin: {min(solve): .5f}\tmax: {max(solve): .5f}\n")
            self.plot_fem_mesh(np.array([self.grid.nodes[x].getPoint() for x in range(self.grid.nN)]),
                               np.array([self.grid.elements[x].getID() for x in range(self.grid.nE)]),
                               solve, i)
        # f.close()


    def solve_matrices(self):
        a = BoundaryConditions.BoundaryConditionSolver(self.grid, self.element)
        for i in range(self.grid.nE):
            self.grid.elements[i].H = [[0 for _ in range(4)] for _ in range(4)]
            self.grid.elements[i].C = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(pow(self.element.npc, 2)):
                self.jacobian.solveJacobian(i, j, self.grid, self.element)
                self.h_matrix.count_h_matrix(j, self.jacobian.jacobian_inverse, self.element)
                self.h_matrix.solve_h_matrix(self.grid.elements[i], self.element, self.jacobian, j)
                self.c_matrix.solve_c_matrix(self.grid.elements[i], self.element, self.jacobian, j)
            a.solve_hbc_matrix(self.grid.elements[i])
            a.solve_p_vector(self.grid.elements[i])

    def quads_to_tris(self, quads):
        tris = [[None for _ in range(3)] for _ in range(2 * len(quads))]
        for i in range(len(quads)):
            j = 2 * i
            n0 = quads[i][0]
            n1 = quads[i][1]
            n2 = quads[i][2]
            n3 = quads[i][3]
            tris[j][0] = n0
            tris[j][1] = n1
            tris[j][2] = n2
            tris[j + 1][0] = n2
            tris[j + 1][1] = n3
            tris[j + 1][2] = n0
        return tris

    def plot_fem_mesh(self, nodes, elements, nodal_values, i):
        x = None
        y = None
        for element in elements:
            x = [nodes[element[i] - 1][0] for i in range(len(element))]
            y = [nodes[element[i] - 1][1] for i in range(len(element))]
            plt.fill(x, y, edgecolor='black', fill=False)

        elements_all_tris = self.quads_to_tris(elements)

        triangulation = tri.Triangulation(nodes[:, 0], nodes[:, 1], elements_all_tris)

        if GlobalData.AMBIENT_TEMPERATURE < GlobalData.INITIAL_TEMPERATURE:
            plt.tricontourf(triangulation, nodal_values,
                            levels=np.linspace(GlobalData.AMBIENT_TEMPERATURE, GlobalData.INITIAL_TEMPERATURE, 11),
                            cmap="inferno")
        else:
            plt.tricontourf(triangulation, nodal_values,
                            levels=np.linspace(GlobalData.INITIAL_TEMPERATURE, GlobalData.AMBIENT_TEMPERATURE, 11),
                            cmap="inferno")
        # show
        plt.colorbar()
        plt.axis('equal')
        plt.show()
        # plt.savefig(f"E:\Studia\SemestrV\MES\Sprawozdanie\TestySprawozdanie\{testfile}\Image{i}.png")
        plt.close()


def load_data(file):
    nodes_points = []
    elements_ids = []
    boundary_condition = []
    nN = 0
    nE = 0
    with open(file) as data_file:
        data = data_file.readlines()
        GlobalData.SIMULATION_TIME = int(data[0].split()[1])
        GlobalData.SIMULATION_STEP_TIME = int(data[1].split()[1])
        GlobalData.CONDUCTIVITY = float(data[2].split()[1])
        GlobalData.ALPHA = float(data[3].split()[1])
        GlobalData.AMBIENT_TEMPERATURE = int(data[4].split()[1])
        GlobalData.INITIAL_TEMPERATURE = int(data[5].split()[1])
        GlobalData.DENSITY = int(data[6].split()[1])
        GlobalData.SPECIFIC_HEAT = int(data[7].split()[1])
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
            if i == len(data) - 1:
                boundary_condition = data[i].split()
            else:
                temp.append(data[i].split()[1:])
    data_file.close()

    for i in range(len(boundary_condition)):
        boundary_condition[i] = int(boundary_condition[i].rstrip(","))
    for i in range(len(nodes_points)):
        x, y = nodes_points[i]
        nodes_points[i] = [float(x.rstrip(",")), float(y.rstrip(","))]
    elements_data = []
    for i in range(len(elements_ids)):
        temp = []
        data = []
        for index in elements_ids[i][0:4]:
            index = index.strip(" ")
            index = index.lstrip(",")
            temp.append(int(index.rstrip(",")))
            # print(temp)
        for __data in elements_ids[i][4:]:
            data.append(float(__data.rstrip(",")))
            # print(data)
        if data:
            elements_data.append(data)
        elements_ids[i] = temp
    _grid = Grid.Grid(0.1, 0.1, 4, 4)
    if elements_data:
        # print(elements_data)
        _grid.load_from_file_with_data(nN, nE, nodes_points, elements_ids, boundary_condition, elements_data)
    else:
        _grid.load_from_file(nN, nE, nodes_points, elements_ids, boundary_condition)
    return _grid


def initTemp(grid):
    node_temp = [0 for _ in range(grid.nN)]
    water_nodes = []
    other_nodes = []
    for el in grid.elements:
        if el.Density == 997:
            for id in el.id:
                water_nodes.append(id-1)
        else:
            for id in el.id:
                other_nodes.append(id-1)

    for id in other_nodes:
        node_temp[id] = 20

    for id in water_nodes:
        node_temp[id] = 100
    return node_temp


if __name__ == "__main__":
    start_time = time.time()
    npc = 4
    grid = load_data("SymulacjaArgonWoda.txt")
    solution = Solution(npc, grid)
    solution.solve_problem()
    print(f"{time.time() - start_time} s")
