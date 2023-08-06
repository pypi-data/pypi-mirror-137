# Installation instructions {#installation-md}

## Prerequisites

You'll need a C compiler, CMake, and Make or Ninja. 
To compile the Matlab interface, you need Matlab and MEX as well.

## Download

Download LADEL from <https://github.com/tttapa/LADEL.git> ([direct link](https://github.com/tttapa/LADEL/archive/refs/heads/main.zip)):

```sh
git clone https://github.com/tttapa/LADEL.git --single-branch --depth 1
```
Alternatively, without git
```sh
wget https://github.com/tttapa/LADEL/archive/refs/heads/main.tar.gz -O- | tar xzf -
```

## Matlab installation

### Build

Open a terminal inside of the LADEL repository, and configure and build the 
project:

```sh
cmake -B build -S LADEL -D CMAKE_BUILD_TYPE=Release -D LADEL_WITH_MEX=On -D CMAKE_POSITION_INDEPENDENT_CODE=On
```
```sh
cmake --build build --config Release -j
```

### Install

On Linux, Matlab automatically adds `~/Documents/MATLAB` to the path, so it's easiest install LADEL there:

```sh
cmake --install build --config Release --component mex_interface --prefix ~/Documents/MATLAB
```

### Uninstall

To uninstall LADEL, simply remove the `@ladel` folder from where you installed it:

```sh
rm -r "~/Documents/MATLAB/@ladel"
```

## C/C++ installation

LADEL currently offers no install target for the C/C++ libraries and headers,
but you can easily add it to your own CMake projects using e.g.
`add_subdirectory`. If you do so, include the `LADEL` subfolder (the one with
the `include`, `mex` and `src` directories in it), not the root of the 
directory, which is the developer project (which includes extra warnings, tests,
code coverage, etc.).
