import toml

from tinvest import __version__


def test_version():
    pyproject = toml.load('pyproject.toml')
    assert __version__ == pyproject['tool']['poetry']['version']
