import Agregation
import Element4_2D
import GlobalData
import Grid
import BoundaryConditions


class TransformationJacobian:
    jacobian_matrix = [[0 for _ in range(2)] for _ in range(2)]
    jacobian_inverse = [[0 for _ in range(2)] for _ in range(2)]
    detJ = 0.0

    # jacobian and inverted jacobian calculation
    def solveJacobian(self, i, j, grid, element: Element4_2D.Element4_2D):
        self.jacobian_matrix = [[0 for _ in range(2)] for _ in range(2)]
        for n in range(4):
            self.jacobian_matrix[0][0] += grid.nodes[grid.elements[i].id[n] - 1].x * element.dNdE[j][n]
            self.jacobian_matrix[0][1] += grid.nodes[grid.elements[i].id[n] - 1].y * element.dNdE[j][n]
            self.jacobian_matrix[1][0] += grid.nodes[grid.elements[i].id[n] - 1].x * element.dNdN[j][n]
            self.jacobian_matrix[1][1] += grid.nodes[grid.elements[i].id[n] - 1].y * element.dNdN[j][n]

        self.detJ = abs(self.jacobian_matrix[0][0] * self.jacobian_matrix[1][1] - self.jacobian_matrix[0][1] * self.jacobian_matrix[1][0])
        det_inverse = abs(1 / self.detJ)
        a = [1, 0]
        for n in range(2):
            for m in range(2):
                if n == m:
                    self.jacobian_inverse[n][m] = det_inverse * self.jacobian_matrix[a[m]][a[n]]
                else:
                    self.jacobian_inverse[n][m] = det_inverse * (-1) * self.jacobian_matrix[n][m]


class HMatrix:
    dNdX = []
    dNdY = []

    def __init__(self):
        self.dNdX = [0 for _ in range(4)]
        self.dNdY = [0 for _ in range(4)]

    def count_h_matrix(self, j : int, jacobian_inverse : list, element: Element4_2D.Element4_2D):
        # j : derivative point
        for i in range(4):
            self.dNdX[i] = jacobian_inverse[0][0] * element.dNdE[j][i] + jacobian_inverse[0][1] * element.dNdN[j][i]
            self.dNdY[i] = jacobian_inverse[1][0] * element.dNdE[j][i] + jacobian_inverse[1][1] * element.dNdN[j][i]

    def solve_h_matrix(self, matrix, element : Element4_2D.Element4_2D, jakobian, k): #k is element number in fem grid
        for i in range(4):
            for j in range(4):
                matrix[i][j] += GlobalData.conductivity * (self.dNdX[i] * self.dNdX[j] + self.dNdY[i] *
                                                                      self.dNdY[j]) * element.wages[k] * jakobian.detJ
        # return matrix


class CMatrix:

    def solve_c_matrix(self, matrix, element:Element4_2D.Element4_2D, jacobian: TransformationJacobian, k):
        for i in range(4):
            for j in range(4):
                matrix[i][j] += GlobalData.specific_heat * GlobalData.density * element.N[k][i] * \
                                element.N[k][j] * element.wages[k] * jacobian.detJ


if __name__ == "__main__":
    pass


