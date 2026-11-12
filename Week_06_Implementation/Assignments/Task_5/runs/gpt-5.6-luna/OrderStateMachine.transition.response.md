```python
def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
    """Return ``target`` if the transition is allowed, else raise."""
    if not self.can_transition(source, target):
        raise InvalidTransitionError(f"Cannot transition from {source} to {target}")
    return target
```