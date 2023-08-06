# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitfolders']

package_data = \
{'': ['*']}

extras_require = \
{'full': ['tqdm']}

entry_points = \
{'console_scripts': ['split-folders = splitfolders.cli:run',
                     'split_folders = splitfolders.cli:run',
                     'splitfolders = splitfolders.cli:run']}

setup_kwargs = {
    'name': 'split-folders',
    'version': '0.5.1',
    'description': 'Split folders with files (e.g. images) into training, validation and test (dataset) folders.',
    'long_description': '# `split-folders` [![Build Status](https://img.shields.io/github/workflow/status/jfilter/split-folders/Test)](https://github.com/jfilter/split-folders/actions/workflows/test.yml) [![PyPI](https://img.shields.io/pypi/v/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/split-folders)](https://pypistats.org/packages/split-folders)\n\nSplit folders with files (e.g. images) into **train**, **validation** and **test** (dataset) folders.\n\nThe input folder should have the following format:\n\n```\ninput/\n    class1/\n        img1.jpg\n        img2.jpg\n        ...\n    class2/\n        imgWhatever.jpg\n        ...\n    ...\n```\n\nIn order to give you this:\n\n```\noutput/\n    train/\n        class1/\n            img1.jpg\n            ...\n        class2/\n            imga.jpg\n            ...\n    val/\n        class1/\n            img2.jpg\n            ...\n        class2/\n            imgb.jpg\n            ...\n    test/\n        class1/\n            img3.jpg\n            ...\n        class2/\n            imgc.jpg\n            ...\n```\n\nThis should get you started to do some serious deep learning on your data. [Read here](https://stats.stackexchange.com/questions/19048/what-is-the-difference-between-test-set-and-validation-set) why it\'s a good idea to split your data intro three different sets.\n\n-   Split files into a training set and a validation set (and optionally a test set).\n-   Works on any file types.\n-   The files get shuffled.\n-   A [seed](https://docs.python.org/3/library/random.html#random.seed) makes splits reproducible.\n-   Allows randomized [oversampling](https://en.wikipedia.org/wiki/Oversampling_and_undersampling_in_data_analysis) for imbalanced datasets.\n-   Optionally group files by prefix.\n-   (Should) work on all operating systems.\n\n## Install\n\nThis package is Python only and there are no external dependencies.\n\n```bash\npip install split-folders\n```\n\nOptionally, you may install [tqdm](https://github.com/tqdm/tqdm) to get get a progress bar when moving files.\n\n```bash\npip install split-folders[full]\n```\n\n## Usage\n\nYou can use `split-folders` as Python module or as a Command Line Interface (CLI).\n\nIf your datasets is balanced (each class has the same number of samples), choose `ratio` otherwise `fixed`.\nNB: oversampling is turned off by default.\nOversampling is only applied to the _train_ folder since having duplicates in _val_ or _test_ would be considered cheating.\n\n### Module\n\n```python\nimport splitfolders\n\n# Split with a ratio.\n# To only split into training and validation set, set a tuple to `ratio`, i.e, `(.8, .2)`.\nsplitfolders.ratio("input_folder", output="output",\n    seed=1337, ratio=(.8, .1, .1), group_prefix=None, move=False) # default values\n\n# Split val/test with a fixed number of items, e.g. `(100, 100)`, for each set.\n# To only split into training and validation set, use a single number to `fixed`, i.e., `10`.\n# Set 3 values, e.g. `(300, 100, 100)`, to limit the number of training values.\nsplitfolders.fixed("input_folder", output="output",\n    seed=1337, fixed=(100, 100), oversample=False, group_prefix=None, move=False) # default values\n```\n\nOccasionally, you may have things that comprise more than a single file (e.g. picture (.png) + annotation (.txt)).\n`splitfolders` lets you split files into equally-sized groups based on their prefix.\nSet `group_prefix` to the length of the group (e.g. `2`).\nBut now _all_ files should be part of groups.\n\nSet `move=True` if you want to move the files instead of copying.\n\n### CLI\n\n```\nUsage:\n    splitfolders [--output] [--ratio] [--fixed] [--seed] [--oversample] [--group_prefix] [--move] folder_with_images\nOptions:\n    --output        path to the output folder. defaults to `output`. Get created if non-existent.\n    --ratio         the ratio to split. e.g. for train/val/test `.8 .1 .1 --` or for train/val `.8 .2 --`.\n    --fixed         set the absolute number of items per validation/test set. The remaining items constitute\n                    the training set. e.g. for train/val/test `100 100` or for train/val `100`.\n                    Set 3 values, e.g. `300 100 100`, to limit the number of training values.\n    --seed          set seed value for shuffling the items. defaults to 1337.\n    --oversample    enable oversampling of imbalanced datasets, works only with --fixed.\n    --group_prefix  split files into equally-sized groups based on their prefix\n    --move          move the files instead of copying\nExample:\n    splitfolders --ratio .8 .1 .1 -- folder_with_images\n```\n\nBecause of some [Python quirks](https://github.com/jfilter/split-folders/issues/19) you have to prepend ` --` afer using `--ratio`.\n\nInstead of the command `splitfolders` you can also use `split_folders` or `split-folders`.\n\n## Development\n\nInstall and use [poetry](https://python-poetry.org/).\n\n## Contributing\n\nIf you have a **question**, found a **bug** or want to propose a new **feature**, have a look at the [issues page](https://github.com/jfilter/split-folders/issues).\n\n**Pull requests** are especially welcomed when they fix bugs or improve the code quality.\n\n## License\n\nMIT\n',
    'author': 'Johannes Filter',
    'author_email': 'hi@jfilter.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jfilter/split-folders',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
