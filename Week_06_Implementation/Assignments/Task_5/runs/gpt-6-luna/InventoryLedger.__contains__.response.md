```python
    def __contains__(self, sku: object) -> bool:
        """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
        sku = normalize_sku(sku)
        return self._on_hand.get(sku, 0) > 0
```