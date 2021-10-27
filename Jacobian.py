from Parameters import Parameters


class Element4_2D:
    dNdE = []
    dNdN = []
    a = Parameters(2)
    points = [[a.points[0], a.points[0]],
              [a.points[1], a.points[0]],
              [a.points[1], a.points[1]],
              [a.points[0], a.points[1]]]

    def __init__(self, npc):
        self.dNdE = [[0 for _ in range(4)] for _ in range(npc)]
        self.dNdN = [[0 for _ in range(4)] for _ in range(npc)]
        for i in range(4):
            self.dNdE[i][0] = -0.25 * (1-self.points[i][1])
            self.dNdE[i][1] = 0.25 * (1 - self.points[i][1])
            self.dNdE[i][2] = 0.25 * (1 + self.points[i][1])
            self.dNdE[i][3] = -0.25 * (1 + self.points[i][1])

            self.dNdN[i][0] = -0.25 * (1 - self.points[i][0])
            self.dNdN[i][1] = -0.25 * (1 + self.points[i][0])
            self.dNdN[i][2] = 0.25 * (1 + self.points[i][0])
            self.dNdN[i][3] = 0.25 * (1 - self.points[i][0])


if __name__ == "__main__":
    a = Element4_2D(4)
    for k in range(4):
        print(a.dNdE[k])
    print()
    for k in range(4):
        print(a.dNdN[k])

