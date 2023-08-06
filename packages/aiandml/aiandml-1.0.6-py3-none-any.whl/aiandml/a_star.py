def astar(start,end,tree,heuristic,cost):
    opened, closed = [[start, 0]], []
    while True:
        fn = [i[1] for i in opened]
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]
        closed.append(opened[chosen_index])
        del opened[chosen_index]
        if closed[-1][0] == end:
            break
        for item in tree[node]:
            if item[0] in [i[0] for i in closed]:
                continue
            cost.update({item[0]: item[1] + cost[node]})
            opened.append([item[0],item[1] + cost[node] + heuristic[item[0]]])
    trace_node, optimal_sequence = 'E', ['E']
    for i in range(len(closed) - 2, -1, -1):
        check_node = closed[i][0]
        if trace_node in [i[0] for i in tree[check_node]]:
            children_cost = [i[1] for i in tree[check_node]]
            children_node = [i[0] for i in tree[check_node]]
            if cost[check_node] + children_cost[children_node.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()
    return closed, optimal_sequence

def algorithm():
    print('''\nAlgorithm: The A* search algorithm is discussed below:
    1) Initialize the open and closed lists
    2) Add start node to the open list
    3) For all the neighbouring nodes, find the least cost F node
    4) Switch to the closed list
        * For nodes adjacent to the current node
        * If the node is not reachable, ignore it. 
        * Else If the node is not on the open list, move it to the open list and calculate f, g, h.
        * If the node is on the open list, check if the path it offers is less than the current path 
          and change to it if it does so.
    5) Stop working when
        * You find the destination
        * You cannot find the destination going through all possible points'''
          )
def problem_statement():
    print('''
Problem Statement:
    Implement A* Search Algorithm.''')
def description():
    print('\nDescription: \n\tA* Search algorithm is one of the best and popular technique used in path-finding and graph traversals. Informally speaking, A* Search algorithms, unlike other traversal techniques, it has “brains”. What it means is that it is really a smart algorithm which separates it from the other conventional algorithms. Example: Consider a square grid having many obstacles and we are given a starting cell and a target cell. We want to reach the target cell from the starting cell as quickly as possible. What A* Search Algorithm does is that at each step it picks the node according to a value-‘f’ which is a parameter equal to the sum of two other parameters – ‘g’ and ‘h’. At each step it picks the node/cell having the lowest ‘f’, and processes that node/cell. The two parameters ‘g’ and ‘h’ are defined as follows: g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there. h = the estimated movement cost to move from that given square on the grid to the final destination.')

def code():
    print('\nProgram for A* Search Algorithm:')
    print('''
tree = {'S': [['A', 1], ['B', 2]],
        'A': [['E', 13]],
        'B': [['E', 5]]}
heuristic = {'S': 5, 'A': 4, 'B': 5, 'E': 0}
cost = {'S': 0}

def astar():
    opened, closed = [['S', 0]], []
    while True:
        fn = [i[1] for i in opened]
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]
        closed.append(opened[chosen_index])
        del opened[chosen_index]
        if closed[-1][0] == 'E':
            break
        for item in tree[node]:
            if item[0] in [i[0] for i in closed]:
                continue
            cost.update({item[0]: item[1] + cost[node]})
            opened.append([item[0], item[1] + cost[node] + heuristic[item[0]]])
    trace_node, optimal_sequence = 'E', ['E']
    for i in range(len(closed) - 2, -1, -1):
        check_node = closed[i][0]
        if trace_node in [i[0] for i in tree[check_node]]:
            children_cost = [i[1] for i in tree[check_node]]
            children_node = [i[0] for i in tree[check_node]]
            if cost[check_node] + children_cost[children_node.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()
    return closed, optimal_sequence

if __name__ == '__main__':
    print(astar())

    ''')

# if __name__ == '__main__':
#     run()