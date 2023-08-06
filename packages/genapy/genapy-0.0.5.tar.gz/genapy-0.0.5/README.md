# gapy

Genetic algorithm for Python 3.

## What is this?

This algorithm is simply a class which can be directly implemented in your project.

### Required Packages

You will need the following packages to run this algorithm (also listed in `src/gapy/requirements.txt`)

```
numpy
pandas
scipy
```

Pandas is only used for aesthetic reasons on the `write` method for the printing and is entirely optional. To remove this feature, simply comment out the method and set logging to False.

### Instalation

A testing version is available in PyPI:

`pip3 install genapy`

### How to use

The file `test.py` presents an example on how to use this algorithm. It requires a fitness function, which must receive a numpy array containing the population on each line, each composed of real numbers, and output a numpy vector with the fitness of each individual as a real number.

Probabilities for crossover or mutation are numbers in the interval [0,1] and set by the parameters `crossover` and `mutation` respectively. They both default to 0.5.

The output range of each parameter used to make up the individual can be scaled separately by passing a numpy array containing the upper and lower bounds in the shape (k,2), where k is the number of parameters (`chromosome_size`), and also setting `has_mask` to True.

The number of bits for each parameter can also be set as an integer in `resolution`.

A printing delay for the `write` method is set by passing the desired value in seconds on `time_print`.
