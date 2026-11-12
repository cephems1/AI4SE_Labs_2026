## Task
Implement Money.__bool__ in playground/playground/models.py: """Return True when the amount is non-zero."""

## Target
File `playground/playground/models.py`, class `Money`, method `__bool__`. The method currently is a stub:
```python
def __bool__(self) -> bool:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from typing import Mapping
from .base import Entity
from .enums import Category
from .util import ensure_positive_int, format_cents, normalize_sku
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.880): playground/playground/models.py lines 90-91, method
```python
    def __bool__(self) -> bool:
        pass
```

### Chunk 2 (similarity 0.861): playground/playground/models.py lines 15-21, method
```python
    def __init__(self, cents: int = 0) -> None:
        """Create a monetary amount; cents must be a non-negative ``int``."""
        if isinstance(cents, bool) or not isinstance(cents, int):
            raise TypeError("cents must be int")
        if cents < 0:
            raise ValueError("money cannot be negative")
        self._cents = cents
```

### Chunk 3 (similarity 0.853): playground/playground/models.py lines 48-54, method
```python
    def __mul__(self, factor: int) -> Money:
        """Return ``self`` multiplied by a non-negative integer."""
        if isinstance(factor, bool) or not isinstance(factor, int):
            raise TypeError("factor must be int")
        if factor < 0:
            raise ValueError("factor cannot be negative")
        return Money(self._cents * factor)
```

### Chunk 4 (similarity 0.849): playground/playground/models.py lines 12-91, class
```python
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None: ...
    @property
    def cents(self) -> int: ...
    def __add__(self, other: Money) -> Money: ...
    def __sub__(self, other: Money) -> Money: ...
    def __mul__(self, factor: int) -> Money: ...
    def __rmul__(self, factor: int) -> Money: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: Money) -> bool: ...
    def __le__(self, other: Money) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __bool__(self) -> bool: ...
```

### Chunk 5 (similarity 0.834): playground/playground/models.py lines 72-76, method
```python
    def __le__(self, other: Money) -> bool:
        """Return True if ``self`` is less than or equal to ``other``."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents <= other._cents
```

## Instructions
Write the complete implementation of `Money.__bool__`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.