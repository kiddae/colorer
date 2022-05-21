from setuptools import setup
setup(
    name='colorer',
    version='2.0.0',
    packages=['colorer'],
    entry_points={
        'console_scripts': ['colorer = colorer.colorer:main']
    }
)
