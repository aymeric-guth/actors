from typing import Callable, Any
from functools import wraps
import time
import threading

from .message import Event, Message, Sig


# def observer(actor: str):
#     def inner(func: Callable):
#         @wraps(func)
#         def _(*args, **kwargs):
#             (self, *value) = args
#             name = func.__name__
#             func(self, *value)
#             res = getattr(self, f'_{name}')
#             send(to=actor, what=Message(sig=Sig.WATCHER, args={name: res}))
#             # send(to=actor, what=Event(type='property-change', name=name, args=res))
#         return _
#     return inner


def clamp(
    lo: int|float, 
    hi: int|float
) -> Callable[[int|float], int|float]:
    def inner(val: int|float) -> int|float:
        return max(lo, min(val, hi))
    return inner


def to_snake_case(s: str) -> str:
    return '_'.join(s.split('-'))


def to_kebab_case(s: str) -> str:
    return '-'.join(s.split('_'))


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def defer(callback: Callable, timeout: float=1., logger=None) -> None:
    def sleepy(timeout: float):
        def inner(func, *args, **kwargs):
            time.sleep(timeout)
            try:
                return func(*args, **kwargs)
            except Exception as err:
                if logger is not None:
                    logger.error(f'{err=}')
                raise SystemExit
        return inner

    threading.Thread(
        target=sleepy(timeout),
        args=[callback],
        daemon=True, 
    ).start()
