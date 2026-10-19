import networkx as nx

INT_MAX = 40960

G = nx.Graph() # undirected graph, might be directed later

# IDs: 0 to 11
all_major_keys = [{"key": "C major"}, {"key": "G major"}, {"key": "D major"}, 
                  {"key": "A major"}, {"key": "E major"}, {"key": "B major"},
                  {"key": "F#/Gb major"}, {"key": "C#/Db major"}, {"key": "Ab major"},
                  {"key": "Eb major"}, {"key": "Bb major"}, {"key": "F major"}]

# IDs: 12 to 23
all_minor_keys = [{"key": "A minor"}, {"key": "E minor"}, {"key": "B minor"},
                  {"key": "F# minor"}, {"key": "C# minor"}, {"key": "G#/Ab minor"},
                  {"key": "D#/Eb minor"}, {"key": "Bb minor"}, {"key": "F minor"},
                  {"key": "C minor"}, {"key": "G minor"}, {"key": "D minor"}]

all_keys = all_major_keys + all_minor_keys

all_major_weights = [1000, 1, 2, 3, 2.5, 6, 10, 6, 2.5, 3, 2, 1, 1, 1, 3, 6, 9, 12, 10, 12, 1, 1, 3, 2]
all_minor_weights = [1000, 1.5, 3, 5, 8, 11, 15, 11, 8, 5, 3, 1]

for i in range(12):
    G.add_node(i, **all_major_keys[i])
for i in range(12, 24):
    G.add_node(i, **all_minor_keys[i-12])

# start with major
for i in range(12):
    # major-to-major
    for j in range(i+1, 12): # if G is directed, then change into range(12)
        G.add_edge(i, j, weight=all_major_weights[j-i])
        

    # then for major-to-minor
    for j in range(12, 24):
        G.add_edge(i, j, weight=all_major_weights[(j-i) % 12 + 12])

# now finish with minor-to-minor

for i in range(12, 24):
    for j in range(i+1, 24):
        G.add_edge(i, j, weight=all_minor_weights[(j-i) % 12])

# print(list(G.edges(data=True)))

# ------------------------------------------------



def find_path(graph, start, end, length):
    # RETURNS: (total_weight, list_of_nodes_traversed)

    # length 0 but different endpoints
    if length == 0:
        if start == end:
            return 0, [start]
        return INT_MAX, None

    # length 1 but same endpoint
    if length == 1:
        if start == end:
            return INT_MAX, None

        if graph.has_edge(start, end):
            return graph[start][end]["weight"], [start, end]

        return INT_MAX, None

    # A simple path cannot return to its starting vertex
    if start == end:
        return INT_MAX, None

    best_weight = INT_MAX
    best_path = None

    def search(current, remaining, visited, path, weight):
        nonlocal best_weight, best_path

        # We have used exactly the required number of edges
        if remaining == 0:
            if current == end and weight < best_weight:
                best_weight = weight
                best_path = path.copy()
            return

        # paths must be simple.
        if current == end:
            return

        for neighbor in graph.neighbors(current):

            # Don't visit a vertex twice
            if neighbor in visited:
                continue

            edge_weight = graph[current][neighbor]["weight"]

            # don't continue if we already can't beat the best path
            new_weight = weight + edge_weight
            if new_weight >= best_weight:
                continue

            visited.add(neighbor)
            path.append(neighbor)

            search(
                neighbor,
                remaining - 1,
                visited,
                path,
                new_weight
            )

            path.pop()
            visited.remove(neighbor)

    search(
        start,
        length,
        {start},
        [start],
        0
    )

    if best_path is None:
        return INT_MAX, None

    return best_weight, best_path

for i in range(1, 7):
    # upper bound is 7 right now, any higher and run time is excruciatingly long

    (weight, path) = find_path(G, 0, 17, i) # CHANGE THIS FOR CUSTOM
    # Ex: 0 is C Major, 17 is G# Minor


    print(f'Path of length {i} ---- total weight = {weight}')
    for item in path:
        print(f'{all_keys[item]["key"]} -->')
    print("---------------------------------------------------------")