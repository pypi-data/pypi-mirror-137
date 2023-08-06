# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University

"""Test suite for `pyRing.likelihood`
"""

import numpy
from numpy.testing import assert_array_equal

from .. import likelihood


def test_inner_product():
    a = numpy.asarray([  # identity
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    ], dtype=float)
    b = numpy.asarray((0.5, 0.5, 0.))
    assert likelihood.inner_product(a, b) == .5
