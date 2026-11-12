```python
def by_status(self, status: OrderStatus) -> Iterator[Order]:
    """Yield orders whose status matches ``status``."""
    yield from (order for order in self._orders if order.status == status)
```