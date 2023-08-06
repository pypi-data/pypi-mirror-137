#!/bin/env python
# -*- coding: utf-8 -*-
"""test Queue
    by Valentyn Stadnytskyi
     created: August 2, 2019
    This is a test library to evaluate the performance of the code.
    Queue is an abstract data structure, somewhat similar to Stacks.
    Unlike stacks, a queue is open at both its ends.
    One end is always used to insert data (enqueue)
    and the other is used to remove data (dequeue)

    to run unittest: python3 -m unittest test_queue
"""

import unittest
import logging
# from numpy.testing import assert_, assert_almost_equal, assert_equal

from .. import numerical

class ImageTest(unittest.TestCase):

    def test_distance_matrix(self):
        """
        various build-in attributes.
        """
        import numpy as np
        row = np.asarray([100,200,400])
        col = np.asarray([100,200,300])
        dist = numerical.distance_matrix(row = row,col = col)
        result = np.array([[  0.        , 141.42135624, 360.55512755],
           [141.42135624,   0.        , 223.60679775],
           [360.55512755, 223.60679775,   0.        ]])
        self.assertEqual((np.around(dist,3)==np.around(result,3)).all(),True)

    def test_nearest_neibhour(self):
        import numpy as np
        row = np.asarray([100,200,400])
        col = np.asarray([100,200,300])
        nn = numerical.nearest_neibhour(row = row,col = col)
        result = np.array([[0, 1, 2],
           [1, 0, 2],
           [2, 1, 0]])
        self.assertEqual((np.around(nn,3)==np.around(result,3)).all(),True)
