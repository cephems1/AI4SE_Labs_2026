```python
def stock_report(self) -> Dict[str, int]:
    """Return a mapping of SKU to available quantity."""
    return {sku: self._ledger.available(sku) for sku in self._ledger}
```