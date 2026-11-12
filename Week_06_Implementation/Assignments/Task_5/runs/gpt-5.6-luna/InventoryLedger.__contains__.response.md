```python
def __contains__(self, sku: object) -> bool:
    """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
    try:
        normalized = normalize_sku(sku)
    except (TypeError, ValueError):
        return False
    return self._on_hand.get(normalized, 0) > 0
```