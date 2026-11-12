## Task
Implement Warehouse.stock_report in playground/playground/inventory.py: """Return a mapping of SKU to available quantity."""

## Target
File `playground/playground/inventory.py`, class `Warehouse`, method `stock_report`. The method currently is a stub:
```python
def stock_report(self) -> Dict[str, int]:
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
### Chunk 1 (similarity 0.891): playground/playground/inventory.py lines 150-151, method
```python
    def stock_report(self) -> Dict[str, int]:
        pass
```

### Chunk 2 (similarity 0.860): playground/playground/inventory.py lines 12-81, class
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

### Chunk 3 (similarity 0.852): playground/playground/inventory.py lines 74-76, method
```python
    def __len__(self) -> int:
        """Return the number of SKUs with positive on-hand stock."""
        return sum(1 for qty in self._on_hand.values() if qty > 0)
```

### Chunk 4 (similarity 0.851): playground/playground/inventory.py lines 146-148, method
```python
    def receive(self, sku: str, quantity: int) -> int:
        """Add stock to the warehouse ledger; return the new on-hand total."""
        return self._ledger.add_stock(sku, quantity)
```

### Chunk 5 (similarity 0.838): playground/playground/inventory.py lines 37-40, method
```python
    def available(self, sku: str) -> int:
        """Return on-hand minus reserved for ``sku``."""
        sku = self._require_sku(sku)
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)
```

## Instructions
Write the complete implementation of `Warehouse.stock_report`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.