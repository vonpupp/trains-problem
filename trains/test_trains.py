#!/usr/bin/env py.test
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import pytest
import doctest
import trains


class TestTrains():
    """
    TestTrains tests class
    """
    def setup(self):
        """
        TearUp: Creates a TrainsProblem object which is going to be used for the
        rest of the tests.
        """
        self.graph = {'A': {'B': 5, 'D': 5, 'E': 7},
                      'B': {'C': 4},
                      'C': {'D': 8, 'E': 2},
                      'D': {'C': 8, 'E': 6},
                      'E': {'B': 3}
                      }
        self.tp = trains.TrainsProblem()
        self.tp._graph = self.graph

    # Unit tests

    def test_input_mapping(self):
        """
        Input test: Tests the input mapping to a dict of dicts (graph
        representation)
        """
        g = {'A': {'B': 5, 'D': 5, 'E': 7},
             'B': {'C': 4},
             'C': {'D': 8, 'E': 2},
             'D': {'C': 8, 'E': 6},
             'E': {'B': 3}
             }
        tp = trains.TrainsProblem()
        tp.create_graph_from_string('AB5, BC4, CD8, DC8, DE6,\
                                     AD5, CE2, EB3, AE7')
        assert g == tp._graph

    def test_input_mapping_invalid_format_exception(self):
        """
        Input test: Tests the input mapping to a dict of dicts (graph
        representation)
        """
        tp = trains.TrainsProblem()
        with pytest.raises(ValueError):
            tp.create_graph_from_string('AB, BC4, CD8, DC8, DE6,\
                                        AD5, CE2, EB3, AE7')

    def test_doctest(self):
        """
        Doctest test: Tests the docstrings by executing each of them within the
        code
        """
        # TODO: Perform doctesting within py.test
        doctest.testmod(trains)

    def test_output01(self):
        """
        Test case 1: Tests the distance from route A-B-C
        """
        assert 9 == self.tp.path_distance(['A', 'B', 'C'])

    def test_output02(self):
        """
        Test case 2: Tests the distance from route A-D
        """
        assert 5 == self.tp.path_distance(['A', 'D'])

    def test_output03(self):
        """
        Test case 3: Tests the distance from route A-D-C
        """
        assert 13 == self.tp.path_distance(['A', 'D', 'C'])

    def test_output04(self):
        """
        Test case 4: Tests the distance from route A-E-B-C-D
        """
        assert 22 == self.tp.path_distance(['A', 'E', 'B', 'C', 'D'])

    def test_output05(self):
        """
        Test case 5 (exception): Test exception on distance calculation from an
        invalid route A-E-D
        """
        with pytest.raises(trains.NoRoute):
            self.tp.path_distance(['A', 'E', 'D'])

    def test_output06(self):
        """
        Test case 6: Tests the paths by maximum stops number on route C-C with
        at most 3 stops
        """
        paths = self.tp.paths_by_maximum_stops('C', 'C', 3)
        assert ['C', 'D', 'C'] in paths
        assert ['C', 'E', 'B', 'C'] in paths
        count = self.tp.paths_number_by_maximum_stops('C', 'C', 3)
        assert count == 2

    def test_output06_negative_stops_exception(self):
        """
        Test case 6 (exception): Tests the paths by maximum stops with a
        negative number of stops from route C-C
        """
        with pytest.raises(ValueError):
            self.tp.paths_by_maximum_stops('C', 'C', -3)
        with pytest.raises(ValueError):
            self.tp.paths_number_by_maximum_stops('C', 'C', -3)

    def test_output07(self):
        """
        Test case 7: Tests the paths by exact stops number on route A-C with at
        most 4 stops
        """
        paths = self.tp.paths_by_exact_stops('A', 'C', 4)
        assert ['A', 'B', 'C', 'D', 'C'] in paths
        assert ['A', 'D', 'C', 'D', 'C'] in paths
        assert ['A', 'D', 'E', 'B', 'C'] in paths
        count = self.tp.paths_number_by_exact_stops('A', 'C', 4)
        assert count == 3

    def test_output07_negative_stops_exception(self):
        """
        Test case 7 (exception): Tests the paths by exact stops number on route
        A-C with a negative number of stops.
        """
        with pytest.raises(ValueError):
            self.tp.paths_by_exact_stops('A', 'C', -4)
        with pytest.raises(ValueError):
            self.tp.paths_number_by_exact_stops('A', 'C', -4)

    def test_output08_normal_flow(self):
        """
        Test case 8: Tests the shortest path on route A-C
        """
        path, weight = self.tp.shortest_path('A', 'C')
        assert 9 == weight

    def test_output08_no_route(self):
        """
        Test case 8 (exception): Tests the exception on shortest path on route
        A-A
        """
        with pytest.raises(trains.NoRoute):
            path, weight = self.tp.shortest_path('A', 'A')

    def test_output09(self):
        """
        Test case 9: Tests the shortest path on route B-B
        """
        path, weight = self.tp.shortest_path('B', 'B')
        assert 9 == weight
        assert len(path) > 1

    def test_output10(self):
        """
        Test case 10: Tests the paths by maximum distance on route C-C with at
        most 30 units of distance and 50 iterations
        """
        iterations = 50
        paths = self.tp.paths_by_maximum_distance('C', 'C', 30, iterations)
        assert ['C', 'D', 'C'] in paths
        assert ['C', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'D', 'C'] in paths
        assert ['C', 'D', 'C', 'E', 'B', 'C'] in paths
        assert ['C', 'D', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C'] in paths
        assert len(paths) == 7

    def test_output10_negative_distance_exception(self):
        """
        Test case 10 (exception): Tests the paths by maximum distance on route C-C with at
        most -30 units of distance and 50 iterations
        """
        iterations = 50
        with pytest.raises(ValueError):
            self.tp.paths_by_maximum_distance('C', 'C', -30, iterations)

    def test_output10_negative_iterations_exception(self):
        """
        Test case 10 (exception): Tests the paths by maximum distance on route C-C with at
        most 30 units of distance and -50 iterations
        """
        iterations = -50
        with pytest.raises(ValueError):
            self.tp.paths_by_maximum_distance('C', 'C', 30, iterations)


class TestApp():
    """
    App tests class
    """
    def setup(self):
        """
        TearUp: Creates a App instance object which is going to be used for the
        rest of the tests.
        """
        self.app = trains.App()

    def test_shortest_path_error_handler(self):
        """
        Test case 6 (exception): Tests the paths by maximum stops with a
        negative number of stops from route C-C
        """
        test = self.app.shortest_path_error_handler('A', 'A')
        assert test == 'NO SUCH ROUTE'

    def test_read_input_exception(self):
        """
        Test case 6 (exception): Tests the paths by maximum stops with a
        negative number of stops from route C-C
        """
        input_data = self.app.read_input('non-existent-file.txt')
        assert None == input_data


# Functional tests
# Note this is not within the class since it is a fixture


@pytest.mark.parametrize(("filename_expected", "function_to_test"), [
    ("expected_output.txt", trains.main)
])
def test_funcoutput(capfd, filename_expected, function_to_test):
    """
    Functional test: Test input against expected output
    """
    function_to_test()
    resout, reserr = capfd.readouterr()
    expected = open(filename_expected, "r").read()
    assert resout == expected
