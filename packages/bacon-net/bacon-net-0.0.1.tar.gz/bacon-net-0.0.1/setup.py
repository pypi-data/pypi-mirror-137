from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Explainable neural network'
LONG_DESCRIPTION = 'A neural network architecture for building fully explainable neural network for arithmetic and gradient logic expression approximation.'

# Setting up
setup(
    name="bacon-net",
    version=VERSION,
    author="haishibai (Haishi Bai)",
    author_email="<haishi.bai@live.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['ai', 'explainable', 'gradient logic',
              'approximation', 'formula', 'explainability', 'decision', 'decision making'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
