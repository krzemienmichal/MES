import math
import Element4_2D
import GlobalData
import Grid
import Parameters
import numpy as np


def count_det_j(grid : Grid.Grid, element: Grid.Grid.elements, f):
    if f == 3:
        det_j = math.sqrt((grid.nodes[element.id[f] - 1].x - grid.nodes[element.id[0] - 1].x) ** 2 +
                          (grid.nodes[element.id[f] - 1].y - grid.nodes[element.id[0] - 1].y) ** 2) / 2 * \
                grid.nodes[element.id[f] - 1].bc * grid.nodes[element.id[0] - 1].bc
    else:
        det_j = math.sqrt((grid.nodes[element.id[f] - 1].x - grid.nodes[element.id[f + 1] - 1].x) ** 2 +
                          (grid.nodes[element.id[f] - 1].y - grid.nodes[
                              element.id[f + 1] - 1].y) ** 2) / 2 * \
                grid.nodes[element.id[f] - 1].bc * grid.nodes[element.id[f + 1] - 1].bc
    return det_j


class BoundaryConditionSolver:
    uni_ele = None
    data = None

    def __init__(self, data: Grid.Grid, element: Element4_2D.Element4_2D):
        self.uni_ele = element
        self.data = data

    def solve_hbc_matrix(self, element: Grid.Grid.elements):
        for i in range(4):
            N = [[0 for _ in range(4)] for _ in range(self.uni_ele.npc)]
            Element4_2D.Element4_2D.count_n_matrix(N, self.uni_ele.borderPoints[i])
            det_j = count_det_j(self.data,element, i)
            for j in range(4):
                tem = [[] for _ in range(self.uni_ele.npc)]
                for k in range(4):
                    for l in range(self.uni_ele.npc):
                        if element.Alpha is not None:
                            tem[l].append(
                                element.Alpha * N[l][j] * N[l][k] * Parameters.Parameters(self.uni_ele.npc).wages[l])
                        else:
                            tem[l].append(
                                GlobalData.ALPHA * N[l][j] * N[l][k] * Parameters.Parameters(self.uni_ele.npc).wages[l])

                for z in range(4):
                    __temp = 0
                    for item in np.array(tem)[:, z]:
                        __temp += item
                    element.Hbc[j][z] += __temp * det_j

    def solve_p_vector(self, element: Grid.Grid.elements):
        for i in range(4):
            N = [[0 for _ in range(4)] for _ in range(self.uni_ele.npc)]
            Element4_2D.Element4_2D.count_n_matrix(N, self.uni_ele.borderPoints[i])
            det_j = count_det_j(self.data, element, i)
            for j in range(4):
                for pc in range(self.uni_ele.npc):
                    if element.Alpha is not None:
                        element.P[j] += element.Alpha * GlobalData.AMBIENT_TEMPERATURE * N[pc][j] * \
                                    Parameters.Parameters(self.uni_ele.npc).wages[pc] * det_j
                    else:
                        element.P[j] += GlobalData.ALPHA * GlobalData.AMBIENT_TEMPERATURE * N[pc][j] * \
                                        Parameters.Parameters(self.uni_ele.npc).wages[pc] * det_j


if __name__ == "__main__":
    pass
