```python
def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
    """Return ``target`` if the transition is allowed, else raise."""
    if self.can_transition(source, target):
        return target
    raise InvalidTransitionError(f"invalid transition from {source} to {target}")
```