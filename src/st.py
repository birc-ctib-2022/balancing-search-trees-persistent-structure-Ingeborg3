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
    """Rotate n left."""
    ...
    return n


def rot_right(n: Tree[Ord]) -> Tree[Ord]:
    """Rotate n right."""
    ...
    return n


def balance(n: Tree[Ord]) -> Tree[Ord]:
    """Re-organize n to balance it."""
    # Simple rotation solution
    if n.bf <= -2:  # left-heavy
        return rot_right(n)
    if n.bf >= 2:   # right-heavy
        return rot_left(n)
    return n


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
