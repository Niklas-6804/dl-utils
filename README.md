# dl-utils: Utilities for Deep Learning with PyTorch

## Content
This package contains mainly loss functions, model definitions and metrics in both functional and modular and (whenever possible) pure PyTorch implementations.


## Subpackages
Currently there are the following subpackages:

* `dlutils.data`: contains data utilities (so far just a dataset for random fake data)
* `dlutils.losses`: extends the losses given in PyTorch itself by a few more loss functions
* `dlutils.metrics`: implements some common metrics
* `dlutils.models`: contains Nd implementations of many popular models
    - `dlutils.models.gans`: contains many basic gan implementations, but so far not for arbitrary dimensions
* `dlutils.optims`: containis additional optimizers
* `dlutils.utils`: contains additional utilities such as tensor operations and module loading

## Note
Most of this code was only tested sparely and not with a proper CI/CD and unittests. I'm currently working on that and any contributions are highly welcomed.
