"""Testing search tree balancing."""

import random
from st import (
    Ord,
    Tree, Empty,
    insert, remove, contains
)


def test_tree() -> None:
    """Test that we still have a working search tree."""
    x: list[int] = random.sample(range(0, 10), 5)
    t: Tree[int] = Empty
    for i, a in enumerate(x):
        t = insert(t, a)
        for b in x[:i+1]:
            assert contains(t, b)
    for i, a in enumerate(x):
        t = remove(t, a)
        for b in x[:i+1]:
            assert not contains(t, b)
    assert t is Empty


def is_balanced(n: Tree[Ord]) -> bool:
    """Check if this tree is balanced."""
    if n is Empty:
        return True
    return abs(n.left.height - n.right.height) < 2 and \
        is_balanced(n.left) and is_balanced(n.right)


# This will fail, because the tree isn't balanced
def test_balanced() -> None:
    """Test that we have a balanced tree."""
    x: list[int] = random.sample(range(0, 20), 20)
    t: Tree[int] = Empty
    for a in x:
        t = insert(t, a)
        assert is_balanced(t)
    for a in x:
        t = remove(t, a)
        assert is_balanced(t)
    assert t is Empty
