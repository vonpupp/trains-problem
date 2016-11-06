<!--  vim: set spell: -->
<!--  vim: set spelllang=en_us: -->

# Programming practice: Trains

## Metrics

Build Status (master branch):
[![Travis-CI](https://img.shields.io/travis/vonpupp/trains-problem.svg)](https://travis-ci.org/vonpupp/trains-problem)

Code Quality (master branch):
[![Scrutinizer](https://img.shields.io/scrutinizer/g/vonpupp/trains-problem.svg)](https://scrutinizer-ci.com/g/vonpupp/trains-problem/)

Code Coverage (master branch):
[![Scrutinizer
Coverage](https://img.shields.io/scrutinizer/coverage/g/vonpupp/trains-problem.svg)](https://scrutinizer-ci.com/g/vonpupp/trains-problem/)

Ready Stories: [![Stories in
Ready](https://badge.waffle.io/vonpupp/trains-problem.png?label=ready&title=Ready)](http://waffle.io/vonpupp/trains-problem)

Stories in Progress: [![Stories in
progress](https://badge.waffle.io/vonpupp/trains-problem.png?label=progress&title=Progress)](http://waffle.io/vonpupp/trains-problem)

[![Throughput
Graph](https://graphs.waffle.io/vonpupp/trains-problem/throughput.svg)](https://waffle.io/vonpupp/trains-problem/metrics)

Throughput Graph


## Problem description:

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
 1. The number of different routes from C to C with a distance of less than 30.
    In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC,
    CEBCEBC, CEBCEBCEBC.


Test Input:
For the test input, the towns are named using the first few letters of the
alphabet from A to D.  A route between two towns (A to B) with a distance of 5
is represented as AB5. Graph:

```
AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
```

Expected Output:

```
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
```

---------------------

## My comments:

### Code description:
- I represented each city as a vertex of a weighted graph, where the weight is
  the "track" of "one-way" connecting each city.
  For such abstraction I used a dict of dicts. Given the example data:
  "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7" can be represented as follows:
```python
graph = {'a': {'b': 5, 'd': 5, 'e': 7},
           'b': {'c': 4},
           'c': {'d': 8, 'e': 2},
           'd': {'c': 8, 'e': 6},
           'e': {'b': 3}
        }
```
- I performed a search using a Breadth-First Search (BFS)  algorithm [1]
  packed within an iterator yielding a path at a time.
  [1]: https://en.wikipedia.org/wiki/Breadth-first_search
- The error messages strings such as "NO SUCH ROUTE", are handled by function
  wrappers on the main code. I don't like to bind user messages to methods. The
  methods should return only data or exceptions while the main would behave as
  "user's" code which would handle the messages. I could have done some sort of
  facade class on the main but I thought it was just overkilling.
- I added an error handler for "NO SUCH ROUTE" while getting the shortest path
  on non existing routes. This is not taken into account on the given original
  problem description.
- It is possible that there are some missing error handlers. However it is not
  clear how you intend to test this code, and therefore I found this deliverable
  to meet a good balance of error handling.
- I thought of using properties for the classes but it didn't look worthing of
  doing it for this example.
- I modeled the problem as one class: TrainsProblem. Each method has its own
  docstring documenting it. An html folder accompanies the deliverable with the
  full documentation.
- I modeled the main program as one class: App. Each method has its own
  docstring documenting it as well. The documentation can be found also in the
  html folder.
- Each method is documented using docstrings (which are also testable). You can
  use introspection to get the documentation, to do so, using python or ipython
  console type:
```
import trains
help(trains)
```
- The API is documented using epydoc (see html folder for details)
- The program contains one exception class: NoRoute raised whenever the "NO SUCH
  ROUTE" should appear, a wrapper on top of this shows the error string on
  user's code.
- Tests coverage is 99% (see htmlcov folder for details)
- Documentation coverage is 95.5% on file trains.py (module docstring missing)
- Documentation coverage is 96.2% on file test_trains.py (module docstring
  missing)


### Assumptions:
- I used the Queue and heapq modules. I don't think this break the rules
  since is part of the standard python library. By external libs I understand
  pip libs.
  I prioritized readability over efficiency since time/efficiency is not a
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
  out of the box, but I haven't tried it out.
- I used pytest for testing instead of the regular testing framework. I feel
  pytest more pythonic.
- This is made in python2 and it should run in python2, I haven't tested it out
  on python3.
- I thought about adding Sphinx documentation but I thought it was overkilling.
  Having docstrings for the size of this project is enough. However I documented
  the program with epydoc. Note that epydoc is not shipped within the
  requirements.txt file, if the documentation needs to be updated consider
  including it. To update the documentation use:
```sh
epydoc trains.py test_trains.py
```


### Code checkups:
- PEP8 compliant (except for some one-line docstrings outputs)
- Doctest passing with 95.5% and 96.2% coverage for trains.py and test_trains.py
  respectively.
  - To check the coverage install via pip the ``docstring-coverage`` package and
    run the test with:
```sh
docstring-coverage trains.py
docstring-coverage test_trains.py
```
- Pytest passing with 99% including unit and functional tests.
  - To check the coverage install via pip the ``pytest-cov`` package and run the
    test with:
```sh
py.test --cov trains.py
```

### How to prepare the environment (pre-requisite to run the code).

Depending on your distro you may use virtualenv instead of virtualenv2 and pip
instead of pip2 binaries. I assume Arch Linux which is the distro I'm using and
python2 binary.

- Unzip
```sh
unzip trains.zip
```
- Create the environment:
```sh
virtualenv2 .env
```
- Activate the environment if not active:
```sh
source .env/bin/activate
```
- Install py.test:
```sh
pip2 install -r requirements.txt
```

### How to run this code:
- Edit the input.txt file and write a valid graph. Example:
```
  AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
```
- Activate the environment if not active:
```sh
source .env/bin/activate
```

- Execute the program at the prompt (assuming Linux)
    * Option 1. Output on stdout:
```sh
./trains.py
```
    * Option 2. Output on stdout + file:
```sh
./trains.py | tee output.txt
```

### How to run the tests:
- To test the code using py.test:
```sh
./test_trains.py
```
- To test the docstrings using doctest:
```sh
python -m doctest trains.py -v
```
