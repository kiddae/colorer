from setuptools import setup
setup(
    name='colorer',
    version='1.6.0',
    packages=['colorer'],
    entry_points={
        'console_scripts': ['colorer = colorer.__main__:main']
    }
)
