```python
def __contains__(self, sku: object) -> bool:
    """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
    try:
        sku = normalize_sku(sku)
    except (InvalidTransitionError, TypeError, ValueError):
        return False
    return self._on_hand.get(sku, 0) > 0
```