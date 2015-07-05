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


---------------------
Comments from Albert:
---------------------


Code description:
---------------------
- I represented each city as a vertex of a weighted graph, where the weight is
  the "track" of "one-way" connecting each city.
  For such abstraction I used a dict of dicts. Given the example data:
  "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7" can be represented as follows:
     graph = {'a': {'b': 5, 'd': 5, 'e': 7},
              'b': {'c': 4},
              'c': {'d': 8, 'e': 2},
              'd': {'c': 8, 'e': 6},
              'e': {'b': 3}
- I performed a search using a Breadth-First Search (BFS)  algorithm [1]
  packed within an iterator yielding a path at a time.
  [1]: https://en.wikipedia.org/wiki/Breadth-first_search
- The error messages strings such as "NO SUCH ROUTE", are handled by function
  wrappers on the main code. I don't like to bind user messages to methods. The
  methods should return only data or exceptions while the main would behave as
  "user's" code which would handle the messages. I could have done some sort of
  facade class on the main but I thought it was just overkilling.
- I added an error handler for "NO SUCH ROUTE" while getting the shortest path
  on non existing routes. This is not taken into account on the given
  description
- It is possible that there are some missing error handlers. However it is not
  clear how you intend to test this code, and therefore I found this deliverable
  to meet a good balance of error handling.
- I thought of using properties for the classes but it didn't look worthing of
  doing it for this example.


Assumptions:
---------------------
- I used the Queue and heapq modules. I don't think this break the rules
  since is part of the standard python library. By external libs I understand
  pip libs.
  I priorized readability over efficiency since time/efficiency is not a
  constraint of the problem. Performance improvements can be done to this code.
- Since the graph has loops to implement the last type of feature the
  algorithm could enter a loop as in fact happens when not limited to a
  number of iterations. Therefore a max_iterations parameter has been added.
- The input is read from input.txt. Only the FIRST line is considered as input,
  the rest of the file is silently ignored. I assumed that the prefix "Graph:"
  is not part of the input. It wasn't clear for me from the description if it
  should have been considered or not.
- The output is written on stdout (the console). It wasn't clear for me from the
  description if I had to write to an output file, if it is the case then just
  run the code as: ``./trains.py | tee output.txt``.
- I made the program in Linux, I haven't tried it out on Windows, it should work
  out of the box, but I haven't tried it out
- I used pytest for testing instead of the regular testing framework. I feel
  pytest more pythonic
- This is made in python2 and it should run in python2, I haven't tested it out
  on python3


Code checkups:
---------------------
- PEP8 compliant (except for some oneline docstrings outputs)
- Doctest passing
- Pytest passing (unit + functional tests)


How to prepare the environment (pre-requisite to run the code). Assuming python2
and archlinux:
---------------------
- Unzip
    ``unzip trains.zip``
- Change directory
    ``cd trains``
- Create the environment:
    ``virtualenv2 .env``
- Activate the environment if not active:
    ``source .env/bin/activate``
- Install py.test:
    ``pip2 install -r requirements.txt``

Note: Depending on your distro you may use virtualenv instead of virtualenv2 and
pip instead of pip2. I assume archlinux which is the distro I'm using and
python2.


How to run this code:
---------------------
- Edit the input.txt file and write a valid graph. Example:
  AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
- Execute the program at the prompt (assuming Linux)
    * Option 1. Output on stdout:
        ``./trains.py``
    * Option 2. Output on stdout + file:
        ``./trains.py | tee output.txt``
"""

import Queue
import heapq


class NoRoute(Exception):
    """
    NoRoute exception.

    Used when there is no way to calculate a distance on a non
    existing route like A-E-D.

    Params:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """
    def __init__(self, msg, code):
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

        Params:
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
        >>> tp.create_graph_from_string('AB5, BC4, CD8, DC8, DE6,\
                                         AD5, CE2, EB3, AE7')
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


def main():
    def path_distance_error_handler(trains, path):
        """
        Handle user messages when calculating distances on a path.
        I personally do not like mixing user messages within a library or a
        class. That should be a responsibility of the main code

        Params:
            trains (TrainsProblem): The TrainsProblem object
            path (list): The list of vertices

        Returns:
            The path distance or 'NO SUCH ROUTE' if an exception occurs.
        """
        try:
            path = trains.path_distance(path)
        except:
            path = 'NO SUCH ROUTE'
        return path

    def shortest_path_error_handler(trains, start, end):
        """
        Handle user messages when calculating the shortest path between two
        vertices

        Params:
            trains (TrainsProblem): The TrainsProblem object
            start (str): The starting vertex
            end (str): The ending vertex

        Returns:
            The shortest path or 'NO SUCH ROUTE' if an exception occurs.
        """
        try:
            _, result = trains.shortest_path(start, end)
        except:
            result = 'NO SUCH ROUTE'
        return result

    def read_input(filename):
        """
        Handle user messages when calculating the shortest path between two
        vertices

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

    input_string = read_input('input.txt')
    trains = TrainsProblem()
    trains.create_graph_from_string(input_string)

    path = path_distance_error_handler(trains, ['A', 'B', 'C'])
    print('Output #1: {}'.format(path))

    path = path_distance_error_handler(trains, ['A', 'D'])
    print('Output #2: {}'.format(path))

    path = path_distance_error_handler(trains, ['A', 'D', 'C'])
    print('Output #3: {}'.format(path))

    path = path_distance_error_handler(trains, ['A', 'E', 'B', 'C', 'D'])
    print('Output #4: {}'.format(path))

    path = path_distance_error_handler(trains, ['A', 'E', 'D'])
    print('Output #5: {}'.format(path))

    count = trains.paths_number_by_maximum_stops('C', 'C', 3)
    print('Output #6: {}'.format(count))

    count = trains.paths_number_by_exact_stops('A', 'C', 4)
    print('Output #7: {}'.format(count))

    result = shortest_path_error_handler(trains, 'A', 'C')
    print('Output #8: {}'.format(result))

    result = shortest_path_error_handler(trains, 'B', 'B')
    print('Output #9: {}'.format(result))

    iterations = 50
    count = trains.paths_number_by_maximum_distance('C', 'C', 30, iterations)
    print('Output #10: {}'.format(count))

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 spelllang=en_us :
