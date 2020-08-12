
class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, id):
        if id not in self.vertices:
            self.vertices[id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Invalid vertix")

    def get_parents(self, vertix):
        if vertix in self.vertices:
            return self.vertices[vertix]
        else:
            raise IndexError("Invalid vertix")

    def find_longest_path(self, vertex):
        parents = self.get_parents(vertex)

        if not parents:
            # reached last node
            return [vertex]
        
        longest_path = None
        for parent in parents:
            current = self.find_longest_path(parent)
            if longest_path is None or len(current) > len(longest_path):
                longest_path = current
            elif len(current) == len(longest_path) and current[-1] < longest_path[-1]:
                longest_path = current
        
        return [vertex] + longest_path


def create_graph(ancestors):
    graph = Graph()

    for pair in ancestors:
        # source is child
        source = pair[1]
        # destination of edge is the parent
        destination = pair[0]

        if source not in graph.vertices:
            graph.add_vertex(source)
        if destination not in graph.vertices:
            graph.add_vertex(destination)
        
        graph.add_edge(source, destination)

    return graph
    

def earliest_ancestor(ancestors, starting_node):
    graph = create_graph(ancestors)

    longest_path = graph.find_longest_path(starting_node)

    return longest_path[-1] if len(longest_path) > 1 else -1
