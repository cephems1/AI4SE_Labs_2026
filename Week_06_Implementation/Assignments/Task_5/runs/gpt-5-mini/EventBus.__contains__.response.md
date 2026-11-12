```python
def __contains__(self, event_type: object) -> bool:
    """Return whether any handlers are registered for ``event_type``."""
    if not isinstance(event_type, EventType):
        raise TypeError("event_type must be EventType")
    return bool(self._handlers.get(event_type, []))
```