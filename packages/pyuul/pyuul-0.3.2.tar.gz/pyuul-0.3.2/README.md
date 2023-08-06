![logo](docs/_static/logo_small.png)

---

## About PyUUL

PyUUL is a Python library designed to process 3D-structures of macromolecules, such as PDBs, translating them into fully differentiable data structures. These data structures can be used as input for any modern neural network architecture. Currently, the user can choose between three different types of data representation: voxel-based, surface point cloud and volumetric point cloud.

If you use PyUUL in your research, please consider citing:
**LINK**

## Installation

We recommend using PyUUL with Python 3.6 or above. 
Package installation should only take a few minutes with any of these methods (conda, pip, source).

### Installing PyUUL with [Anaconda](https://www.anaconda.com/download/):

```sh
 conda install -c grogdrinker pyuul 
```

### Installing PyUUL with pip:

```sh
pip install pyuul
```

### Installing PyUUL from source:

If you want to install PyUUL from this repository, you need to install the dependencies first.
First, install [PyTorch](https://pytorch.org/get-started/locally/). The library is currently compatible with PyTorch versions between 0.4.1 and 1.8.0. We will continue to update PyUUL to be compatible with the latest version of PyTorch.
You can also install Pytorch with the following command:

```sh
conda install pytorch -c pytorch
```

In addition, PyUUL requires: scipy, numpy and scikit-learn. Please make sure you have these already installed. Otherwise, you can use the following command:

```sh
conda install scipy numpy scikit-learn
```

Finally, you can clone the repository with the following command:

```sh
git clone https://bitbucket.org/grogdrinker/pyuul/
```

## Documentation

The documentation for PyUUL is available https://pyuul.readthedocs.io/modules.html

## Quickstart

We provide a quickstart example to show how to easily build a 3D representation of biological structures with PyUUL.
The quickstart is available https://pyuul.readthedocs.io/quickstart.html#


## Tutorials

Tutorials for pyUUL are available https://pyuul.readthedocs.io/examples/index.html

We recommend the tutorials to be run on a machine with a GPU, as they will take longer when run on a CPU machine.

The benchmarking folder contains data to reproduce the results of the paper, as well as the network architecture we used for GTP pose optimization and protein classification. 

## Help

For bug reports, features addition and technical questions please contact gabriele.orlando@kuleuven.be
