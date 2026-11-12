## Task
Implement EventBus.__contains__ in playground/playground/events.py: """Return whether any handlers are registered for ``event_type``."""

## Target
File `playground/playground/events.py`, class `EventBus`, method `__contains__`. The method currently is a stub:
```python
def __contains__(self, event_type: object) -> bool:
    pass
```
Names imported in that file:
```python
from __future__ import annotations
from collections.abc import Mapping
from typing import Callable, Dict, List
from .enums import EventType
```

## Relevant code from the repository (retrieved)
### Chunk 1 (similarity 0.892): playground/playground/events.py lines 53-54, method
```python
    def __contains__(self, event_type: object) -> bool:
        pass
```

### Chunk 2 (similarity 0.812): playground/playground/events.py lines 26-32, method
```python
    def unsubscribe(self, event_type: EventType, handler: Callable[..., None]) -> bool:
        """Remove ``handler`` from ``event_type``; return whether it was present."""
        handlers = self._handlers.get(event_type, [])
        if handler not in handlers:
            return False
        handlers.remove(handler)
        return True
```

### Chunk 3 (similarity 0.810): playground/playground/events.py lines 34-47, method
```python
    def publish(self, event_type: EventType, payload: Mapping[str, object]) -> int:
        """Invoke every handler subscribed to ``event_type`` with ``payload``.

        Returns the number of handlers invoked.
        """
        if not isinstance(event_type, EventType):
            raise TypeError("event_type must be EventType")
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a Mapping")
        count = 0
        for handler in list(self._handlers.get(event_type, [])):
            handler(payload)
            count += 1
        return count
```

### Chunk 4 (similarity 0.803): playground/playground/events.py lines 11-54, class
```python
class EventBus:
    """Synchronous publish/subscribe keyed by :class:`EventType`."""
    def __init__(self) -> None: ...
    def subscribe(self, event_type: EventType, handler: Callable[..., None]) -> None: ...
    def unsubscribe(self, event_type: EventType, handler: Callable[..., None]) -> bool: ...
    def publish(self, event_type: EventType, payload: Mapping[str, object]) -> int: ...
    def __len__(self) -> int: ...
    def __contains__(self, event_type: object) -> bool: ...
```

### Chunk 5 (similarity 0.801): playground/playground/events.py lines 18-24, method
```python
    def subscribe(self, event_type: EventType, handler: Callable[..., None]) -> None:
        """Register ``handler`` to be called when ``event_type`` is published."""
        if not isinstance(event_type, EventType):
            raise TypeError("event_type must be EventType")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers.setdefault(event_type, []).append(handler)
```

## Instructions
Write the complete implementation of `EventBus.__contains__`.
- Keep the signature exactly as in the stub; do not repeat its decorators.
- Put the docstring from the task as the method's docstring.
- Use only names that are imported in the file, defined in it, or are builtins.
Answer with the method in a single ```python block.