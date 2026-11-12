## Task
Implement Customer.can_afford in playground/playground/models.py: """Return True if ``balance + total`` does not exceed the credit limit."""

## Target
File `playground/playground/models.py`, class `Customer`, method `can_afford`. The method currently is a stub:
```python
def can_afford(self, total: Money) -> bool:
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
### Chunk 1 (similarity 0.864): playground/playground/models.py lines 261-262, method
```python
    def can_afford(self, total: Money) -> bool:
        pass
```

### Chunk 2 (similarity 0.851): playground/playground/models.py lines 264-268, method
```python
    def charge(self, total: Money) -> None:
        """Increase the balance by ``total``, raising if the limit would be exceeded."""
        if not self.can_afford(total):
            raise ValueError("credit limit exceeded")
        self._balance = self._balance + total
```

### Chunk 3 (similarity 0.830): playground/playground/models.py lines 247-250, method
```python
    @property
    def credit_limit(self) -> Money:
        """Return the credit limit."""
        return self._credit_limit
```

### Chunk 4 (similarity 0.783): playground/playground/models.py lines 221-268, class
```python
class Customer(Entity):
    """Buyer with a credit limit. Balance is the amount owed."""
    def __init__(self, customer_id: str, name: str, credit_limit: Money = Money(0)) -> None: ...
    @property
    def customer_id(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def credit_limit(self) -> Money: ...
    @property
    def balance(self) -> Money: ...
    def identity(self) -> str: ...
    def can_afford(self, total: Money) -> bool: ...
    def charge(self, total: Money) -> None: ...
```

### Chunk 5 (similarity 0.772): playground/playground/models.py lines 224-235, method
```python
    def __init__(self, customer_id: str, name: str, credit_limit: Money = Money(0)) -> None:
        """Create a customer with the given identity, name, and credit limit."""
        if not isinstance(customer_id, str) or customer_id.strip() == "":
            raise ValueError("customer_id required")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("name required")
        if not isinstance(credit_limit, Money):
            raise TypeError("credit_limit must be Money")
        self._customer_id = customer_id
        self._name = name
        self._credit_limit = credit_limit
        self._balance = Money(0)
```

## Instructions
Write the complete implementation of `Customer.can_afford`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.