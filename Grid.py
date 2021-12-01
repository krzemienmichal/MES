class Node:
    x = None
    y = None
    bc = None

    def __init__(self, x=0.0, y=0.0, bc = 0):
        self.x = x
        self.y = y
        self.bc = bc


class Element:
    id = []
    H = []
    Hbc = []

    def __init__(self, ids):
        self.id = ids
        self.Hbc = [[0 for _ in range(4)] for _ in range(4)]

    def getID(self):
        return  self.id


class Grid:
    h = 0.5
    b = 0.1
    nH = 3
    nB = 4
    nN = nH*nB
    nE = (nH-1)*(nB-1)
    nodes = []
    elements = []

    def __init__(self):
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
            if (node.x == 0.0 or node.y == 0.0 or node.x == (self.nB-1)*(self.b/(self.nB-1)) or
                    node.y == (self.nH-1)*(self.h/(self.nH-1))):
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

