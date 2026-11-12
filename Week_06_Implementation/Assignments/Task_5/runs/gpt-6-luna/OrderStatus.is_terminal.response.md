```python
def is_terminal(self) -> bool:
    """True when the status ends further transitions."""
    return self in (OrderStatus.SHIPPED, OrderStatus.CANCELLED)
```