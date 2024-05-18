def add_node(v):
    if v in graph:
        print(v, "is already present in the graph")
    else:
        graph[v] = []

def add_edge(v1, v2):
    if v1 not in graph:
        print(v1, "is not present in the graph")
    elif v2 not in graph:
        print(v2, "is not present in the graph")
    else:
        graph[v1].append(v2)
        # graph[v2].append(v1)

def delete_node(v):
    if v not in graph:
        print(v,"is not present in graph")
    else:
        graph.pop(v)
        for i in graph:
            list1 = graph[i]
            graph[i] = [x for x in list1 if x != v]


def delete_edge(v1,v2):
    if v1 not in graph:
        print(v1,"not present")
    elif v2 not in graph:
        print(v2,"not present")
    else:
        graph[v1].remove(v2)
        # graph[v2].remove(v1)


def DFS(node, visited, graph):
    if node not in graph:
        print("Node not found")
        return
    if node not in visited:
        print(node)
        visited.add(node)
        for i in graph[node]:
            DFS(i, visited, graph)


def BFS(node, visited, graph):
    queue = [node]
    while queue:
        current = queue.pop(0)  # pop from the front

        if current not in visited:
            print(current)
            visited.add(current)

            for i in graph.get(current, []):
                if i not in visited:
                    queue.append(i)

def print_graph():
    for node in graph:
        print(node, "->", graph[node])

visited = set()
graph = {}

add_node("A")
add_node("B")
add_node("C")
add_node("D")
add_edge("A", "B")
add_edge("B", "D")
add_edge('A','B')
add_edge("C","D")
add_edge("D","A")
# delete_node("A")
# delete_edge("B","C")
print(graph)
DFS("A",visited,graph)
# BFS("A",visited,graph)

# print_graph()

