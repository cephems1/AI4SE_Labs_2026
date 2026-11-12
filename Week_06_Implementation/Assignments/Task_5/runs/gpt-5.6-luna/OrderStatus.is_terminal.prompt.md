## Task
Implement OrderStatus.is_terminal in playground/playground/enums.py: """True when the status ends further transitions."""

## Target
File `playground/playground/enums.py`, class `OrderStatus`, method `is_terminal`. The method currently is a stub:
```python
@property
def is_terminal(self) -> bool:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from enum import Enum
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.876): playground/playground/enums.py lines 45-47, method
```python
    @property
    def is_terminal(self) -> bool:
        pass
```

### Chunk 2 (similarity 0.852): playground/playground/enums.py lines 37-47, class
```python
class OrderStatus(Enum):
    """Lifecycle stages for an order."""
    NEW = "new"
    RESERVED = "reserved"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    @property
    def is_terminal(self) -> bool: ...
```

### Chunk 3 (similarity 0.775): playground/playground/orders.py lines 35-36, method
```python
    def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        pass
```

### Chunk 4 (similarity 0.773): playground/playground/orders.py lines 24-29, method
```python
    @staticmethod
    def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]:
        """Return the set of statuses reachable from ``status``."""
        if not isinstance(status, OrderStatus):
            raise TypeError("status must be OrderStatus")
        return OrderStateMachine.TRANSITIONS[status]
```

### Chunk 5 (similarity 0.772): playground/playground/orders.py lines 14-40, class
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
Write the complete implementation of `OrderStatus.is_terminal`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.