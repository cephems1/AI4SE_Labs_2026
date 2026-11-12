```python
def __contains__(self, event_type: object) -> bool:
    """Return whether any handlers are registered for ``event_type``."""
    return event_type in self._handlers and bool(self._handlers[event_type])
```