from ..api.manufacturer import Manufacturer

from pydantic import BaseModel, Field

from collections import defaultdict

import typing as T

class Plugin(BaseModel):
    id: str

    name: str
    
    version: str
    
    description: str
    
    tags: list[str]
    
    logo: str

    manufacturers: list[Manufacturer]
    
    #
    #
    #
    
    def __init__(self, **data: T.Any):
        super().__init__(**data)
        
        self._events = defaultdict(list)  # type: T.DefaultDict[str, T.List[T.Callable]]

    #
    #
    #

    def on(self, event: str, *handlers: T.Callable) -> T.Callable:
        """Registers one or more handlers to a specified event.
        This method may as well be used as a decorator for the handler."""

        def _on_wrapper(*handlers: T.Callable) -> T.Callable:
            """wrapper for on decorator"""
            self._events[event].extend(handlers)
            return handlers[0]

        if handlers:
            return _on_wrapper(*handlers)
        
        return _on_wrapper

    def trigger(self, event: str, *args: T.Any, **kw: T.Any) -> bool:
        """Triggers all handlers which are subscribed to an event.
        Returns True when there were callbacks to execute, False otherwise."""

        callbacks = list(self._events.get(event, []))
        if not callbacks:
            return False

        for callback in callbacks:
            callback(*args, **kw)
            
        return True
