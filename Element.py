from Parameters import Parameters

# noinspection PyTypeChecker
class Element4_2D:
    dNdE = []
    dNdN = []
    points = []
    borderPoints = [] #macierz punktów calkowania
    npc = 0
    wages = [] #macierz wag
    N = [] #macierz funkcji ksztaltu

    def __init__(self, npc):
        self.npc = npc
        self.dNdE = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.dNdN = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.points = [[0 for _ in range(2)] for _ in range(pow(npc, 2))]
        self.borderPoints = [[[0 for _ in range(2)] for _ in range(npc)] for _ in range(4)]
        self.N = [[0 for _ in range(4)] for _ in range(pow(npc,2))]
        param = Parameters(npc)
        for i in range(npc):
            for j in range(npc):
                self.points[i * npc + j][0] = param.points[j]
                self.points[i * npc + j][1] = param.points[i]
                self.wages.append(param.wages[j]*param.wages[i])

        for i in range(4):
            for j in range(npc):
                if i == 0:
                    self.borderPoints[i][j][0] = param.points[j]
                    self.borderPoints[i][j][1] = -1
                if i == 1:
                    self.borderPoints[i][j][0] = 1
                    self.borderPoints[i][j][1] = param.points[j]
                if i == 2:
                    self.borderPoints[i][j][0] = param.points[j]
                    self.borderPoints[i][j][1] = 1
                if i == 3:
                    self.borderPoints[i][j][0] = -1
                    self.borderPoints[i][j][1] = param.points[j]

        for i in range(pow(npc, 2)):
            self.dNdE[i][0] = -0.25 * (1 - self.points[i][1])
            self.dNdE[i][1] = 0.25 * (1 - self.points[i][1])
            self.dNdE[i][2] = 0.25 * (1 + self.points[i][1])
            self.dNdE[i][3] = -0.25 * (1 + self.points[i][1])

            self.dNdN[i][0] = -0.25 * (1 - self.points[i][0])
            self.dNdN[i][1] = -0.25 * (1 + self.points[i][0])
            self.dNdN[i][2] = 0.25 * (1 + self.points[i][0])
            self.dNdN[i][3] = 0.25 * (1 - self.points[i][0])

    def countNmatrix(self, N, points):
        for i in range(len(N)):
            N[i][0] = 0.25*(1-points[i][0])*(1-points[i][1])
            N[i][1] = 0.25*(1+points[i][0])*(1-points[i][1])
            N[i][2] = 0.25*(1+points[i][0])*(1+points[i][1])
            N[i][3] = 0.25*(1-points[i][0])*(1+points[i][1])



if __name__ == "__main__":
    npc = 2
    a = Element4_2D(npc)
    # for k in range(pow(npc,2)):
    #     print(a.dNdE[k])
    # print()
    # for k in range(pow(npc,2)):
    #     print(a.dNdN[k])
    for bp in a.borderPoints:
        print(bp)

    print()
    for N in a.N:
        print(N)

    # for item in a.wages:
    #     print(item)
