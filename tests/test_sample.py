"""Sample test file to verify pytest setup."""

import pytest


def test_sample():
    """A simple test to verify pytest is working."""
    assert 1 + 1 == 2


def test_environment():
    """Test that we can import our package."""
    import src
    assert hasattr(src, "__version__")


class TestSampleClass:
    """Sample test class."""
    
    def test_something(self):
        """Test method in a class."""
        result = "hello".upper()
        assert result == "HELLO"
    
    def test_something_else(self):
        """Another test method."""
        numbers = [1, 2, 3, 4, 5]
        assert sum(numbers) == 15


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_parametrized(input, expected):
    """Example of a parametrized test."""
    assert input * 2 == expected
