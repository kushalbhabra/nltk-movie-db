class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.capacity)
 
class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
        self.paths = []
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge,residual) in path:
                result = self.find_path( edge.sink, sink, path + [(edge,residual)] ) 
                if result != None:
                    return result
 
    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(res for edge,res in path)
            for edge,res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[edge] for edge in self.get_edges(source))


    def set_path(self,source,sink,path):
        if source == sink:
            path = path +' -> ' +sink
            self.paths.append(path)
        else:
            if source == 's':
                path = source
            else:
                path = path + ' -> ' + source

            for edge in self.get_edges(source):
                residual = edge.capacity - self.flow[edge]
                if residual == 0 and edge.capacity > 0:
                    self.set_path(edge.sink,sink,path)

    def get_path(self):
        return self.paths

    #Getting list of  vertices from paths expressed as string
    def getVertices(self,paths):
        vertices=[]
        for path in paths:
            nodes = path.split('->')
            for node in nodes:
                n = node.strip()
                if n not in vertices:
                    vertices.append(n)

        return vertices
    
    #Getting edges as list of tuples pair (FROM,TO) from paths expressed as string
    def getEdges(self,paths):
        edges=[]
        for path in paths:
            nodes = path.split('->')
            for i in range(len(nodes)-1):
                FROM = nodes[i].strip()
                TO = nodes[i+1].strip()
                edge_set = self.get_edges(FROM)
                for edge in edge_set:
                    if edge.sink == TO:
                        edges.append((FROM,TO,edge.capacity))
                #edges.append((FROM,TO,1))# last element is the weight ,which is 1
                edges.append((FROM,TO,1))
        return edges

