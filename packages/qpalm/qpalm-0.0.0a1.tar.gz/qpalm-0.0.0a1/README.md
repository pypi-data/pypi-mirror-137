[![Python Wheels](https://github.com/tttapa/QPALM-minimal/actions/workflows/wheel.yml/badge.svg)](https://github.com/tttapa/QPALM-minimal/actions/workflows/wheel.yml)
[![Matlab Package](https://github.com/tttapa/QPALM-minimal/actions/workflows/matlab.yml/badge.svg)](https://github.com/tttapa/QPALM-minimal/actions/workflows/matlab.yml)
[![Test Coverage](https://img.shields.io/endpoint?url=https://tttapa.github.io/QPALM-minimal/Coverage/shield.io.coverage.json)](https://tttapa.github.io/QPALM-minimal/Coverage/index.html)

# Proximal Augmented Lagrangian method for Quadratic Programs

QPALM is a numerical optimization package that finds stationary points of (possibly **nonconvex**) quadratic programs, that is 
```
minimize        ½ xᵀQx + qᵀx

subject to      l ≤ Ax ≤ u
```

## Documentation

The documentation can be found at: <https://tttapa.github.io/QPALM-minimal/Doxygen>  
Examples are included as well: <https://tttapa.github.io/QPALM-minimal/Doxygen/examples.html>

## Installation

To install the Python interface to QPALM, you can download pre-built binaries
from [PyPI](https://pypi.org/project/qpalm/):
```sh
python3 -m pip install qpalm
```

To install the Matlab interface, download `qpalm-matlab.tar.gz` from the 
[releases page](https://github.com/tttapa/QPALM-minimal/releases/latest), and 
extract it into the `~/Documents/MATLAB` folder. As a one-liner:
```sh
wget https://github.com/tttapa/QPALM-minimal/releases/download/0.0.0a1/qpalm-matlab.tar.gz -O- | tar xz -C ~/Documents/MATLAB
```

## Benchmarks

Check out the papers below for detailed benchmark tests comparing QPALM with state-of-the-art solvers.

 * [QPALM: A Newton-type Proximal Augmented Lagrangian Method for Quadratic Programs](https://arxiv.org/abs/1911.02934)
 * [QPALM: A Proximal Augmented Lagrangian Method for Nonconvex Quadratic Programs](https://arxiv.org/abs/2010.02653)

## Citing

If you use QPALM in your research, please cite the following paper:
```bibtex
@inproceedings{hermans2019qpalm,
	author      = {Hermans, B. and Themelis, A. and Patrinos, P.},
	booktitle   = {58th IEEE Conference on Decision and Control},
	title       = {{QPALM}: {A} {N}ewton-type {P}roximal {A}ugmented {L}agrangian {M}ethod for {Q}uadratic {P}rograms},
	year        = {2019},
	volume      = {},
	number      = {},
	pages       = {},
	doi         = {},
	issn        = {},
	month       = {Dec.},
}
```

## License

QPALM is licensed under LGPL v3.0. Some modules are used in this software: 
* LADEL: authored by Ben Hermans and licensed under [LGPL-v3](https://github.com/Benny44/LADEL/blob/master/LICENSE).
* LOBPCG: the version of LOBPCG used here was written by Ben Hermans and licensed under the GNU Lesser General Public License v3.0, see [LOBPCG/LICENSE](https://github.com/Benny44/LOBPCG/blob/master/LICENSE).
* LAPACK: authored by The University of Tennessee and The University of Tennessee Research Foundation, The University of California Berkeley, and The University of Colorado Denver, and licensed under BSD-3, see [here](https://github.com/Reference-LAPACK/lapack/blob/master/LICENSE).
* Minunit: a minimal unit testing framework for C, modified from the version by David Siñuela Pastor and licensed under MIT, see [here](https://github.com/siu/minunit/blob/master/MIT-LICENSE.txt).

