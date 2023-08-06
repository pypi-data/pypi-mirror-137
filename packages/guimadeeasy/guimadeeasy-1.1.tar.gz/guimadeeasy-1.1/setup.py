from setuptools import setup, find_packages

setup(
    name="guimadeeasy",
    version="1.1",
    description="this is just a fun challenge for my friend",
    packages=['guimadeeasy'],
    long_description="""

    This is my first package, I think these GUIs are super safe. Prove me wrong :->

    Examples - 

    >>> from guimadeeasy import *
    >>> clock()
    
    >>> from guidmadeasy import *
    >>> wheather()

    >>> from guimadeeasy import *
    >>> calculator()

    >>> from guimadeeasy import *
    >>> notepad()

    >>> from guimadeeasy import *
    >>> todo()

    >>> from guimadeeasy import *
    >>> snake()"""
)
