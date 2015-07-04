#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""Thoughtworks results for problem one: Trains

Problem description:

The local commuter railroad services a number of towns in Kiwiland.  Because of
monetary concerns, all of the tracks are 'one-way.'  That is, a route from
Kaitaia to Invercargill does not imply the existence of a route from
Invercargill to Kaitaia.  In fact, even if both of these routes do happen to
exist, they are distinct and are not necessarily the same distance!

The purpose of this problem is to help the railroad provide its customers with
information about the routes.  In particular, you will compute the distance
along a certain route, the number of different routes between two towns, and
the shortest route between two towns.

Input:  A directed graph where a node represents a town and an edge represents
a route between two towns.  The weighting of the edge represents the distance
between the two towns.  A given route will never appear more than once, and for
a given route, the starting and ending town will not be the same town.

Output: For test input 1 through 5, if no such route exists, output 'NO SUCH
ROUTE'.  Otherwise, follow the route as given; do not make any extra stops!
For example, the first problem means to start at city A, then travel directly
to city B (a distance of 5), then directly to city C (a distance of 4).

 1. The distance of the route A-B-C.
 2. The distance of the route A-D.
 3. The distance of the route A-D-C.
 4. The distance of the route A-E-B-C-D.
 5. The distance of the route A-E-D.
 6. The number of trips starting at C and ending at C with a maximum of 3
    stops.  In the sample data below, there are two such trips: C-D-C (2 stops).
    and C-E-B-C (3 stops).
 7. The number of trips starting at A and ending at C with exactly 4 stops.  In
    the sample data below, there are three such trips: A to C (via B,C,D);
    A to C (via D,C,D); and A to C (via D,E,B).
 8. The length of the shortest route (in terms of distance to travel) from
    A to C.
 9. The length of the shortest route (in terms of distance to travel) from
    B to B.
10. The number of different routes from C to C with a distance of less than 30.
    In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC,
    CEBCEBC, CEBCEBCEBC.


Test Input:
For the test input, the towns are named using the first few letters of the
alphabet from A to D.  A route between two towns (A to B) with a distance of 5
is represented as AB5.  Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7

Expected Output:
Output #1: 9
Output #2: 5
Output #3: 13
Output #4: 22
Output #5: NO SUCH ROUTE
Output #6: 2
Output #7: 3
Output #8: 9
Output #9: 9
Output #10: 7


Comments from Albert:
> Description:
> - I represented each city as a vertex of a weighted graph, where the weight is
> the "track" of "one-way" connecting each city.
> For such abstraction I used a dict of dicts. Given the example data:
> "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7" can be represented as follows:
>    graph = {'a': {'b': 5, 'd': 5, 'e': 7},
>             'b': {'c': 4},
>             'c': {'d': 8, 'e': 2},
>             'd': {'c': 8, 'e': 6},
>             'e': {'b': 3}
> - I performed a search using a Breadth-First Search (BFS)  algorithm [1]
> packed within an iterator yielding a path at a time.
> [1]: https://en.wikipedia.org/wiki/Breadth-first_search
> - Perhaps using Depth-First Search (DFS) would produce a more elegant
> solution, specially for the last type of problems, specially if the order of
> the paths matter. I will assume that it doesn't matter and therefore use BFS
> as well to not repeat myself.
>
>
> Assumptions:
> - I used the Queue and heapq modules. I don't think this break the rules
> since is part of the standard python library. By external libs I understand
> pip libs.
> I priorized readability over efficience since time/efficiency is not a
> constraint of the problem. Performance improvements can be done to this code.
> - Since the graph has loops to implement the last type of feature the
> algorithm could be caugh in a loop as in fact happens when not limited to a
> number of iterations. Therefore a max_iterations parameter has been added.
>
>
> Code checkups:
> - PEP8 compliant
> - Doctest passing
> - Pytest passing
"""

import Queue
import heapq


class NoRoute(Exception):
    """NoRoute exception

    Used when there is no way to calculate a distance on a non
    existing route like A-E-D

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code


class TrainsProblem:
    def __init__(self):
        self.graph = {}

    def create_graph_from_string(self, string):
        """
        Generates a graph from a string representation.

        Attributes:
            string (str): A string representation of a graph

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> tp = TrainsProblem()
        >>> tp.create_graph_from_string('AB5, BC4, CD8, DC8, DE6,\
                                         AD5, CE2, EB3, AE7')
        >>> tp.graph
        {'A': {'B': 5, 'E': 7, 'D': 5}, 'C': {'E': 2, 'D': 8}, 'B': {'C': 4}, 'E': {'B': 3}, 'D': {'C': 8, 'E': 6}}
        """
        try:
            result = {}
            s = string.replace(' ', '')
            l = s.split(',')
            for edge in l:
                src = edge[0]
                dst = edge[1]
                distance = int(edge[2])
                if src not in result:
                    result[src] = {}
                result[src][dst] = distance
            self.graph = result
        except:
            raise ValueError('Invalid format for input string')

    def path_distance(self, path):
        """
        Calculates the distance/weight of a given path

        Attributes:
            path (list): A path

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.path_distance(['A', 'B', 'C'])
        9
        """
        result = 0
        for idx, node in enumerate(path):
            try:
                next_node = path[idx + 1]
                result += self.graph[node][next_node]
            except KeyError:
                raise NoRoute('NO SUCH ROUTE'
                              .format(path), 1)
            except:
                result += 0
        return result

    def bfs_iterator(self, start, end, q):
        """
        Returns a BFS iterator performing a Breadth-First Search (BFS)
        algorithm [1]

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            q (Queue): The queue used to process the nodes
        [1]: https://en.wikipedia.org/wiki/Breadth-first_search
        """
        temp_path = [start]
        q.put(temp_path)
        while not q.empty():
            tmp_path = q.get()
            last_node = tmp_path[len(tmp_path)-1]
            if tmp_path[len(tmp_path)-1] == end:
                yield tmp_path
            for link_node in self.graph[last_node]:
                new_path = []
                new_path = tmp_path + [link_node]
                q.put(new_path)

    def paths_by_maximum_stops(self, start, end, max_stops):
        """
        Calculates the paths between start and end vertices in max_stops steps.
        Note:
            max_stops does not count the origin vertex (path C-D-C is 2 stops)
            No loops allowed (see description)

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            max_stops (int): The maximum number of stops

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_by_maximum_stops('C', 'C', 3)
        [['C', 'D', 'C'], ['C', 'E', 'B', 'C']]
        """
        if max_stops < 0:
            raise ValueError("max_stops must be positive")
        paths = []
        q = Queue.Queue()
        paths_iterator = self.bfs_iterator(start, end, q)
        while True:
            path = paths_iterator.next()
            # Even when not visiting another vertex is a valid solution,
            # this type of solutions are not added to the list since they
            # are not part of the accepted answers
            if len(path) > 1:
                paths += [path]
            if len(path) >= max_stops + 1:
                break
        return paths

    def paths_number_by_maximum_stops(self, start, end, max_stops):
        """
        Calculates the number of paths between start and end vertices in
        max_stops steps.
        Note:
            max_stops does not count the origin vertex (path C-D-C is 2 stops)
            No loops allowed (see description)

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            max_stops (int): The maximum number of stops

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_number_by_maximum_stops('C', 'C', 3)
        2
        """
        return len(self.paths_by_maximum_stops(start, end, max_stops))

    def paths_by_exact_stops(self, start, end, stops_number):
        """
        Calculates the paths between start and end vertices in exactly
        stops_number stesp.

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            stops_number (int): The exact number of stops

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_by_exact_stops('A', 'C', 4)
        [['A', 'B', 'C', 'D', 'C'], ['A', 'D', 'C', 'D', 'C'], ['A', 'D', 'E', 'B', 'C']]
        """
        if stops_number < 0:
            raise ValueError("stops_number must be positive")
        paths = []
        q = Queue.Queue()
        paths_iterator = self.bfs_iterator(start, end, q)
        while True:
            path = paths_iterator.next()
            if len(path) == stops_number + 1:
                paths += [path]
            if len(path) > stops_number + 1:
                break
        return paths

    def paths_number_by_exact_stops(self, start, end, stops_number):
        """
        Calculates the number of paths between start and end vertices in exactly
        stops_number stesp.

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            stops_number (int): The exact number of stops

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_number_by_exact_stops('A', 'C', 4)
        3
        """
        return len(self.paths_by_exact_stops(start, end, stops_number))

    def paths_by_maximum_distance(self, start, end, max_distance,
                                  max_iterations):
        """
        Calculates the paths between start and in maximum max_distance steps and
        in maximum max_iterations iterations (since the graph may contain loops)

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            max_distance (int): The maximum distance
            max_iterations (int): The maximum number of iterations

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_by_maximum_distance('C', 'C', 30, 30)
        [['C', 'D', 'C'], ['C', 'E', 'B', 'C'], ['C', 'D', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'D', 'C'], ['C', 'D', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C']]
        """
        if max_distance < 0:
            raise ValueError("max_distance must be positive")
        if max_iterations < 0:
            raise ValueError("max_iterations must be positive")
        paths = []
        lifo = Queue.Queue()
        paths_iterator = self.bfs_iterator(start, end, lifo)
        i = 0
        while i < max_iterations:
            path = paths_iterator.next()
            if len(path) > 1 and self.path_distance(path) < max_distance:
                paths += [path]
            i += 1
        return paths

    def paths_number_by_maximum_distance(self, start, end, max_distance,
                                         max_iterations):
        """
        Calculates the number of paths between start and in maximum
        max_distance steps and in maximum max_iterations iterations (since the
        graph may contain loops)

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex
            max_distance (int): The maximum distance
            max_iterations (int): The maximum number of iterations

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_number_by_maximum_distance('C', 'C', 30, 50)
        7
        """
        return len(self.paths_by_maximum_distance(start, end, max_distance,
                   max_iterations))

    def heap_shortest_path(self, start, end):
        """
        Find the shortest path between start and end nodes in a graph using
        heaps

        Atributes:
            start (str): The starting vertex
            end (str): The ending vertex

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains.graph = graph
        >>> trains.paths_by_maximum_distance('C', 'C', 30, 30)
        [['C', 'D', 'C'], ['C', 'E', 'B', 'C'], ['C', 'D', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'D', 'C'], ['C', 'D', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C']]
        """
        queue = [(0, start, [])]
        seen = set()
        while True:
            (cost, v, path) = heapq.heappop(queue)
            if v not in seen:
                path = path + [v]
                seen.add(v)
                for (next, c) in self.graph[v].iteritems():
                    heapq.heappush(queue, (cost + c, next, path))
            if v == end and cost != 0:
                return path, cost


def main():
    graph = {'A': {'B': 5, 'D': 5, 'E': 7},
             'B': {'C': 4},
             'C': {'D': 8, 'E': 2},
             'D': {'C': 8, 'E': 6},
             'E': {'B': 3}
             }
    trains = TrainsProblem()
    trains.create_graph_from_string('AB5, BC4, CD8, DC8, DE6,\
                                    AD5, CE2, EB3, AE7')

    print('Output #1: {}'.format(trains.path_distance(['A', 'B', 'C'])))
    print('Output #2: {}'.format(trains.path_distance(['A', 'D'])))
    print('Output #3: {}'.format(trains.path_distance(['A', 'D', 'C'])))
    print('Output #4: {}'
          .format(trains.path_distance(['A', 'E', 'B', 'C', 'D'])))

    try:
        path = trains.path_distance(graph, ['a', 'e', 'd'])
    except:
        path = 'NO SUCH ROUTE'

    print('Output #5: {}'.format(path))

    count = trains.paths_number_by_maximum_stops('C', 'C', 3)
    print('Output #6: {}'.format(count))

    count = trains.paths_number_by_exact_stops('A', 'C', 4)
    print('Output #7: {}'.format(count))

    path, weight = trains.heap_shortest_path('A', 'C')
    print('Output #8: {}'.format(weight))

    path, weight = trains.heap_shortest_path('B', 'B')
    print('Output #9: {}'.format(weight))

    iterations = 50
    count = trains.paths_number_by_maximum_distance('C', 'C', 30, iterations)
    print('Output #10: {}'.format(count))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
