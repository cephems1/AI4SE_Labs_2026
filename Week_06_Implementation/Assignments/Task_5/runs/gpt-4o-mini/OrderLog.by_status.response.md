```python
def by_status(self, status: OrderStatus) -> Iterator[Order]:
    """Yield orders whose status matches ``status``."""
    for order in self:
        if order.status == status:
            yield order
```