import math

import Element4_2D
import GlobalData
import Grid
import Parameters


class HbcSolver():
    uni_ele = None
    data = None
    sides = None

    def __init__(self, data:Grid.Grid ,npc:int):
        self.uni_ele = Element4_2D.Element4_2D(npc)
        self.data = data
        self.sides = []


    def countDetJ(self, pointA, pointB):
        # print(pointA, pointB)
        detJ = math.sqrt(pow(pointB[0] - pointA[0], 2) + pow(pointB[1]-pointA[1],2))/2
        return detJ

    def defineSides(self, grid:Grid.Grid.elements):
        # for i in range(len(data)):
        #     if(i == len(data)-1):
        #         self.sides.append([self.data[i], self.data[0]])
        #     else:
        #         self.sides.append([self.data[i], self.data[i+1]])
        #
        for i in range(4):
            if i == 3 and (self.data.nodes[grid.id[i]-1].bc == 1 and self.data.nodes[grid.id[0]-1].bc == 1):
                self.sides.append([self.data.nodes[grid.id[i]-1].getPoint(), self.data.nodes[grid.id[0]-1].getPoint()])
            elif i!=3 and (self.data.nodes[grid.id[i]-1].bc == 1 and self.data.nodes[grid.id[i+1]-1].bc == 1):
                self.sides.append([self.data.nodes[grid.id[i]-1].getPoint(), self.data.nodes[grid.id[i+1]-1].getPoint()])
            else:
                self.sides.append(False)

    def solveHbc(self, grid:Grid.Grid.elements):
        self.sides = []
        self.defineSides(grid)
        for i in range(4):
            N = [[0 for _ in range(4)] for _ in range(self.uni_ele.npc)]
            self.uni_ele.countNmatrix(N, self.uni_ele.borderPoints[i])
            if self.sides[i]:
                detJ = self.countDetJ(self.sides[i][0],self.sides[i][1])
            else:
                detJ = 0.0
            for j in range(4):
                tem = [[] for _ in range(self.uni_ele.npc)]
                for k in range(4):
                    for l in range(self.uni_ele.npc):
                        tem[l].append(GlobalData.GlobalData.alpha *N[l][j]*N[l][k]*Parameters.Parameters(self.uni_ele.npc).wages[l])

                for l in range(self.uni_ele.npc): #obliczanie wektora P PRZENIESC DO OSOBNEJ FUNKCJI
                    grid.P[j] += GlobalData.GlobalData.alpha * GlobalData.GlobalData.temperature * N[l][j] * Parameters.Parameters(self.uni_ele.npc).wages[l] * detJ

                if self.uni_ele.npc == 2:
                    for a,b,z in zip(tem[0],tem[1], range(4)):
                        grid.Hbc[j][z] += (a+b)*detJ
                else:
                    for a, b, c, z in zip(tem[0], tem[1], tem[2], range(4)):
                        grid.Hbc[j][z] += (a + b + c) * detJ


if __name__ == "__main__":
    # data = [[0,0],
    #         [0,0.025],
    #         [0.025,0.025],
    #         [0,0.025]]
    data = Grid.Grid()
    a = HbcSolver(data, 2)
    for i in range(data.nE):
        a.solveHbc(data.elements[i])
        # for matrix in data.elements[i].Hbc:
        #     print(matrix)
        # print()
        for hbc in data.elements[i].Hbc:
            print(hbc)
        print()
        print(data.elements[i].P)
        print()


