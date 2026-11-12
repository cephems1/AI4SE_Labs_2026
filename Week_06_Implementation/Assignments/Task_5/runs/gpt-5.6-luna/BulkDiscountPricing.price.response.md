```python
def price(self, items: Sequence[LineItem]) -> Money:
    """Return the base price, less the discount if the quantity qualifies."""
    base_price = self._base.price(items)
    quantity = sum(item.quantity for item in items)
    if quantity >= self._threshold:
        return base_price * (100 - self._percent_off) / 100
    return base_price
```