import Element
import Grid


class Jacobian:
    jacobian = [[0 for _ in range(2)] for _ in range(2)]
    jacobianInverse = [[0 for _ in range(2)] for _ in range(2)]

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

        det = self.jacobian[0][0] * self.jacobian[1][1] - self.jacobian[0][1] * self.jacobian[1][0]
        det = 1 / det
        for n in range(2):
            for m in range(2):
                self.jacobianInverse[n][m] = det * self.jacobian[n][m]


if __name__ == "__main__":
    # grid = [[0, 0], [0.025, 0], [0.025, 0.025], [0, 0.025]]
    grid = Grid.Grid()
    element = Element.Element4_2D(2)
    # for i in range(len(grid)):
    jakobian = Jacobian()
    for i in range(grid.nE):
        #print(grid.elements[i].id[0])
        for j in range(pow(element.npc, 2)):
            jakobian.solveJacobian(i, j, grid, element)
            # print(jakobian.jacobian)
            # print("Inverse")
            print(jakobian.jacobianInverse)
            # print("End inverse")

    print("test")
