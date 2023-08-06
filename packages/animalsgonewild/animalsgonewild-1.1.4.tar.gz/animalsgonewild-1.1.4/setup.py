# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['animalsgonewild']

package_data = \
{'': ['*'], 'animalsgonewild': ['images/*', 'imgs/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'codecov>=2.1.12,<3.0.0',
 'newspaper3k>=0.2.8,<0.3.0',
 'nltk>=3.6.7,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'wordcloud>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'animalsgonewild',
    'version': '1.1.4',
    'description': 'Behaves like the text equivalent of an animal inspired Instagram filter',
    'long_description': '# animalsgonewild\n\n[![codecov](https://codecov.io/gh/UBC-MDS/animalsgonewild/branch/main/graph/badge.svg?token=tGLNiVr2OZ)](https://codecov.io/gh/UBC-MDS/animalsgonewild) [![ci-cd](https://github.com/UBC-MDS/animalsgonewild/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/animalsgonewild/actions/workflows/ci-cd.yml) [![Docs](https://readthedocs.org/projects/animalsgonewild/badge/?version=latest)](https://animalsgonewild.readthedocs.io/en/latest/index.html)\n\nThis package is designed to demonstrate how basic features of text analysis can be utilized to analyze and represent a text file or string while applying a humorous lens (because what is data science without a dash of humor!). It counts the number of words from a text, calculates the average word length of that text, and returns an animal image corresponding to the average word length. It subsequently transforms the text into a wordcloud in the shape of the animal. We have included a bonus fourth function for fun, inspired by the popular childhood game - MadLibs.\n\n# Contributors\n\nKyle Maj, Nagraj Rao, Morgan Rosenberg, Junrong Zhu\n\n## Installation\n\n```bash\npip install git+https://github.com/UBC-MDS/animalsgonewild\n```\n\n## Usage\n\nThis package can be used in conjunction with any code to read in multiple text files to analyze and compare whole corpuses (your software must call the Animals Gone Wild functions for each text variable).\n\n### Function 1: animalClassifier\n\nThis function takes a sequence of text(str), counts the words in the string, and then returns an animal type (str).\n\n### Function 2: animalType\n\nThis function takes a sequence of text(str)  and a species (str), determines the average word length (proxy for language complexity), and returns an smart looking animal image (jpg) corresponding to the average word length.\n\n### Function 3: wordcloud\n\nThis function takes a sequence of text(str) and an animal image (jpg), and returns a wordcloud in the shape of the species comprised of the sequence of text (jpg).\n\n### Function 4: textTransformer\n\nThis function takes a sequence of text(str) and a species(str), and returns a new text sequence where all proper nouns are replaced with the species.\n\n### Fit within the Python ecosystem\n\nWhile other fun packages with animal images exist, most are very basic. For example, the animal-cuties script (<https://pypi.org/project/animal-cuties/#description>) generates animal images (e.g. animal-cuties cat). However, we were unable to find any interactive, multidimensional comedic relief package, where users can input information, and receive dynamic humorous feedback in the form of cute and/or hilarious animals. Given how much time we all are spending in front of a computer screen during the pandemic, this package is an essential addition to the ecosystem promoting mental wellness through humor. By offering it as a package rather than a script, we also empower other developers to integrate this is as a fun injection to their coding projecs.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`animalsgonewild` was created by DSCI 524 - Team 16:\nNagraj Rao, Junrong Zhu, Kyle Maj, Morgan Rosenberg\n\nIt is licensed under the terms of the MIT license.\n\n## Credits\n\n`animalsgonewild` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n# Easter egg #1\n\nDid you know the name of our package was almost called "whattheduck"?\n\n# Easter egg #2\n\nGot any carrots?\n\n# Easter egg #3\n\nAren\'t we pretty?\n',
    'author': 'DSCI 524 - Team 16',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
