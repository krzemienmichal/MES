import Agregation
import Element4_2D
import GlobalData
import Grid
import HbcMatrix


class Matrixes:
    jacobian = [[0 for _ in range(2)] for _ in range(2)]
    jacobianInverse = [[0 for _ in range(2)] for _ in range(2)]
    detJ = 0

    # jacobian and inverted jacobian calculation
    def solveJacobian(self, i, j, grid, element: Element4_2D.Element4_2D):
        self.jacobian = [[0 for _ in range(2)] for _ in range(2)]
        for n in range(4): #
            self.jacobian[0][0] += grid.nodes[grid.elements[i].id[n]-1].x * element.dNdE[j][n]
            self.jacobian[0][1] += grid.nodes[grid.elements[i].id[n]-1].y * element.dNdE[j][n]
            self.jacobian[1][0] += grid.nodes[grid.elements[i].id[n]-1].x * element.dNdN[j][n]
            self.jacobian[1][1] += grid.nodes[grid.elements[i].id[n]-1].y * element.dNdN[j][n]

        self.detJ = abs(self.jacobian[0][0] * self.jacobian[1][1] - self.jacobian[0][1] * self.jacobian[1][0])
        det = abs(1 / self.detJ)
        a = [1, 0]
        for n in range(2):
            for m in range(2):
                if n == m:
                    self.jacobianInverse[n][m] = det * self.jacobian[a[m]][a[n]]
                else:
                    self.jacobianInverse[n][m] = det * (-1) * self.jacobian[n][m]


class HMatrix:
    dNdX = []
    dNdY = []
    # dNdXT = []
    # dNdYT = []

    def __init__(self):
        self.dNdX = [0 for _ in range(4)]
        self.dNdY = [0 for _ in range(4)]
        self.dNdXT = [[0] for _ in range(4)]
        self.dNdYT = [[0] for _ in range(4)]

    def count_h_matrix(self, j, jacobianInverse, element: Element4_2D.Element4_2D):
        for i in range(4):
            self.dNdX[i] = jacobianInverse[0][0] * element.dNdE[j][i] + jacobianInverse[0][1] * element.dNdN[j][i]
            self.dNdY[i] = jacobianInverse[1][0] * element.dNdE[j][i] + jacobianInverse[1][1] * element.dNdN[j][i]

    # def matrix_transpose(self):
    #     for i in range(4):
    #         self.dNdXT[i][0] = self.dNdX[i]
    #         self.dNdYT[i][0] = self.dNdY[i]

    def solve_H_matrix(self, matrix, element:Element4_2D.Element4_2D, jakobian, k): #k is element number in fem grid
        # self.matrix_transpose()
        # temp2 = []
        # for i in range(4):
        #     tmp = []
        #     for j in range(4):
        #         temp = GlobalData.GlobalData.conductivity * (self.dNdX[i] * self.dNdXT[j][0] + self.dNdY[i] * self.dNdYT[j][0]) * element.wages[k] * jakobian.detJ
        #         tmp.append(temp)
        #     temp2.append(tmp)
        # for item, i in zip(temp2,range(4)):
        #     for j in range(len(item)):
        #         matrix[i][j] += item[j]

        for i in range(4):
            for j in range(4):
                matrix[i][j] += GlobalData.conductivity * (self.dNdX[i] * self.dNdX[j] + self.dNdY[i] *
                                                                      self.dNdY[j]) * element.wages[k] * jakobian.detJ
        return matrix


class Cmatrix:
    def solveCmatrix(self, matrix, element:Element4_2D.Element4_2D, jacobian, k):
        for i in range(4):
            for j in range(4):
                matrix[i][j] += GlobalData.specific_heat * GlobalData.density * element.N[k][i] * \
                                element.N[k][j] * element.wages[k] * jacobian.detJ


if __name__ == "__main__":
    pass


