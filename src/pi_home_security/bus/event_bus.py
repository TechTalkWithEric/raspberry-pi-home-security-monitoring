from typing import Callable, Any, Dict, List
import fnmatch

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_name: str, callback: Callable[[Any], None]):
        self.listeners.setdefault(event_name, []).append(callback)

    def publish(self, event_name: str, data: Any = None):
        items = list(self.listeners.items())
        for pattern, callbacks in items:
            if fnmatch.fnmatch(event_name, pattern):
                for cb in callbacks:
                    cb(data)

    def subscriber(self, event_pattern: str):
        """Decorator to register a function as a subscriber."""
        def decorator(fn: Callable[[Any], None]):
            self.subscribe(event_pattern, fn)
            return fn
        return decorator


# Global instance
event_bus = EventBus()