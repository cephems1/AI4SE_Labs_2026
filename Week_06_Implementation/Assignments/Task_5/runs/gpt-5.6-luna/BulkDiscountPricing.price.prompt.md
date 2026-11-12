## Task
Implement BulkDiscountPricing.price in playground/playground/pricing.py: """Return the base price, less the discount if the quantity qualifies."""

## Target
File `playground/playground/pricing.py`, class `BulkDiscountPricing`, method `price`. The method currently is a stub:
```python
def price(self, items: Sequence[LineItem]) -> Money:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from typing import Sequence
from .base import PricingStrategy
from .models import LineItem, Money
from .util import ensure_positive_int
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.851): playground/playground/pricing.py lines 66-68, method
```python
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"BulkDiscountPricing(threshold={self._threshold}, percent_off={self._percent_off})"
```

### Chunk 2 (similarity 0.848): playground/playground/pricing.py lines 53-56, method
```python
    @property
    def threshold(self) -> int:
        """Return the qualifying total quantity."""
        return self._threshold
```

### Chunk 3 (similarity 0.839): playground/playground/pricing.py lines 63-64, method
```python
    def price(self, items: Sequence[LineItem]) -> Money:
        pass
```

### Chunk 4 (similarity 0.836): playground/playground/pricing.py lines 58-61, method
```python
    @property
    def percent_off(self) -> int:
        """Return the discount percentage."""
        return self._percent_off
```

### Chunk 5 (similarity 0.823): playground/playground/pricing.py lines 37-68, class
```python
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None: ...
    @property
    def threshold(self) -> int: ...
    @property
    def percent_off(self) -> int: ...
    def price(self, items: Sequence[LineItem]) -> Money: ...
    def __repr__(self) -> str: ...
```

## Instructions
Write the complete implementation of `BulkDiscountPricing.price`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.