from Parameters import Parameters


# noinspection PyTypeChecker
class Element4_2D:
    dNdE = []
    dNdN = []
    points = []
    npc = 0

    def __init__(self, npc):
        self.npc = npc
        self.dNdE = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.dNdN = [[0 for _ in range(4)] for _ in range(pow(npc, 2))]
        self.points = [[0 for _ in range(2)] for _ in range(pow(npc, 2))]
        param = Parameters(npc)
        for i in range(npc):
            for j in range(npc):
                self.points[i * npc + j][0] = param.points[j]
                self.points[i * npc + j][1] = param.points[i]

        for i in range(pow(npc, 2)):
            self.dNdE[i][0] = -0.25 * (1 - self.points[i][1])
            self.dNdE[i][1] = 0.25 * (1 - self.points[i][1])
            self.dNdE[i][2] = 0.25 * (1 + self.points[i][1])
            self.dNdE[i][3] = -0.25 * (1 + self.points[i][1])

            self.dNdN[i][0] = -0.25 * (1 - self.points[i][0])
            self.dNdN[i][1] = -0.25 * (1 + self.points[i][0])
            self.dNdN[i][2] = 0.25 * (1 + self.points[i][0])
            self.dNdN[i][3] = 0.25 * (1 - self.points[i][0])


if __name__ == "__main__":
    npc = 2
    a = Element4_2D(npc)
    for k in range(pow(npc,2)):
        print(a.dNdE[k])
    print()
    for k in range(pow(npc,2)):
        print(a.dNdN[k])
