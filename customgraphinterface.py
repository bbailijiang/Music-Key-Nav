INT_MAX = 4096

def initialize(num_vertices):
    list = []
    for i in range(num_vertices):
        inner_list = []
        for j in range(num_vertices):
            inner_list.append(INT_MAX)
        list.append(inner_list)

    return list

def change_edge_weight(graph, start, end, new_weight):
    graph[start][end] = new_weight
    return graph
