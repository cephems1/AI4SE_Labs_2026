```python
def can_afford(self, total: Money) -> bool:
    """Return True if ``balance + total`` does not exceed the credit limit."""
    return self._balance + total <= self._credit_limit
```