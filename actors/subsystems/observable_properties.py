from typing import Any, Callable
from collections import defaultdict

from ..message import Event, Message, Sig
from ..actor_system import send, ActorSystem, _get_caller
from utils import to_kebab_case, to_snake_case


class ObservableProperties:
    def __init__(self) -> None:
        self._observers: defaultdict[str, list[str | int]] = defaultdict(list)
        self._registred: set[str] = set()

    def register(self, name: str, pid: int | str) -> None:
        obs = self._observers[name]
        if name not in self:
            self._registred.add(name)
        if pid not in obs:
            obs.append(pid)

    def unregister(self, name: str, pid: int | str) -> None:
        obs = self._observers.get(name)
        if pid in obs:  # type: ignore
            obs.remove(pid)  # type: ignore

    def notify_one(
        self, receiver: int, name: str, value: Any, frame_id: int = 4
    ) -> None:
        caller = _get_caller(frame_id)
        event = Event(type="property-change", name=to_kebab_case(name), args=value)
        ActorSystem()._send(sender=caller, receiver=receiver, msg=event)

    def notify(self, name: str, value: Any, frame_id: int = 4) -> None:
        event = Event(type="property-change", name=to_kebab_case(name), args=value)
        caller = _get_caller(frame_id)
        for obs in self._observers[name]:
            ActorSystem()._send(sender=caller, receiver=obs, msg=event)

    def __contains__(self, key: str) -> bool:
        return key in self._registred

    def __repr__(self) -> str:
        return repr(self._observers)


class Observable:
    def __init__(self, name=None, setter=lambda x: 0.0 if x is None else x) -> None:
        self.name = name
        self.setter = setter

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> object:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.name] = self.setter(value)
        try:
            obs = instance.__dict__["obs"]
        except Exception as err:
            raise SystemExit
        obs.notify(self.name, instance.__dict__[self.name])
