```python
def __contains__(self, sku: object) -> bool:
    """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
    sku = self._require_sku(sku)
    return self.available(sku) > 0
```