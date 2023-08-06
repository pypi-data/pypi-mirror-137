[![ci-cd](https://github.com/UBC-MDS/coordgeompy/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/coordgeompy/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/UBC-MDS/CoordGeomPy/branch/main/graph/badge.svg?token=9jgbpldNoe)](https://codecov.io/gh/UBC-MDS/CoordGeomPy)
[![Documentation Status](https://readthedocs.org/projects/coordgeompy/badge/?version=latest)](https://coordgeompy.readthedocs.io/en/latest/?badge=latest)

# coordgeompy

A simple coordinate geometry helper package. This package is developed for the UBC MDS DSCI 524 Collaborative Software Development course at the University of British Columbia.

## Overview

This starter package allows users to perform various geometric operations like calculate distance between two parallel lines, distance between two n dimensional vectors, intersection of lines in 3-Dimensional space and so on. Our motivation in creating this package was to allow users with minimal experience in python coding to be able to perform these geometric calculations easily.
## Installation

```bash
$ pip install git+https://github.com/UBC-MDS/CoordGeomPy.git@v1.0.0
```

## Features

There are four main functions planned for development as outlined below. Additional functions may be added in the future.

Function 1 `dist_pll_lines_2d`: This function allows a user to calculate the distance between two parallel lines. This is the distance between the points where a perpendicular line intersects between the two parallel lines. This function will find that distance (d).

Function 2 `get_distance`: This function allows a user to calculate the the distance between two n dimensional vectors. Possible metrics that can be used with this function includes: Euclidean, Manhattan, Chebyshev, or Minkowski

Function 3 `is_intersection_3d`: This function allows a user to determine whether two infinite lines intersect in 3-dimensional space. The function will return True or False based on the input arguments.

Function 4 `is_orthogonal`: This function allows a user to determine whether two infinite lines are perpendicular in n-dimensional space. The function will return True or False based on the input arguments.

While we are not really reinventing the wheel on coordinate geometry calculations with our package, we used this as an opportunity to gain some experience in understanding how these calculations function in python language. There are existing packages that execute similar functions. For example, [SymPy](https://www.sympy.org/en/index.html) is a Python library that contains comprehensive mathematical functions including intersection of lines, shortest distance between a point and a line etc. We also found a package [coordinate-geometry 1.0.02](https://pypi.org/project/coordinate-geometry/) that had similar functions to calculating distance between two points, a point and a line, area of a triangle etc. [Scipy's](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html) `scipy.spatial.distance.cdist` functions similarly to Function 2. 
## Usage

```
import numpy as np
from coordgeompy.coordgeompy import dist_pll_lines_2d
from coordgeompy.coordgeompy import get_distance
from coordgeompy.coordgeompy import is_intersection_3d
from coordgeompy.coordgeompy import is_orthogonal

x1 <- c(1, 2, 3, 4)
x2 <- c(5, 6, 7, 8)
get_distance(x1, x2, metric="Euclidean")
```

## Documentation 

The official documentation is hosted on [Read the Docs](https://coordgeompy.readthedocs.io/en/latest/)
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Contributors

We welcome and recognize all contributors. Names and GitHub @usernames listed below:

- Arlin Cherian: @arlincherian
- Nico Van Den Hooff: @nicovandenhooff
- Zheren Xu: @ZherenXu
- Jordan Casoli: @jcasoli

## License

`coordgeompy` was created by Jordan Casoli, Nico Van Den Hooff, Arlin Cherian and Zheren Xu. It is licensed under the terms of the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Credits

`coordgeompy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
