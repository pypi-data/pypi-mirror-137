# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reader']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.8,<7.0.0', 'html2text>=2020.1.16,<2021.0.0']

entry_points = \
{'console_scripts': ['realpy-feed = reader.__main__:main']}

setup_kwargs = {
    'name': 'realpy-feed',
    'version': '0.1.0',
    'description': 'Read the latest Real Python tutorials',
    'long_description': '# realpy-feed\n\n> <https://realpython.com/pypi-publish-python-package/>\n\n\nThe realpy-feed is a basic [web feed](https://en.wikipedia.org/wiki/Web_feed) reader that can download the latest Real Python tutorials from the [Real Python feed](https://realpython.com/contact/#rss-atom-feed).\n\nFor more information see the tutorial [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/) on Real Python.\n\n## Installation\n\nYou can install the realpy-feed from [PyPI](https://pypi.org/project/realpy-feed/):\n\n```sh\npython -m pip install realpy-feed\n```\n\n## How to use\n\nThe Feed Reader is a command line application, named `realpy-feed`. To see a list of the [latest Real Python tutorials](https://realpython.com/), call the program without any arguments:\n\n    $ realpy-feed\n    The latest tutorials from Real Python (https://realpython.com/)\n     0 How to Publish an Open-Source Python Package to PyPI\n     1 Python "while" Loops (Indefinite Iteration)\n     2 Writing Comments in Python (Guide)\n     3 Setting Up Python for Machine Learning on Windows\n     4 Python Community Interview With Michael Kennedy\n     5 Practical Text Classification With Python and Keras\n     6 Getting Started With Testing in Python\n     7 Python, Boto3, and AWS S3: Demystified\n     8 Python\'s range() Function (Guide)\n     9 Python Community Interview With Mike Grouchy\n    10 How to Round Numbers in Python\n    11 Building and Documenting Python REST APIs With Flask and Connexion - Part 2\n    12 Splitting, Concatenating, and Joining Strings in Python\n    13 Image Segmentation Using Color Spaces in OpenCV + Python\n    14 Python Community Interview With Mahdi Yusuf\n    15 Absolute vs Relative Imports in Python\n    16 Top 10 Must-Watch PyCon Talks\n    17 Logging in Python\n    18 The Best Python Books\n    19 Conditional Statements in Python\n\nTo read one particular tutorial, call the program with the numerical ID of the tutorial as a parameter:\n\n    $ realpy-feed 0\n    # How to Publish an Open-Source Python Package to PyPI\n\n    Python is famous for coming with batteries included. Sophisticated\n    capabilities are available in the standard library. You can find modules for\n    working with sockets, parsing CSV, JSON, and XML files, and working with\n    files and file paths.\n\n    However great the packages included with Python are, there are many\n    fantastic projects available outside the standard library. These are most\n    often hosted at the Python Packaging Index (PyPI), historically known as the\n    Cheese Shop. At PyPI, you can find everything from Hello World to advanced\n    deep learning libraries.\n\n    [... The full text of the article ...]\n\nYou can also call the Python Feed Reader in your own Python code, by importing from the `reader` package:\n\n    >>> from reader import feed\n    >>> feed.get_titles("https://realpython.com/atom.xml")\n    [\'How to Publish an Open-Source Python Package to PyPI\', ...]\n',
    'author': 'Xavier Young',
    'author_email': '45989017+younger-1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/younger-1/realpy-feed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
