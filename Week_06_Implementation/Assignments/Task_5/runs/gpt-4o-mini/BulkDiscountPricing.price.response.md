```python
def price(self, items: Sequence[LineItem]) -> Money:
    """Return the base price, less the discount if the quantity qualifies."""
    total_quantity = sum(item.quantity for item in items)
    if total_quantity < self._threshold:
        return self.base.price(items)
    
    discount = self.base.price(items) * (self._percent_off / 100)
    return self.base.price(items) - discount
```