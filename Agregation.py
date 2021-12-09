import Grid


class Agregation:
    # agregacja H
    grid = None
    H = []
    C = []
    P = []
    Summed = []


    def __init__(self, grid:Grid.Grid):
        self.grid = grid
        self.sumHwithHbc()

    def aggregateMatrix(self):
        self.H = [[0 for _ in range(self.grid.nN)] for _ in range(self.grid.nN)]
        self.C = [[0 for _ in range(self.grid.nN)] for _ in range(self.grid.nN)]
        self.P = [0 for _ in range(self.grid.nN)]
        Summed = [[0 for _ in range(self.grid.nN)] for _ in range(self.grid.nN)]
        for i in range(0, self.grid.nE):
            for j in range(4):
                for k in range(4):
                    self.H[self.grid.elements[i].id[j]-1][self.grid.elements[i].id[k]-1] += self.grid.elements[i].SummedMatrix[j][k]
                    self.C[self.grid.elements[i].id[j]-1][self.grid.elements[i].id[k]-1] += self.grid.elements[i].C[j][k]
                    self.Summed[]

    def sumHwithHbc(self):
        for i  in range(self.grid.nE):
            for H, Hbc, j in zip(self.grid.elements[i].H, self.grid.elements[i].Hbc, range(4)):
                for x, y in zip(H, Hbc):
                    self.grid.elements[i].SummedMatrix[j].append(x+y)


if __name__ == "__main__":
    pass
