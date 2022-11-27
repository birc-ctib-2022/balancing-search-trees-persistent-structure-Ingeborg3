"""A balanced search tree."""

from __future__ import annotations
from abc import (
    ABC,
    abstractmethod
)
from dataclasses import (
    dataclass, field
)
from typing import (
    Protocol, TypeVar, Generic,
    Optional,
    Any
)


# Some type stuff
class Ordered(Protocol):
    """Types that support < comparison."""

    def __lt__(self: Ord, other: Ord) -> bool:
        """Determine if self is < other."""
        ...


Ord = TypeVar('Ord', bound=Ordered)

# Tree structure


class Tree(Generic[Ord], ABC):
    """Abstract tree."""

    @property
    @abstractmethod
    def value(self) -> Ord:
        """Get the value in the root of the tree."""
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        """Get the height of the tree."""
        ...

    @property
    @abstractmethod
    def left(self) -> Tree[Ord]:
        """Get the left sub-tree."""
        ...

    @property
    @abstractmethod
    def right(self) -> Tree[Ord]:
        """Get the right sub-tree."""
        ...

    @property
    def bf(self) -> int:
        """Get the balance factor."""
        return self.right.height - self.left.height


class EmptyClass(Tree[Ord]):
    """Empty tree."""

    # This is some magick to ensure we never have more
    # than one empty tree.
    _instance: Optional[EmptyClass[Any]] = None

    def __new__(cls) -> EmptyClass[Any]:
        """Create a new empty tree."""
        if cls._instance is None:
            cls._instance = super(EmptyClass, cls).__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        """Return 'Empty'."""
        return "Empty"

    @property
    def value(self) -> Ord:
        """Raise an exception."""
        raise AttributeError("No value on an empty tree")

    @property
    def height(self) -> int:
        """
        Return 0.

        The height of an empty tree is always 0.
        """
        return 0

    @property
    def left(self) -> Tree[Ord]:
        """Return an empty tree."""
        return Empty

    @property
    def right(self) -> Tree[Ord]:
        """Return an empty tree."""
        return Empty

    def __str__(self) -> str:
        """Return textual representation."""
        return "*"


# This is the one and only empty tree
Empty = EmptyClass()


@dataclass(frozen=True)
class InnerNode(Tree[Ord]):
    """
    Inner node in the search tree.

    Inner nodes are "frozen" to make them immutable. For this exercise, we want
    to work with persistent trees, so we cannot modify any existing tree, only
    make new trees that potentially share with existing trees.
    """

    _value: Ord
    _left: Tree[Ord] = Empty
    _right: Tree[Ord] = Empty
    _height: int = field(init=False)  # Don't set in init, fix in post_init.

    def __post_init__(self) -> None:
        """Fix consistency after creation."""
        object.__setattr__(
            self,
            '_height', max(self.left.height, self.right.height) + 1
        )

    @property
    def value(self) -> Ord:
        """Get the value in the root of the tree."""
        return self._value

    @property
    def height(self) -> int:
        """Get the height of the tree."""
        return self._height

    @property
    def left(self) -> Tree[Ord]:
        """Get the left sub-tree."""
        return self._left

    @property
    def right(self) -> Tree[Ord]:
        """Get the right sub-tree."""
        return self._right

    def __str__(self) -> str:
        """Return textual representation."""
        return f"({self.left}, {self.value}[{self.bf}], {self.right})"


def rot_left(n: Tree[Ord]) -> Tree[Ord]:
    """Rotate n left.
    # Test for right-heavy tree where the heaviness comes from the
    # outer grandchild.
    >>> rot_left(InnerNode('A', InnerNode('B'), InnerNode('C', InnerNode('D', InnerNode('E')), InnerNode('F', None, InnerNode('G')))))
    (((*, B[0], *), A[0], ((*, E[0], *), D[0], *)), C[0], (*, F[0], (*, G[0], *)))
    # Hvorfor virker sådan en test ikke?
    """
    n = InnerNode(n.right.value, InnerNode(n.value, n.left, \
        n.right.left), n.right.right)
    return n 


def rot_right(n: Tree[Ord]) -> Tree[Ord]:
    """Rotate n right.""" # NB: The search tree data is implemented as
    # a persistent data structure. I.e., a new search tree (given by a 
    # node that contain nodes) must be returned. 
    n = InnerNode(n.left.value, n.left.left, InnerNode(n.value, n.left.right,\
        n.right))
    return n 


def balance(n: Tree[Ord]) -> Tree[Ord]:
    """Re-organize n to balance it."""
    # Simple rotation solution
    if n.bf <= -2:  # left-heavy.
        if n.left.bf > 0: # left-heavy tree due to inner grand-child. 
            # Left-right double rotation.
            return rot_right(InnerNode(
                n.value, 
                rot_left(n.left),
                n.right
            ))
        # if n.left.bf <= 0: # Left-heavy tree due to outer grandchild. 
        # Right-rotation. 
        return rot_right(n)
    if n.bf >= 2:   # right-heavy
        if n.right.bf < 0: # right-heavy tree due to inner grandchild.
            # Right-left double rotation.
            return rot_left(InnerNode(
                n.value,
                n.left,
                rot_right(n.right)
            ))
        # right-heavy tree due to outer grandchild.
        return rot_left(n)
    return n # if n.bf = -1 or 0 or 1, the tree n is considered 
    # balanced.


def contains(t: Tree[Ord], val: Ord) -> bool:
    """Test if val is in t."""
    while True:
        if t is Empty:
            return False
        if t.value == val:
            return True
        if val < t.value:
            t = t.left
        else:
            t = t.right


def insert(t: Tree[Ord], val: Ord) -> Tree[Ord]:
    """Insert val into t."""
    if t is Empty:
        return InnerNode(val, Empty, Empty)
    if t.value < val:
        return balance(InnerNode(t.value, t.left, insert(t.right, val)))
    if t.value > val:
        return balance(InnerNode(t.value, insert(t.left, val), t.right))
    return t


def rightmost(t: Tree[Ord]) -> Ord:
    """Get the rightmost value in t."""
    assert t is not Empty
    while t.right is not Empty:
        t = t.right
    return t.value


def remove(t: Tree[Ord], val: Ord) -> Tree[Ord]:
    """Remove val from t."""
    if t is Empty:
        return Empty

    if val < t.value:
        return balance(InnerNode(t.value, remove(t.left, val), t.right))
    if val > t.value:
        return balance(InnerNode(t.value, t.left, remove(t.right, val)))

    if t.left is Empty:
        return t.right
    if t.right is Empty:
        return t.left

    x = rightmost(t.left)
    return balance(InnerNode(x, remove(t.left, x), t.right))

# function to determine length of search tree.
# recursive.

def rec_len(node) -> int:
    if node is Empty:
        return 0
    return 1 + len(node.left) + len(node.right)

# tail-recursive version
def tail_rec_len(node, len=0) -> int:
    if node is Empty:
        pass

# tail-recursive version mulig?
