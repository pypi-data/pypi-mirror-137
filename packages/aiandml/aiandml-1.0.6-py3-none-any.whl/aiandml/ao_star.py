class Graph:
    def __init__(self, graph, hnl, startNode):
        self.graph = graph
        self.H = hnl
        self.start = startNode
        self.parent = {}
        self.status = {}
        self.solutionGraph = {}

    def applyAOstar(self):
        self.aoStar(self.start, False)

    def getNeighbors(self, v):
        return self.graph.get(v, '')

    def getStatus(self, v):
        return self.status.get(v, 0)

    def setStatus(self, v, val):
        self.status[v] = val

    def gethnv(self, n):
        return self.H.get(n, 0)

    def sethnv(self, n, val):
        self.H[n] = val

    def printSolution(self):
        print("FOR GRAPH SOLUTION, TRAVERSE THE GRAPH FROM THE START NODE : ", self.start)
        print(
            "---------------------------------------------------------------------------------------------------------------")
        print(self.solutionGraph)
        print(
            "---------------------------------------------------------------------------------------------------------------")
    def cmccn(self, v):
        mc = 0
        ctcn = {}
        ctcn[mc] = []
        flag = True
        for element in self.getNeighbors(v):
            cost = 0
            nl = []
            for c, weight in element:
                cost = cost + self.gethnv(c) + weight
                nl.append(c)
            if flag == True:
                mc = cost
                ctcn[mc] = nl
                flag = False
            else:
                if mc > cost:
                    mc = cost
                    ctcn[mc] = nl
        return mc, ctcn[mc]

    def aoStar(self, v, bt):
        print("HEURISTIC VALUE : ", self.H)
        print("SOLUTION GRAPH : ", self.solutionGraph)
        print("PROCESSING NODE : ", v)
        print(
            "---------------------------------------------------------------------------------------------------------------")
        if self.getStatus(v) >= 0:
            mc, cnl = self.cmccn(v)
            self.sethnv(v, mc)
            self.setStatus(v, len(cnl))
            solved = True
            for cn in cnl:
                self.parent[cn] = v
                if self.getStatus(cn) != -1:
                    solved = solved & False
            if solved:
                self.setStatus(v, -1)
                self.solutionGraph[v] = cnl
            if v != self.start:
                self.aoStar(self.parent[v], True)
            if not bt:
                for cn in cnl:
                    self.setStatus(cn, 0)
                    self.aoStar(cn, False)

#
# def run(graph , heuristicNodeList , startNode):
#     h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 0, 'J': 1, 'T': 3}
#     graph1 = {
#         'A': [[('B', 1), ('C', 1)], [('D', 1)]],
#         'B': [[('G', 1)], [('H', 1)]],
#         'C': [[('J', 1)]],
#         'D': [[('E', 1), ('F', 1)]],
#         'G': [[('I', 1)]]
#     }
#     G1 = Graph(graph , heuristicNodeList , startNode)
#     G1.applyAOstar()
#     G1.printSolution()
#
#     h2 = {'A': 1, 'B': 6, 'C': 12, 'D': 10, 'E': 4, 'F': 4, 'G': 5, 'H': 7}
#     graph2 = {
#         'A': [[('B', 1), ('C', 1)], [('D', 1)]],
#         'B': [[('G', 1)], [('H', 1)]],
#         'D': [[('E', 1), ('F', 1)]]
#     }
#     G2 = Graph(graph2, h2, 'A')
#     G2.applyAOstar()
#     G2.printSolution()

def problem_statement():
    print('''
Problem Statement:
    Implement AO* Search algorithm
    ''')
def description():
    print('Description:\n\tAO* Algorithm basically based on  problem decomposition (Breakdown problem into small pieces).When a problem can be divided into a set of sub problems, where each sub problem can be solved separately and a combination of these will be a solution, AND-OR graphs or AND - OR trees are used for representing the solution. The decomposition of the problem or problem reduction generates AND arcs.')
def algorithm():
    print('''
Algorithm: The AO* search algorithm is discussed below:
    1. Let GRAPH consist only of the node representing the initial state. Call this node INIT, Compute h' (INIT). 
    2. Until INIT is labelled SOLVED or until INIT’s h' value becomes greater than FUTILITY, repeat the following procedure:
        a. Trace the labelled arcs from INIT and select for expansion one of the as yet unexpanded nodes that occurs on 
           this path. Call the selected node NODE.
        b. Generate the successors of NODE. If there are none, then assign FUTILITY as the h' value of NODE. 
           This is equivalent to saying that NODE is not solvable. If there are successors, then for each one (called SUCCESSOR) do the following:
            i) Add SUCCESSOR to GRAPH.
            ii) If SUCCESSOR is a terminal node, label it SOLVED & assign it an h' value to 0.
            iii) If SUCCESSOR is not a terminal node, compute its h' value.
        c. Propagate the newly discovered information up the graph by doing the following: Let S be a set of nodes that have 
           been labelled SOLVED or whose h' values have been changed and so need to have values propagated back to their parents.
           Initialize S to NODE. Until S is empty, repeat the following procedure:
            i) If possible, select from S a node none of whose descendants in GRAPH occurs in S. If there is no such node, 
               select any node from S. Call this node CURRENT, and remove it from S.
            ii) Compute the cost of each of the arcs emerging from CURRENT. The cost of each arc is equal to the sum of the h' 
                values of each of the nodes at the end of the arc plus whatever the cost of the arc itself is. Assign as 
                CURRENT’S new h' value the minimum of the costs just computed for the arcs emerging from it.
            iii) Mark the best path out of CURRENT by making the arc that had the minimum cost as compared in the previous step.
            iv) Mark CURRENT SOLVED if all the nodes connected to it through the new labelled arc have been labelled SOLVED.
            v) If CURRENT has been labelled SOLVED or if the cost of CURRENT was just changed, then its new status must be 
               propagated back up the graph. 
            So add all of the ancestors of CURRENT to S.
    ''')
def code():
    print('\n Program for AO* algorithm: ')
    print('''
class Graph:
    def __init__(self, graph, heuristicNodeValue, startNode):
        self.graph = graph
        self.H = heuristicNodeValue
        self.start = startNode
        self.parent = {}
        self.status = {}
        self.solutionGraph = {}

    def getNeighbour(self, v):
        return self.graph.get(v, '')

    def getStatus(self, v):
        return self.status.get(v, 0)

    def setStatus(self, v, val):
        self.status[v] = val

    def getH(self, v):
        return self.H.get(v, 0)

    def setH(self, v, val):
        self.H[v] = val

    def printSolution(self):
        print('FOR THE GRAPH SOLUTION , TRAVERSE THE GRAPH FROM THE NODE : ', self.start)
        print('-' * 100)
        print(self.solutionGraph)
        print('-' * 100)

    def applyAOStar(self):
        self.AOStar(self.start, False)

    def minimumCostChild(self, v):
        minimumCost = 0
        ChildNodeList = {minimumCost: []}
        flag = True
        for item in self.getNeighbour(v):
            cost, nodeList = 0, []
            for c, w in item:
                cost += self.getH(c) + w
                nodeList.append(c)
            if flag:
                minimumCost = cost
                ChildNodeList[minimumCost] = nodeList
                flag = False
            else:
                if minimumCost > cost:
                    minimumCost = cost
                    ChildNodeList[minimumCost] = nodeList
        return minimumCost, ChildNodeList[minimumCost]

    def AOStar(self, v, backtracking):
        print(

            'Heuristic Value : ', self.H,
            '\\nSolution Graph : ', self.solutionGraph,
            '\\nProcessing Node : ', v,'\\n',
            '-' * 100
        )
        if self.getStatus(v) >= 0:
            minimumCost, childNodeList = self.minimumCostChild(v)
            self.setH(v, minimumCost)
            self.setStatus(v, len(childNodeList))
            Solved = True
            for childNode in childNodeList:
                self.parent[childNode] = v
                if self.getStatus(childNode) != -1:
                    Solved &= False
            if Solved:
                self.setStatus(v, -1)
                self.solutionGraph[v] = childNodeList
            if v != self.start:
                self.AOStar(self.parent[v], True)
            if not backtracking:
                for childNode in childNodeList:
                    self.setStatus(childNode, 0)
                    self.AOStar(childNode, False)


if __name__ == '__main__':
    h = {'A': 1, 'B': 6, 'C': 12, 'D': 10, 'E': 4, 'F': 4, 'G': 5, 'H': 7}
    graph = {
        'A': [[('B', 1), ('C', 1)], [('D', 1)]],
        'B': [[('G', 1)], [('H', 1)]],
        'D': [[('E', 1), ('F', 1)]]
    }
    g = Graph(graph, h, 'A')
    g.applyAOStar()
    g.printSolution()

    ''')