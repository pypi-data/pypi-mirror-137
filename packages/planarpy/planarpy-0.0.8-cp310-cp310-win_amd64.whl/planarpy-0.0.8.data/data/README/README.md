# PlanarPy

A fast hp-FEA program for the membrane Poisson equation

```
c(Δu) = -f 
```

using variable order triangle elements (orders 1-20) with heterogeneous p-refinement.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PlanarPy.

```bash
pip install planarpy
```

## Usage

The Mesh object requires a list of point tuples, pts = [(x0,y0), (x1,y1), ...], a list triangle node tuples, cells
= [(0,1,2), (2,5,6), ...], and a base power, pow = 2, to initialize.

Define groups using boolean functions. Always use both coordinates x,y for all function definitions. Groups are used to
define Dirichlet boundary conditions and may also be used to set volume forces on part of the domain. If no group is
chosen when setting a volume force, a default group is used.

```python
from planarpy import Mesh, Dom, sin, cos

# it is up to the user to define points and cells
# either manually or by using a foreign library.
# here the domain is assumed to be [-10, 10]x[-10, 10]
# enable the reverse Cuthill Mckee algorithm (rcm) for 
# increased memory alignment 
mesh = Mesh(pts, cells, 1, rcm=True)

# define groups
outer = mesh.def_group(lambda x, y: x == -10. or x == 10. or y == -10. or y == 10.)
left_half = mesh.def_group(lambda x, y: x <= 0.)

# p-refinement 
mesh.adapt_p(left_half, 10)

# domain setup
dom = Dom(mesh)

# define Dirichlet boundary
dom.set_boundary(outer)
# get the amount of free and constrained degrees of freedom
pos_dofs, neg_dofs = dom.dofs()
# set material constant c
dom.set_consts(1.)
# set boundary condition, default is 0
dom.embed_bcond(lambda x, y: [sin(x) + cos(y)], outer)
# set force in the domain
dom.set_force(lambda x, y: [sin(x) + cos(y)])

# solve
dom.solve()

# measure error with an exact solution
err = dom.err(lambda x, y: [sin(x) + cos(y)])
```

## Plotting

PlanarPy offers three functions in order to extract graphical data in the form of lines

```python
# mesh plot
sys = dom.plot_sys()
# displacement plot with 5 segments per line
disp = dom.plot_disp()
# displacement plot with a given 
# number of segments per line
smooth = dom.plot_smooth(50)
```

The functions return three lists, x, y, z, for line coordinates.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

PlanarPy is licensed under [GNU LGPLv3](https://choosealicense.com/licenses/lgpl-3.0).

This software relies on the [PyO3](https://github.com/PyO3/pyo3) library under
the [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/) license for ffi and on
the [rayon](https://github.com/rayon-rs/rayon) crate under the [MIT](https://choosealicense.com/licenses/mit/#)
and [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)
licenses for parallelism.
