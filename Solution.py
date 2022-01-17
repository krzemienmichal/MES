import Element4_2D
import GlobalData
import Grid
import BoundaryConditions
import Agregation
from Matrices import TransformationJacobian, HMatrix, CMatrix
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.collections
import matplotlib.tri as tri


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
        self.jacobian = TransformationJacobian()
        self.h_matrix = HMatrix()
        self.c_matrix = CMatrix()

    def solve_problem(self):
        solve = None
        self.solve_matrices()
        agg = Agregation.Agregation()
        agg.sumHwithHbc(self.grid)
        iterations = int(GlobalData.simulation_time/GlobalData.simultaion_step_time)

        print()
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

        self.plot_fem_mesh(np.array([self.grid.nodes[x].getPoint() for x in range(self.grid.nN)]),
                          np.array([self.grid.elements[x].getID() for x in range(self.grid.nE)]),
                          solve)

    def solve_matrices(self):
        a = BoundaryConditions.BoundaryConditionSolver(self.grid, self.element)
        for i in range(self.grid.nE):
            self.grid.elements[i].H = [[0 for _ in range(4)] for _ in range(4)]
            self.grid.elements[i].C = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(pow(self.element.npc, 2)):
                self.jacobian.solveJacobian(i, j, self.grid, self.element)
                self.h_matrix.count_h_matrix(j, self.jacobian.jacobian_inverse, self.element)
                self.h_matrix.solve_h_matrix(self.grid.elements[i].H, self.element, self.jacobian, j)
                self.c_matrix.solve_c_matrix(self.grid.elements[i].C, self.element, self.jacobian, j)
            a.solve_hbc_matrix(self.grid.elements[i])
            a.solve_p_vector(self.grid.elements[i])

    # def showMeshPlot(self ,nodes, elements, values):
    #     print(nodes)
    #     print(elements)
    #     y = nodes[:, 0]
    #     z = nodes[:, 1]
    #
    #     def quatplot(y, z, quatrangles, values, ax=None, **kwargs):
    #         if not ax: ax = plt.gca()
    #         yz = np.c_[y, z]
    #         verts = yz[quatrangles]
    #         pc = matplotlib.collections.PolyCollection(verts, **kwargs)
    #         pc.set_array(values)
    #         ax.add_collection(pc)
    #         ax.autoscale()
    #         return pc
    #
    #     fig, ax = plt.subplots()
    #     ax.set_aspect('equal')
    #
    #     pc = quatplot(y, z, np.asarray(elements), values, ax=ax,
    #                   edgecolor="black", linewidth=0.1, cmap="rainbow")
    #     fig.colorbar(pc, ax=ax)
    #     ax.plot(y, z, linewidth=0.01, marker="o",markersize=0.1, ls="", color="black")
    #
    #     ax.set(title='This is the plot for: quad', xlabel='Y Axis', ylabel='Z Axis')
    #
    #     plt.show()

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

    # plots a finite element mesh
    def plot_fem_mesh(self, nodes, elements, nodal_values):
        for element in elements:
            x = [nodes[element[i]-1][0] for i in range(len(element))]
            y = [nodes[element[i]-1][1] for i in range(len(element))]
            plt.fill(x, y, edgecolor='black', fill=False)

    # convert all elements into triangles
        elements_all_tris = self.quads_to_tris(elements)

        # create an unstructured triangular grid instance
        triangulation = tri.Triangulation(nodes[:, 0], nodes[:, 1], elements_all_tris)

        # plot the contours
        plt.tricontourf(triangulation, nodal_values, cmap="rainbow")

        # show
        plt.colorbar()
        plt.axis('equal')
        plt.show()


def dataLoader(file):
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
        x, y = nodes_points[i]
        nodes_points[i] = [float(x.rstrip(",")),float(y.rstrip(","))]

    for i in range(len(elements_ids)):
        temp = []
        for index in elements_ids[i]:
            temp.append(int(index.rstrip(",")))
        elements_ids[i] = temp
    _grid = Grid.Grid(0.1,0.1,4,4)
    _grid.load_from_file(nN, nE, nodes_points, elements_ids, boundary_condition)
    return _grid


if __name__ == "__main__":
    start_time = time.time()
    npc = 4
    grid = dataLoader("Test1_4_4.txt")
    GlobalData.printGlobalData()
    solution = Solution(npc, grid)
    # print(solution.grid.nE)
    # print(solution.grid.nN)
    solution.solve_problem()
    # solution.grid.print_nodes()
    print(f"{time.time()-start_time} s")

