```python
    def __contains__(self, event_type: object) -> bool:
        """Return whether any handlers are registered for ``event_type``."""
        return isinstance(event_type, EventType) and bool(self._handlers.get(event_type))
```