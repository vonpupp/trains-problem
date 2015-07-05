#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

------------------------------------------------------------------------------

See the README.md that is shiped with this code.
"""

import Queue
import heapq


class NoRoute(Exception):
    """
    NoRoute exception.

    Used when there is no way to calculate a distance on a non
    existing route like A-E-D.
    """
    def __init__(self, msg, code):
        """
        Creates a NoRoute exception.

        Params:
            msg (str): Human readable string describing the exception.
            code (int): Exception error code.
        """
        self.msg = msg
        self.code = code


class TrainsProblem:
    """
    TrainsProblem class.

    Implements the solution of the problem proposed by Thoughtworks.

    Attributes:
        _graph (dict): A nested dict containing a graph representation.

    """
    def __init__(self):
        """
        Creates an empty graph.

        Attributes:
            _graph (dict): A nested dict containing a graph representation.
        """
        self._graph = {}

    def create_graph_from_string(self, string):
        """
        Generates a graph from a string representation.

        Params:
            string (str): A string representation of a graph

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> tp = TrainsProblem()
        >>> tp.create_graph_from_string('AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7')
        >>> tp._graph
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
            self._graph = result
        except:
            raise ValueError('Invalid format for input string')

    def path_distance(self, path):
        """
        Calculates the distance/weight of a given path.

        Params:
            path (list): A path

        Returns:
            The distance (int)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> trains.path_distance(['A', 'B', 'C'])
        9
        """
        result = 0
        for idx, node in enumerate(path):
            try:
                next_node = path[idx + 1]
                result += self._graph[node][next_node]
            except KeyError:
                raise NoRoute('NO SUCH ROUTE'
                              .format(path), 1)
            except:
                result += 0
        return result

    def bfs_iterator(self, start, end, q):
        """
        Returns a BFS iterator performing a Breadth-First Search (BFS)
        algorithm [1] from start to end using a queue.

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            q (Queue): The queue used to process the nodes

        Returns:
            The path (list)

        [1]: https://en.wikipedia.org/wiki/Breadth-first_search
        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> q = Queue.Queue()
        >>> i = trains.bfs_iterator('C', 'C', q)
        >>> i.next()
        ['C']
        >>> i.next()
        ['C', 'D', 'C']
        >>> i.next()
        ['C', 'E', 'B', 'C']
        """
        temp_path = [start]
        q.put(temp_path)
        while not q.empty():
            last_path = q.get()
            last_node = last_path[len(last_path)-1]
            if last_path[len(last_path)-1] == end:
                yield last_path
            for link_node in self._graph[last_node]:
                new_path = []
                new_path = last_path + [link_node]
                q.put(new_path)

    def paths_by_maximum_stops(self, start, end, max_stops):
        """
        Calculates the paths between start and end vertices in max_stops steps.
        Note:
            max_stops does not count the origin vertex (path C-D-C is 2 stops)
            No loops allowed (see description)

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            max_stops (int): The maximum number of stops

        Returns:
            The paths with a maximum of stops (list)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
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

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            max_stops (int): The maximum number of stops

        Returns:
            The number of pahts (int) with a maximum stops

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> trains.paths_number_by_maximum_stops('C', 'C', 3)
        2
        """
        return len(self.paths_by_maximum_stops(start, end, max_stops))

    def paths_by_exact_stops(self, start, end, stops_number):
        """
        Calculates the paths between start and end vertices in exactly
        stops_number steps.

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            stops_number (int): The exact number of stops

        Returns:
            The paths with exact stops (list)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
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

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            stops_number (int): The exact number of stops

        Returns:
            The number paths with exact stops (int)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> trains.paths_number_by_exact_stops('A', 'C', 4)
        3
        """
        return len(self.paths_by_exact_stops(start, end, stops_number))

    def paths_by_maximum_distance(self, start, end, max_distance,
                                  max_iterations):
        """
        Calculates the paths between start and in maximum max_distance steps and
        in maximum max_iterations iterations (since the graph may contain loops)

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            max_distance (int): The maximum distance
            max_iterations (int): The maximum number of iterations

        Returns:
            The paths with maximum distance (list)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
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

        Params:
            start (str): The starting vertex
            end (str): The ending vertex
            max_distance (int): The maximum distance
            max_iterations (int): The maximum number of iterations

        Returns:
            The number of paths with maximum distance (int)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> trains.paths_number_by_maximum_distance('C', 'C', 30, 50)
        7
        """
        return len(self.paths_by_maximum_distance(start, end, max_distance,
                   max_iterations))

    def shortest_path(self, start, end):
        """
        Find the shortest path between start and end nodes in a graph using
        heaps

        Params:
            start (str): The starting vertex
            end (str): The ending vertex

        Returns:
            The shortest path (list)

        >>> graph = {'A': {'B': 5, 'D': 5, 'E': 7},
        ...  'B': {'C': 4},
        ...  'C': {'D': 8, 'E': 2},
        ...  'D': {'C': 8, 'E': 6},
        ...  'E': {'B': 3}
        ... }
        >>> trains = TrainsProblem()
        >>> trains._graph = graph
        >>> trains.paths_by_maximum_distance('C', 'C', 30, 30)
        [['C', 'D', 'C'], ['C', 'E', 'B', 'C'], ['C', 'D', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'D', 'C'], ['C', 'D', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C'], ['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C']]
        """
        try:
            path = []
            distance = 0
            queue = [(0, start, [])]
            seen = set()
            while True:
                (distance, vertex, path) = heapq.heappop(queue)
                if vertex not in seen:
                    path = path + [vertex]
                    seen.add(vertex)
                    for (next, last_distance) in self._graph[vertex].iteritems():
                        heapq.heappush(queue, (distance + last_distance, next,
                                               path))
                if vertex == end and distance != 0:
                    return path, distance
        except:
            raise NoRoute('No route from {} to {}'.format(start, end), 2)


class App:
    """
    App class.

    Implements the main App class for the solution of the problem proposed by
    Thoughtworks.

    Attributes:
        trains (TrainsProblem): The instance of the solution class
    """

    def __init__(self):
        """
        Creates an empty app.

        Attributes:
            _trains (TrainsProblem): A TrainsProblem instance
        """
        self._trains = TrainsProblem()

    def path_distance_error_handler(self, path):
        """
        Facade for path_distance method handling error messages when when
        calculating distances on a path.  I personally do not like mixing user
        messages within a library or a class. That should be a responsibility of
        the main code

        Params:
            path (list): The list of vertices

        Returns:
            The path distance or 'NO SUCH ROUTE' if an exception occurs.
        """
        try:
            path = self._trains.path_distance(path)
        except:
            path = 'NO SUCH ROUTE'
        return path

    def shortest_path_error_handler(self, start, end):
        """
        Facade for shortest_path method handling error messages when
        calculating the shortest path between two vertices

        Params:
            start (str): The starting vertex
            end (str): The ending vertex

        Returns:
            The shortest path or 'NO SUCH ROUTE' if an exception occurs.
        """
        try:
            _, result = self._trains.shortest_path(start, end)
        except:
            result = 'NO SUCH ROUTE'
        return result

    def read_input(self, filename):
        """
        Reads the first line of a file given by filename and returns it. If
        something goes wrong it prints a message to the user.

        Params:
            filename (str): The filename of the input file

        Returns:
            The first line of the file
        """
        try:
            input = ''
            with open(filename) as f:
                input = f.readline()
            return str(input)
        except:
            print('Problem reading input, check that input.txt exists\
                   and it is formated correctly as the problem description')

    def run(self):
        """
        App runner (main program)
        """
        input_string = self.read_input('input.txt')
        self._trains.create_graph_from_string(input_string)

        path = self.path_distance_error_handler(['A', 'B', 'C'])
        print('Output #1: {}'.format(path))

        path = self.path_distance_error_handler(['A', 'D'])
        print('Output #2: {}'.format(path))

        path = self.path_distance_error_handler(['A', 'D', 'C'])
        print('Output #3: {}'.format(path))

        path = self.path_distance_error_handler(['A', 'E', 'B', 'C', 'D'])
        print('Output #4: {}'.format(path))

        path = self.path_distance_error_handler(['A', 'E', 'D'])
        print('Output #5: {}'.format(path))

        count = self._trains.paths_number_by_maximum_stops('C', 'C', 3)
        print('Output #6: {}'.format(count))

        count = self._trains.paths_number_by_exact_stops('A', 'C', 4)
        print('Output #7: {}'.format(count))

        result = self.shortest_path_error_handler('A', 'C')
        print('Output #8: {}'.format(result))

        result = self.shortest_path_error_handler('B', 'B')
        print('Output #9: {}'.format(result))

        iterations = 50
        count = self._trains.paths_number_by_maximum_distance('C', 'C', 30,
                                                              iterations)
        print('Output #10: {}'.format(count))


def main():
    import doctest
    doctest.testmod()
    app = App()
    app.run()

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 spelllang=en_us :
