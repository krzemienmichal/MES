import GlobalData
import Grid


class Aggregation:
    # agregacja H

    def aggregate_matrices(self, grid):
        H = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]
        C = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]

        Summed = [[0 for _ in range(grid.nN)] for _ in range(grid.nN)]
        for i in range(0, grid.nE):
            for j in range(4):
                for k in range(4):
                    H[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] += grid.elements[i].SummedMatrix[j][k]
                    C[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] += grid.elements[i].C[j][k]
                    Summed[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1] = \
                        H[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1]+\
                        C[grid.elements[i].id[j]-1][grid.elements[i].id[k]-1]/GlobalData.SIMULATION_STEP_TIME
        return H, C, Summed

    def aggregate_p_vector(self, grid:Grid.Grid, aggregated_c_matrix: list, temp_vector : list):
        P = [0 for _ in range(grid.nN)]
        for i in range(0, grid.nE):
            for j in range(4):
                P[grid.elements[i].id[j] - 1] += grid.elements[i].P[j]

        for i in range(grid.nN):
            for j in range(grid.nN):
                P[i] += aggregated_c_matrix[i][j] / GlobalData.SIMULATION_STEP_TIME * temp_vector[j]
        return P

    def sum_H_with_Hbc(self, grid):
        for i  in range(grid.nE):
            for H, Hbc, j in zip(grid.elements[i].H, grid.elements[i].Hbc, range(4)):
                for x, y in zip(H, Hbc):
                    grid.elements[i].SummedMatrix[j].append(x+y)


if __name__ == "__main__":
    pass
