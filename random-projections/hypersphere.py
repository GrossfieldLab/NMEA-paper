#!/usr/bin/env python3

class HyperSphere:
    """
    This class generates random vectors on a hypersphere of arbitrary dimension
    """

    def __init__(self, ndim=3):
        from numpy.random import default_rng
        self.ndim = ndim
        self.generator = default_rng()


    def vector(self):
        """
        Create a random vector on a self.ndim dimensional unit sphere
        """
        from math import sqrt
        import numpy

        components = self.generator.standard_normal(self.ndim)
        components /= sqrt(numpy.add.reduce(components*components))
        return components
