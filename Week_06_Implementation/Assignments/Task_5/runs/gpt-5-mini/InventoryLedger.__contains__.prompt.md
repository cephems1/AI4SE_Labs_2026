## Task
Implement InventoryLedger.__contains__ in playground/playground/inventory.py: """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""

## Target
File `playground/playground/inventory.py`, class `InventoryLedger`, method `__contains__`. The method currently is a stub:
```python
def __contains__(self, sku: object) -> bool:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from typing import Dict, Iterator
from .base import Entity, Repository
from .exceptions import InvalidTransitionError, OutOfStockError, UnknownSKUError
from .util import ensure_positive_int, normalize_sku
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.891): playground/playground/inventory.py lines 71-72, method
```python
    def __contains__(self, sku: object) -> bool:
        pass
```

### Chunk 2 (similarity 0.833): playground/playground/inventory.py lines 74-76, method
```python
    def __len__(self) -> int:
        """Return the number of SKUs with positive on-hand stock."""
        return sum(1 for qty in self._on_hand.values() if qty > 0)
```

### Chunk 3 (similarity 0.822): playground/playground/inventory.py lines 12-81, class
```python
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None: ...
    def _require_sku(self, sku: str) -> str: ...
    def add_stock(self, sku: str, quantity: int) -> int: ...
    def available(self, sku: str) -> int: ...
    def reserve(self, sku: str, quantity: int) -> ReservationContext: ...
    def release(self, sku: str, quantity: int) -> None: ...
    def commit(self, sku: str, quantity: int) -> None: ...
    def __contains__(self, sku: object) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
```

### Chunk 4 (similarity 0.821): playground/playground/inventory.py lines 37-40, method
```python
    def available(self, sku: str) -> int:
        """Return on-hand minus reserved for ``sku``."""
        sku = self._require_sku(sku)
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)
```

### Chunk 5 (similarity 0.809): playground/playground/inventory.py lines 23-28, method
```python
    def _require_sku(self, sku: str) -> str:
        """Normalise ``sku`` and raise ``UnknownSKUError`` if it is unregistered."""
        sku = normalize_sku(sku)
        if sku not in self._product_repo:
            raise UnknownSKUError(sku)
        return sku
```

## Instructions
Write the complete implementation of `InventoryLedger.__contains__`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.