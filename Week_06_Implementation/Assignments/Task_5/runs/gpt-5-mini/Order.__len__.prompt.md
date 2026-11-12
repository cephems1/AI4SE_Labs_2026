## Task
Implement Order.__len__ in playground/playground/orders.py: """Return the number of line items."""

## Target
File `playground/playground/orders.py`, class `Order`, method `__len__`. The method currently is a stub:
```python
def __len__(self) -> int:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from typing import Dict, FrozenSet, Iterator, List, Tuple
from .base import PricingStrategy
from .enums import OrderStatus
from .exceptions import DuplicateEntityError, InvalidTransitionError
from .models import Customer, LineItem, Money
from .pricing import FlatPricing
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.894): playground/playground/orders.py lines 158-160, method
```python
    def __len__(self) -> int:
        """Return the number of recorded lines."""
        return len(self._lines)
```

### Chunk 2 (similarity 0.850): playground/playground/orders.py lines 190-192, method
```python
    def __len__(self) -> int:
        """Return the number of logged orders."""
        return len(self._orders)
```

### Chunk 3 (similarity 0.845): playground/playground/orders.py lines 103-104, method
```python
    def __len__(self) -> int:
        pass
```

### Chunk 4 (similarity 0.828): playground/playground/orders.py lines 162-164, method
```python
    def __bool__(self) -> bool:
        """Return True when at least one line has been recorded."""
        return len(self) > 0
```

### Chunk 5 (similarity 0.818): playground/playground/orders.py lines 76-79, method
```python
    @property
    def items(self) -> Tuple[LineItem, ...]:
        """Return a tuple copy of the order's line items."""
        return tuple(self._items)
```

## Instructions
Write the complete implementation of `Order.__len__`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.