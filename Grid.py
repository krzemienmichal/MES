import math


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
    Conductivity = None
    Density = None
    SpecificHeat = None
    Alpha = None

    def __init__(self, ids, data: list = None):
        self.id = ids
        self.Hbc = [[0 for _ in range(4)] for _ in range(4)]
        self.P = [0 for _ in range(4)]
        self.C = [[0 for _ in range(4)] for _ in range(4)]
        self.H = [[0 for _ in range(4)] for _ in range(4)]
        self.SummedMatrix = [[] for _ in range(4)]
        if data:
            self.Alpha = data[0]
            self.Conductivity = data[1]
            self.Density = data[2]
            self.SpecificHeat = data[3]

    def getID(self):
        return [(x-1) for x in self.id]


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

    def load_from_file_with_data(self,nodes_number: int, elements_number: int, nodes: list, elements: list, boundary_condition: list,
                       el_data: list):
        self.nN = nodes_number
        self.nE = elements_number
        self.nodes = [Node(x, y) for x, y in nodes]
        self.elements = []
        for el, _data in zip(elements,el_data):
            self.elements.append(Element(el, _data))

        for bc in boundary_condition:
            self.nodes[bc-1].bc = 1

    def load_from_file(self, nodes_number: int, elements_number: int, nodes: list, elements: list,
                       boundary_condition: list):
        self.nN = nodes_number
        self.nE = elements_number
        self.nodes = [Node(x, y) for x, y in nodes]
        self.elements = []
        for el in elements:
            self.elements.append(Element(el))

        for bc in boundary_condition:
            self.nodes[bc - 1].bc = 1

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
            print(f"{i+1}, {self.nodes[i].x}, {self.nodes[i].y}")
        bc_list = []
        for i in range(self.nN):
            if self.nodes[i].bc == 1:
                bc_list.append(i+1)
        print(bc_list)
    def print_elements(self):
        for i in range(self.nE):
            print(f"{i+1}, {self.elements[i].id[0]}, {self.elements[i].id[1]}, {self.elements[i].id[2]}, {self.elements[i].id[3]}")


if __name__ == '__main__':
    a = Grid()
    a.print_nodes()
    a.print_elements()

