## Task
Implement OrderStateMachine.transition in playground/playground/orders.py: """Return ``target`` if the transition is allowed, else raise."""

## Target
File `playground/playground/orders.py`, class `OrderStateMachine`, method `transition`. The method currently is a stub:
```python
def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
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
### Chunk 1 (similarity 0.893): playground/playground/orders.py lines 35-36, method
```python
    def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        pass
```

### Chunk 2 (similarity 0.887): playground/playground/orders.py lines 31-33, method
```python
    def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool:
        """Return whether ``target`` is reachable from ``source``."""
        return target in OrderStateMachine.allowed_from(source)
```

### Chunk 3 (similarity 0.871): playground/playground/orders.py lines 38-40, method
```python
    def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        """Convenience alias for :meth:`transition`."""
        return self.transition(source, target)
```

### Chunk 4 (similarity 0.854): playground/playground/orders.py lines 98-101, method
```python
    def advance(self, target: OrderStatus) -> None:
        """Transition the order to ``target`` status, raising if not allowed."""
        new_status = self._machine.transition(self._status, target)
        self._status = new_status
```

### Chunk 5 (similarity 0.847): playground/playground/orders.py lines 14-40, class
```python
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""
    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    @staticmethod
    def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]: ...
    def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool: ...
    def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus: ...
    def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus: ...
```

## Instructions
Write the complete implementation of `OrderStateMachine.transition`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.