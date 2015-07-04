#!/usr/bin/env py.test
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import pytest
import doctest
import trains


class TestTrains():
    def setup(self):
        self.graph = {'A': {'B': 5, 'D': 5, 'E': 7},
                      'B': {'C': 4},
                      'C': {'D': 8, 'E': 2},
                      'D': {'C': 8, 'E': 6},
                      'E': {'B': 3}
                      }
        self.tp = trains.TrainsProblem()
        self.tp.graph = self.graph

    def test_input_mapping(self):
        g = {'A': {'B': 5, 'D': 5, 'E': 7},
             'B': {'C': 4},
             'C': {'D': 8, 'E': 2},
             'D': {'C': 8, 'E': 6},
             'E': {'B': 3}
             }
        tp = trains.TrainsProblem()
        tp.create_graph_from_string('AB5, BC4, CD8, DC8, DE6,\
                                     AD5, CE2, EB3, AE7')
        assert g == tp.graph

    def test_doctest(self):
        # TODO: Perform doctesting within py.test
        doctest.testmod(trains)

    def test_output01(self):
        assert 9 == self.tp.path_distance(['A', 'B', 'C'])

    def test_output02(self):
        assert 5 == self.tp.path_distance(['A', 'D'])

    def test_output03(self):
        assert 13 == self.tp.path_distance(['A', 'D', 'C'])

    def test_output04(self):
        assert 22 == self.tp.path_distance(['A', 'E', 'B', 'C', 'D'])

    def test_output05(self):
        with pytest.raises(trains.NoRoute):
            self.tp.path_distance(['A', 'E', 'D'])

    def test_output06(self):
        paths = self.tp.paths_by_maximum_stops('C', 'C', 3)
        assert ['C', 'D', 'C'] in paths
        assert ['C', 'E', 'B', 'C'] in paths
        count = self.tp.paths_number_by_maximum_stops('C', 'C', 3)
        assert count == 2

    def test_output07(self):
        paths = self.tp.paths_by_exact_stops('A', 'C', 4)
        assert ['A', 'B', 'C', 'D', 'C'] in paths
        assert ['A', 'D', 'C', 'D', 'C'] in paths
        assert ['A', 'D', 'E', 'B', 'C'] in paths
        count = self.tp.paths_number_by_exact_stops('A', 'C', 4)
        assert count == 3

    def test_output08_normal_flow(self):
        path, weight = self.tp.shortest_path('A', 'C')
        assert 9 == weight

    def test_output08_no_route(self):
        with pytest.raises(trains.NoRoute):
            path, weight = self.tp.shortest_path('A', 'A')

    def test_output09(self):
        path, weight = self.tp.shortest_path('B', 'B')
        assert 9 == weight
        assert len(path) > 1

    def test_output10(self):
        iterations = 30
        paths = self.tp.paths_by_maximum_distance('C', 'C', 30, iterations)
        assert ['C', 'D', 'C'] in paths
        assert ['C', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'D', 'C'] in paths
        assert ['C', 'D', 'C', 'E', 'B', 'C'] in paths
        assert ['C', 'D', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'E', 'B', 'C'] in paths
        assert ['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C'] in paths
        assert len(paths) == 7
