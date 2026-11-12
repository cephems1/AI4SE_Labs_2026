```python
@property
def is_terminal(self) -> bool:
    """True when the status ends further transitions."""
    return self in (self.SHIPPED, self.CANCELLED)
```