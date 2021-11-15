import Element
import Grid


class Jacobian:
    jacobian = [[0 for _ in range(2)] for _ in range(2)]
    jacobianInverse = [[0 for _ in range(2)] for _ in range(2)]
    detJ = 0

    # def __init__(self, npc):
    #     self.element = Element.Element4_2D(npc)
    #     self.grid = Grid.Grid()

    def solveJacobian(self, i, j, grid, element: Element.Element4_2D):
        self.jacobian = [[0 for _ in range(2)] for _ in range(2)]
        for n in range(4):
            # self.jacobian[0][0] += grid[n][0] * element.dNdE[j][n] #this 4 lines are saved for now because they are important for my FEM course
            # self.jacobian[0][1] += grid[n][1] * element.dNdE[j][n]
            # self.jacobian[1][0] += grid[n][0] * element.dNdN[j][n]
            # self.jacobian[1][1] += grid[n][1] * element.dNdN[j][n]

            self.jacobian[0][0] += grid.nodes[grid.elements[i].id[n]-1].x * element.dNdE[j][n]
            self.jacobian[0][1] += grid.nodes[grid.elements[i].id[n]-1].y * element.dNdE[j][n]
            self.jacobian[1][0] += grid.nodes[grid.elements[i].id[n]-1].x * element.dNdN[j][n]
            self.jacobian[1][1] += grid.nodes[grid.elements[i].id[n]-1].y * element.dNdN[j][n]

        self.detJ = self.jacobian[0][0] * self.jacobian[1][1] - self.jacobian[0][1] * self.jacobian[1][0]
        det = 1 / self.detJ
        # temp = self.jacobian[0][0]
        # self.jacobian[0][0] = self.jacobian[1][1]
        # self.jacobian[1][1] = temp
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
    dNdXT = []
    dNdYT = []

    def __init__(self, npc):
        self.dNdX = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.dNdY = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.dNdXT = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.dNdYT = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]

    def count_h_matrix(self, j, jacobianInverse, element: Element.Element4_2D):
        for i in range(4):
            self.dNdX[j][i] = jacobianInverse[0][0] * element.dNdE[j][i] + jacobianInverse[0][1] * element.dNdN[j][i]
            self.dNdY[j][i] = jacobianInverse[1][0] * element.dNdE[j][i] + jacobianInverse[1][1] * element.dNdN[j][i]

    def matrix_transpose(self):
        for i in range(4):
            for j in range(4):
                self.dNdXT[j][i] = self.dNdX[i][j]
                self.dNdYT[j][i] = self.dNdY[i][j]

    def solve_H_matrix(self, npc):
        self.matrix_transpose()
        raw_h_matrix = []
        a = 0
        b = 0
        temp2 = []
        for i in range(pow(npc, 4)):
            tmp = []
            for j in range(4):
                temp = 30 * (hmatrix.dNdX[a][b] * hmatrix.dNdXT[j][a] + hmatrix.dNdY[a][b] * hmatrix.dNdYT[j][
                    a]) * jakobian.detJ
                tmp.append(temp)
            temp2.append(tmp)
            b += 1
            if b > 3:
                b = 0
                a += 1
                raw_h_matrix.append(temp2)
                temp2 = []
        hfinal = [[0 for _ in range(4)] for _ in range(4)]
        for item in raw_h_matrix:
            for i in range(len(item)):
                for j in range(len(item)):
                    hfinal[i][j] += item[i][j]

        return hfinal


if __name__ == "__main__":
    npc = 2

    # grid = [[0, 0], [0.025, 0], [0.025, 0.025], [0, 0.025]]
    grid = Grid.Grid()
    element = Element.Element4_2D(npc)
    # for i in range(len(grid)):
    jakobian = Jacobian()
    hmatrix = HMatrix(npc)
    for i in range(grid.nE):
        print(grid.elements[i].id[0])
        for j in range(pow(element.npc, 2)):
            jakobian.solveJacobian(i, j, grid, element)
            # print(jakobian.jacobian[0])
            # print(jakobian.jacobian[1])
            # print("Inverse")
            # print(jakobian.jacobianInverse[0])
            # print(jakobian.jacobianInverse[1])
            hmatrix.count_h_matrix(j, jakobian.jacobianInverse, element)
        grid.elements[i].H = hmatrix.solve_H_matrix(npc)
        print(grid.elements[i].H)


