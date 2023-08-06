# realpy-feed

> <https://realpython.com/pypi-publish-python-package/>


The realpy-feed is a basic [web feed](https://en.wikipedia.org/wiki/Web_feed) reader that can download the latest Real Python tutorials from the [Real Python feed](https://realpython.com/contact/#rss-atom-feed).

For more information see the tutorial [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/) on Real Python.

## Installation

You can install the realpy-feed from [PyPI](https://pypi.org/project/realpy-feed/):

```sh
python -m pip install realpy-feed
```

## How to use

The Feed Reader is a command line application, named `realpy-feed`. To see a list of the [latest Real Python tutorials](https://realpython.com/), call the program without any arguments:

    $ realpy-feed
    The latest tutorials from Real Python (https://realpython.com/)
     0 How to Publish an Open-Source Python Package to PyPI
     1 Python "while" Loops (Indefinite Iteration)
     2 Writing Comments in Python (Guide)
     3 Setting Up Python for Machine Learning on Windows
     4 Python Community Interview With Michael Kennedy
     5 Practical Text Classification With Python and Keras
     6 Getting Started With Testing in Python
     7 Python, Boto3, and AWS S3: Demystified
     8 Python's range() Function (Guide)
     9 Python Community Interview With Mike Grouchy
    10 How to Round Numbers in Python
    11 Building and Documenting Python REST APIs With Flask and Connexion - Part 2
    12 Splitting, Concatenating, and Joining Strings in Python
    13 Image Segmentation Using Color Spaces in OpenCV + Python
    14 Python Community Interview With Mahdi Yusuf
    15 Absolute vs Relative Imports in Python
    16 Top 10 Must-Watch PyCon Talks
    17 Logging in Python
    18 The Best Python Books
    19 Conditional Statements in Python

To read one particular tutorial, call the program with the numerical ID of the tutorial as a parameter:

    $ realpy-feed 0
    # How to Publish an Open-Source Python Package to PyPI

    Python is famous for coming with batteries included. Sophisticated
    capabilities are available in the standard library. You can find modules for
    working with sockets, parsing CSV, JSON, and XML files, and working with
    files and file paths.

    However great the packages included with Python are, there are many
    fantastic projects available outside the standard library. These are most
    often hosted at the Python Packaging Index (PyPI), historically known as the
    Cheese Shop. At PyPI, you can find everything from Hello World to advanced
    deep learning libraries.

    [... The full text of the article ...]

You can also call the Python Feed Reader in your own Python code, by importing from the `reader` package:

    >>> from reader import feed
    >>> feed.get_titles("https://realpython.com/atom.xml")
    ['How to Publish an Open-Source Python Package to PyPI', ...]
