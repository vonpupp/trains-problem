#!/usr/bin/env python2


#def paths(graph, v):
#    """Generate the maximal cycle-free paths in graph starting at v.
#    graph must be a mapping from vertices to collections of
#    neighbouring vertices.
#
#    >>> g = {1: [2, 3], 2: [3, 4], 3: [1], 4: []}
#    >>> sorted(paths(g, 1))
#    [[1, 2, 3], [1, 2, 4], [1, 3]]
#    >>> sorted(paths(g, 3))
#    [[3, 1, 2, 4]]
#
#    """
#    path = [v]                  # path traversed so far
#    seen = {v}                  # set of vertices in path
#    def search():
#        dead_end = True
#        for neighbour in graph[path[-1]]:
#            if neighbour not in seen:
#                dead_end = False
#                seen.add(neighbour)
#                path.append(neighbour)
#                yield from search()
#                path.pop()
#                seen.remove(neighbour)
#        if dead_end:
#            yield list(path)
#    yield from search()


# SOURCE: http://www.widecodes.com/0zzjXXjXkk/find-all-paths-between-two-vertices-nodes-in-a-graph-using-python.html

import Queue
#from priodict import priorityDictionary
import sys
import heapq
import copy
from collections import deque

class MyQUEUE: # just an implementation of a queue

    def __init__(self):
        self.holder = []

    def enqueue(self,val):
        self.holder.append(val)

    def dequeue(self):
        val = None
        try:
            val = self.holder[0]
            if len(self.holder) == 1:
                self.holder = []
            else:
                self.holder = self.holder[1:]
        except:
            pass

        return val

    def IsEmpty(self):
        result = False
        if len(self.holder) == 0:
            result = True
        return result


path_queue = MyQUEUE() # now we make a queue

class TrainsProblem:
    def __init__(self):
        self.graph = {}

    def path_weight(self, path):
        result = 0
        for idx, node in enumerate(path):
            try:
                next_node = path[idx + 1]
                result += self.graph[node][next_node]
            except KeyError, e:
                raise
            except:
                result += 0
        return result


    def BFS(self, start, end, q):
        temp_path = [start]
        #q.enqueue(temp_path)
        q.put(temp_path)
        #while q.IsEmpty() == False:
        while not q.empty():
            #tmp_path = q.dequeue()
            tmp_path = q.get()
            last_node = tmp_path[len(tmp_path)-1]
            #if last_node == end:
            #    print "VALID_PATH : ",tmp_path
            if tmp_path[len(tmp_path)-1] == end:
                yield tmp_path
            for link_node in self.graph[last_node]:
                #if link_node not in tmp_path:
                new_path = []
                new_path = tmp_path + [link_node]
                #w = path_weight(graph, new_path)
                #q.enqueue(new_path)
                q.put(new_path)

    def DFS(self, start, end, q):
        temp_path = [start]
        #q.enqueue(temp_path)
        q.put(temp_path)
        #while q.IsEmpty() == False:
        while not q.empty():
            #tmp_path = q.dequeue()
            tmp_path = q.get()
            last_node = tmp_path[len(tmp_path)-1]
            if last_node == end:
                print "VALID_PATH : ",tmp_path
            if tmp_path[len(tmp_path)-1] == end:
                yield tmp_path
            for link_node in self.graph[last_node]:
                #if link_node not in tmp_path:
                new_path = []
                new_path = [link_node] + tmp_path
                #w = path_weight(graph, new_path)
                #q.enqueue(new_path)
                q.put(new_path)



    def paths_by_maximum_stops(self, start, end, max_stops):
        q = Queue.Queue()
        paths_iterator = self.BFS(start, end, q)
        paths = []
        while True:
            path = paths_iterator.next()
            # Even when not visiting another vertex is a valid solution,
            # this type of solutions are not added to the list since they are
            # not part of the accepted answers
            if len(path) > 1:
                paths += [path]
            if len(path) >= max_stops:
                break
        return paths

    def paths_by_exact_stops(self, start, end, max_stops):
        q = Queue.Queue()
        paths_iterator = self.BFS(start, end, q)
        paths = []
        while True:
            path = paths_iterator.next()
            # Even when not visiting another vertex is a valid solution,
            # this type of solutions are not added to the list since they are
            # not part of the accepted answers
            if len(path) == max_stops:
                paths += [path]
            if len(path) > max_stops:
                break
        return paths

    def paths_by_minimum_weight(self, start, end):
        q = Queue.Queue()
        paths_iterator = self.BFS(start, end, q)
        path = paths_iterator.next()
        return path, self.path_weight(path)

    def paths_by_maximum_weight(self, start, end, max_weight, max_iterations):
        lifo = Queue.Queue()
        paths_iterator = self.BFS(start, end, lifo)
        paths = []
        i = 0
        while i < max_iterations:
            path = paths_iterator.next()
            # Even when not visiting another vertex is a valid solution,
            # this type of solutions are not added to the list since they are
            # not part of the accepted answers
            if len(path) > 1 and self.path_weight(path) < max_weight:
                paths += [path]
            #if self.path_weight(path) < max_weight:
            #    break
            i += 1
        return paths

    def dijkstra_all(graph, src):
        length = len(graph)
        type_ = type(graph)
        if type_ == list:
            nodes = [i for i in xrange(length)]
        elif type_ == dict:
            nodes = [i for i in graph.keys()]

        visited = [src]
        path = {src:{src:[]}}
        nodes.remove(src)
        distance_graph = {src:0}
        pre = next = src

        while nodes:
            distance = float('inf')
            for v in visited:
                for d in nodes:
                    new_dist = graph[src][v] + graph[v][d]
                    if new_dist < distance:
                        distance = new_dist
                        next = d
                        pre = v
                        graph[src][d] = new_dist


            path[src][next] = [i for i in path[src][pre]]
            path[src][next].append(next)

            distance_graph[next] = distance

            visited.append(next)
            nodes.remove(next)

        return distance_graph, path

    def Dijkstra(self, start, end=None):
            """
            Find shortest paths from the start vertex to all
            vertices nearer than or equal to the end.

            The input graph G is assumed to have the following
            representation: A vertex can be any object that can
            be used as an index into a dictionary.  G is a
            dictionary, indexed by vertices.  For any vertex v,
            G[v] is itself a dictionary, indexed by the neighbors
            of v.  For any edge v->w, G[v][w] is the length of
            the edge.  This is related to the representation in
            <http://www.python.org/doc/essays/graphs.html>
            where Guido van Rossum suggests representing graphs
            as dictionaries mapping vertices to lists of neighbors,
            however dictionaries of edges have many advantages
            over lists: they can store extra information (here,
            the lengths), they support fast existence tests,
            and they allow easy modification of the graph by edge
            insertion and removal.  Such modifications are not
            needed here but are important in other graph algorithms.
            Since dictionaries obey iterator protocol, a graph
            represented as described here could be handed without
            modification to an algorithm using Guido's representation.

            Of course, G and G[v] need not be Python dict objects;
            they can be any other object that obeys dict protocol,
            for instance a wrapper in which vertices are URLs
            and a call to G[v] loads the web page and finds its links.

            The output is a pair (D,P) where D[v] is the distance
            from start to v and P[v] is the predecessor of v along
            the shortest path from s to v.

            Dijkstra's algorithm is only guaranteed to work correctly
            when all edge lengths are positive. This code does not
            verify this property for all edges (only the edges seen
            before the end vertex is reached), but will correctly
            compute shortest paths even for some graphs with negative
            edges, and will raise an exception if it discovers that
            a negative edge has caused it to make a mistake.
            """

            D = {}  # dictionary of final distances
            P = {}  # dictionary of predecessors
            Q = priorityDictionary()   # est.dist. of non-final vert.
            Q[start] = 0

            for v in Q:
                D[v] = Q[v]
                if v == end:
                    break
                for w in self.graph[v]:
                    vwLength = D[v] + self.graph[v][w]
                    if w in D:
                        if vwLength < D[w]:
                            raise ValueError, \
                                "Dijkstra: found better path to already-final vertex"
                        elif w not in Q or vwLength < Q[w]:
                            Q[w] = vwLength
                            P[w] = v

            return (D, P)

    def shortest_path(self, start, end):
            """
            Find a single shortest path from the given start vertex
            to the given end vertex.
            The input has the same conventions as Dijkstra().
            The output is a list of the vertices in order along
            the shortest path.
            """

            D, P = self.Dijkstra(self.graph, start, end)
            Path = []
            while 1:
                Path.append(end)
                if end == start:
                    break
                end = P[end]
            Path.reverse()
            return Path, self.path_weight(Path)

    def dijkstra_shortest_path(self, start, end, visited=[], distances={}, predecessors={}):
        """Find the shortest path between start and end nodes in a graph"""
        # we've found our end node, now find the path to it, and return
        # This snippet has been adapted from:
        # https://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
        if start==end:
            path=[]
            while end != None:
                path.append(end)
                end=predecessors.get(end,None)
            return path[::-1], distances[start]
        # detect if it's the first time through, set current distance to zero
        if not visited: distances[start]=0
        # process neighbors as per algorithm, keep track of predecessors
        for neighbor in self.graph[start]:
            if neighbor not in visited:
                neighbordist = distances.get(neighbor,sys.maxint)
                tentativedist = distances[start] + self.graph[start][neighbor]
                if tentativedist < neighbordist:
                    distances[neighbor] = tentativedist
                    predecessors[neighbor]=start
        # neighbors processed, now mark the current node as visited
        visited.append(start)
        # finds the closest unvisited node to the start
        unvisiteds = dict((k, distances.get(k,sys.maxint)) for k in self.graph if k not in visited)
        closestnode = min(unvisiteds, key=unvisiteds.get)
        # now we can take the closest node and recurse, making it current
        return self.dijkstra_shortest_path(closestnode, end, visited, distances, predecessors)

    def sp(self, start, end):
        visited = []
        distances = {}
        predecessors = {}
        return self.dijkstra_shortest_path(start, end, visited, distances, predecessors)


    def heap_shortest_path(self, start, end):
        queue = [(0, start, [])]
        seen = set()
        while True:
            (cost, v, path) = heapq.heappop(queue)
            if v not in seen:
                print('cost: {}, v: {}, path: {}, end: {}'.format(cost, v, path, end))
                path = path + [v]
                seen.add(v)
                for (next, c) in self.graph[v].iteritems():
                    heapq.heappush(queue, (cost + c, next, path))
            if v == end and cost != 0:
                return path, cost

    def heap_shortest_paths(self, start, end, max_cost):
        queue = [(0, start, [])]
        seen = set()
        result = []
        while True:
            (cost, v, path) = heapq.heappop(queue)
            if v not in seen:
                print('cost: {}, v: {}, path: {}, end: {}'.format(cost, v, path, end))
                path = path + [v]
                seen.add(v)
                for (next, c) in self.graph[v].iteritems():
                    heapq.heappush(queue, (cost + c, next, path))
            if v == end and cost != 0:
                result += [path]
            if cost > max_cost:
                return result

    def remove_entries_from_dict(self, the_dict, entries):
        result = copy.copy(the_dict)
        for key in entries:
            if key in result:
                del result[key]
        return result

    def dfs_paths(self, start, goal):
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            li = self.remove_entries_from_dict(self.graph[vertex], path)
            for next in li:
                import ipdb; ipdb.set_trace() # BREAKPOINT
                if next == goal:
                    yield path + [next]
                else:
                    stack.append((next, path + [next]))

    def bfs(self, start):
        queue, enqueued = deque([(None, start)]), set([start])
        while queue:
            parent, n = queue.popleft()
            yield parent, n
            new = set(graph[n]) - enqueued
            enqueued |= new
            queue.extend([(n, child) for child in new])


    def dfs(self, start):
        stack, enqueued = [(None, start)], set([start])
        while stack:
            parent, n = stack.pop()
            yield parent, n
            new = set(self.graph[n]) - enqueued
            enqueued |= new
            stack.extend([(n, child) for child in new])

    def shortest_path_ab(self, start, end):
        parents = {}
        for parent, child in self.bfs(start):
            parents[child] = parent
            if child == end:
                revpath = [end]
                while True:
                    parent = parents[child]
                    revpath.append(parent)
                    if parent == start:
                        break
                    child = parent
                return list(reversed(revpath))
        return None # or raise appropriate exception




# Assumptions:
# - I used the Queue module. I don't think this break the rules since is part of
# the standard python library.
# - Relatively small graphs, I priorized readability over efficience since
# time/efficiency is not a constraint of the problem.

# Description:
# - I represented each city as a vertex of a weighted graph, where the weight is
# the "track" of "one-way" connecting each city.
# For such abstraction I used a dict of dicts. Given the example data:
# "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7" can be represented as follows:
#    graph = {'a': {'b': 5, 'd': 5, 'e': 7},
#             'b': {'c': 4},
#             'c': {'d': 8, 'e': 2},
#             'd': {'c': 8, 'e': 6},
#             'e': {'b': 3}
# - I performed a search using a Breadth-First Search (BFS)  algorithm [1] packed
# within an iterator yielding a path at a time.
# [1]: https://en.wikipedia.org/wiki/Breadth-first_search
# - Perhaps using Depth-First Search (DFS) would produce a more elegant
# solution, specially for the last type of problems, specially if the order of
# the paths matter. I will assume that it doesn't matter and therefore use BFS
# as well to not repeat myself.

if __name__ == "__main__":
    graph = {'a': {'b': 5, 'd': 5, 'e': 7},
             'b': {'c': 4},
             'c': {'d': 8, 'e': 2},
             'd': {'c': 8, 'e': 6},
             'e': {'b': 3}
            }

    #print(sorted(paths(graph, 'c')))
    #import ipdb; ipdb.set_trace() # BREAKPOINT
    #print('---')
    #v = BFS(graph, "a", "c", path_queue)
    trains = TrainsProblem()
    trains.graph = graph

    print('#1: {}'.format(trains.path_weight(['a', 'b', 'c'])))
    print('#2: {}'.format(trains.path_weight(['a', 'd'])))
    print('#3: {}'.format(trains.path_weight(['a', 'd', 'c'])))
    print('#4: {}'.format(trains.path_weight(['a', 'e', 'b', 'c', 'd'])))
    #print('#5: {}'.format(path_weight(graph, ['a', 'e', 'd'])))

    print('---')
    paths = trains.paths_by_maximum_stops('c', 'c', 4)
    print('#6: {}'.format(paths))

    print('---')
    paths = trains.paths_by_exact_stops('a', 'c', 5)
    print('#7: {}'.format(paths))

    print('---')
#    path, weight = trains.heap_shortest_path('a', 'c')
#    print('#8: {}, with weight {}'.format(path, weight))

    print('---')
#    path, weight = trains.heap_shortest_path('b', 'b')
#    print('#9: {}, with weight {}'.format(path, weight))
    #q9 = Queue()
    #v9 = BFS(graph, "b", "b", q9)
    #while True:
    #    path = v9.next()
    #    print('#9: {} weight {}'.format(path, path_weight(graph, path)))
    #    if len(path) >= 6:
    #        break

    print('---10')
    #paths = trains.DFS('c', 'c')
    #print(paths.next())
    #print(paths.next())
    #print(paths.next())
    #print(paths.next())
    #print(paths.next())
    #print(paths.next())
    #iterations = 10
    #paths = trains.paths_by_maximum_weight('c', 'c', 30, 10)
#    paths = trains.heap_shortest_paths('b', 'b', 30)
    #print('#10: {} solutions found in {} iterations: {}'.format(len(paths), iterations, paths))
    iterations = 5
    paths = trains.paths_by_maximum_weight('c', 'c', 30, iterations)
    print('#10: {} solutions found in {} iterations: {}'.format(len(paths), iterations, paths))
    iterations = 10
    paths = trains.paths_by_maximum_weight('c', 'c', 30, iterations)
    print('#10: {} solutions found in {} iterations: {}'.format(len(paths), iterations, paths))
    iterations = 20
    paths = trains.paths_by_maximum_weight('c', 'c', 30, iterations)
    print('#10: {} solutions found in {} iterations: {}'.format(len(paths), iterations, paths))
    iterations = 30
    paths = trains.paths_by_maximum_weight('c', 'c', 30, iterations)
    print('#10: {} solutions found in {} iterations: {}'.format(len(paths), iterations, paths))
    #import ipdb; ipdb.set_trace() # BREAKPOINT
    #q10 = MyQUEUE() # now we make a queue
    #v10 = BFS(graph, "c", "c", q10)
    #while True:
    #    path = v10.next()
    #    w = path_weight(graph, path)
    #    print('#10: {} weight {}'.format(path, w))
    #    if len(path) >= 11:
    #        break


    #import ipdb; ipdb.set_trace() # BREAKPOINT
