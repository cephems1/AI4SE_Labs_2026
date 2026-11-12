## Task
Implement OrderLog.by_status in playground/playground/orders.py: """Yield orders whose status matches ``status``."""

## Target
File `playground/playground/orders.py`, class `OrderLog`, method `by_status`. The method currently is a stub:
```python
def by_status(self, status: OrderStatus) -> Iterator[Order]:
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
### Chunk 1 (similarity 0.886): playground/playground/orders.py lines 183-184, method
```python
    def by_status(self, status: OrderStatus) -> Iterator[Order]:
        pass
```

### Chunk 2 (similarity 0.831): playground/playground/orders.py lines 194-196, method
```python
    def __iter__(self) -> Iterator[Order]:
        """Iterate over the logged orders."""
        yield from list(self._orders)
```

### Chunk 3 (similarity 0.826): playground/playground/orders.py lines 71-74, method
```python
    @property
    def status(self) -> OrderStatus:
        """Return the current order status."""
        return self._status
```

### Chunk 4 (similarity 0.822): playground/playground/orders.py lines 167-196, class
```python
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None: ...
    def record(self, order: Order) -> None: ...
    def by_status(self, status: OrderStatus) -> Iterator[Order]: ...
    def __getitem__(self, index: int) -> Order: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Order]: ...
```

### Chunk 5 (similarity 0.799): playground/playground/orders.py lines 186-188, method
```python
    def __getitem__(self, index: int) -> Order:
        """Return the order at ``index``."""
        return self._orders[index]
```

## Instructions
Write the complete implementation of `OrderLog.by_status`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.