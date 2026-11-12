```python
    def price(self, items: Sequence[LineItem]) -> Money:
        """Return the base price, less the discount if the quantity qualifies."""
        base_price = self._base.price(items)
        total_quantity = sum(item.quantity for item in items)
        if total_quantity < self._threshold:
            return base_price
        discount = base_price.cents * self._percent_off // 100
        return Money(base_price.cents - discount)
```