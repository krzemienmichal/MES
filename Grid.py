import math
import numbers


class Node:
    x = None
    y = None
    bc = None

    def __init__(self, x=0.0, y=0.0, bc = 0):
        self.x = x
        self.y = y
        self.bc = bc

    def getPoint(self):
        return  [self.x, self.y]


class Element:
    id = []
    H = []
    Hbc = []
    P = []
    C = []
    SummedMatrix = []

    def __init__(self, ids):
        self.id = ids
        self.Hbc = [[0 for _ in range(4)] for _ in range(4)]
        self.P = [0 for _ in range(4)]
        self.C = [[0 for _ in range(4)] for _ in range(4)]
        self.H = [[0 for _ in range(4)] for _ in range(4)]
        self.SummedMatrix = [[] for _ in range(4)]

    def getID(self):
        return self.id


class Grid:
    h = None
    b = None
    nH = None
    nB = None
    nN = None
    nE = None
    nodes = []
    elements = []

    def __init__(self, h: float, b: float, nH: int, nB: int):
        self.h = h
        self.b = b
        self.nH = nH
        self.nB = nB
        self.nN = nH*nB
        self.nE = (nH-1)*(nB-1)
        self.nodes = [Node(x=i*(self.b/(self.nB-1)), y=j*self.h/(self.nH-1))
                      for i in range(self.nB) for j in range(self.nH)]
        self.generate_elements()
        self.set_boundary_conditions()

    def generate_elements(self):
        remainder = 0
        for item in range(1, self.nE+1):
            if item != 0 and (item+remainder) % self.nH == 0:
                remainder += 1
            ids = [item+remainder, item+remainder+self.nH, item+remainder+self.nH+1, item+remainder+1]
            self.elements.append(Element(ids))

    def set_boundary_conditions(self):
        for node in self.nodes:
            if (node.x == 0.0 or node.y == 0.0 or math.isclose(node.x, self.b) or
                    math.isclose(node.y, self.h)):
                node.bc = 1


    def print_nodes(self):
        for i in range(self.nN):
            print(f"{self.nodes[i].x} ,{self.nodes[i].y}, {self.nodes[i].bc}")

    def print_elements(self):
        for i in range(self.nE):
            # nodes = self.nodes[self.elements[i].getID()]
            print(self.elements[i].getID())


if __name__ == '__main__':
    a = Grid()
    a.print_nodes()
    a.print_elements()

