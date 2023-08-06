from setuptools import setup

setup (
    name='pygments_clingo',
    version='0.1.4',
    license='MIT',
    description='Syntax highlighting for clingo',
    author='Roland Kaminski',
    url='https://github.com/rkaminsk/pygments_clingo',
    packages=['pygments_clingo'],
    install_requires=['pygments'],
    entry_points =
    """
    [pygments.lexers]
    clingolexer = pygments_clingo.clingo:ClingoLexer
    """,
)
