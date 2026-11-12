```python
def stock_report(self) -> Dict[str, int]:
    """Return a mapping of SKU to available quantity."""
    report: Dict[str, int] = {}
    for sku in self._ledger:
        available_qty = self._ledger.available(sku)
        if available_qty > 0:
            report[sku] = available_qty
    return report
```