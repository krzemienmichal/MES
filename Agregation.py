import copy

import GlobalData
import Grid


class Agregation:
    # agregacja H

    def aggregateMatrix(self, grid):
        H = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]
        C = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]


        Summed = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]
        for i in range(0, grid.nE):
            for j in range(4):
                for k in range(4):
                    H[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] += grid.elements[i].SummedMatrix[j][k]
                    C[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] += grid.elements[i].C[j][k]
                    Summed[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] = H[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1]+C[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1]/GlobalData.GlobalData.simultaion_step_time

        return H ,C ,Summed


    def aggregatePvector(self,grid:Grid.Grid, aggregatedCmatrix: list, tempVector : list):
        P = [0 for _ in range(grid.nN)]
        for i in range(0, grid.nE):
            for j in range(4):
                P[grid.elements[i].id[j] - 1] += grid.elements[i].P[j]

        for i in range(grid.nN):
            for j in range(grid.nN):
                P[i] += aggregatedCmatrix[i][j]/GlobalData.GlobalData.simultaion_step_time * tempVector[j]
        return P



    def sumHwithHbc(self, grid):
        for i  in range(grid.nE):
            for H, Hbc, j in zip(grid.elements[i].H, grid.elements[i].Hbc, range(4)):
                for x, y in zip(H, Hbc):
                    grid.elements[i].SummedMatrix[j].append(x+y)

if __name__ == "__main__":
    pass
