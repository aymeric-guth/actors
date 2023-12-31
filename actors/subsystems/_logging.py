import os
from typing import Any
import threading
import logging
import logging.handlers

from utils import clamp

LOG_HOST = "127.0.0.1" if not os.getenv("LOG_HOST") else os.getenv("LOG_HOST")
LOG_PORT = 8080 if not os.getenv("LOG_PORT") else os.getenv("LOG_PORT")
LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(actor)s][%(name)s:%(lineno)s][%(message)s]"


# logging
class Logging:
    def __init__(self, name: str, actor: str) -> None:
        self._name = name
        self._last = 0
        self._logger: logging.LoggerAdapter[logging.Logger]
        self._log_l = threading.Lock()

        fmt = logging.Formatter(fmt=LOG_FORMAT)
        handler = logging.handlers.SocketHandler(LOG_HOST, LOG_PORT)
        handler.setFormatter(fmt)
        self.__logger = logging.getLogger(self._name)
        self.__logger.addHandler(handler)
        self._logger = logging.LoggerAdapter(self.__logger, {"actor": actor})

    @property
    def log_lvl(self) -> int:
        return self._log_lvl

    @log_lvl.setter
    def log_lvl(self, value: int) -> None:
        self._log_lvl = int(clamp(0, 50)(value))
        self.logger.setLevel(self._log_lvl)
        # self._logger.error(f'Setting {self} to level={self._log_lvl}')

    @property
    def log_lock(self) -> threading.Lock:
        return self._log_l

    @log_lock.setter
    def log_lock(self, value: Any) -> None:
        raise TypeError("Property is immutable")

    @property
    def logger(self) -> logging.LoggerAdapter:
        # with self._log_l:
        return self._logger

    @logger.setter
    def logger(self, value: Any) -> None:
        raise TypeError("Property is immutable")

    def log(self, sender: str, receiver: str, msg: str) -> None:
        self.logger.info(f"{sender=}\n{receiver=}\n{msg=}")

    # def log(self, sender: Optional[int], receiver: Optional[int], msg: Message|dict[str, Any], fmt: str='') -> None:
    #     if not isinstance(sender, int):
    #         self.logger.error(f'{fmt}\nGot unexpected Sender={sender}, type={type(sender)}\nmsg={msg}')
    #     elif sender == receiver:
    #         self.logger.info(f'{fmt}\nself={self!r}\n{msg=}')
    #     else:
    #         self.logger.info(f'{fmt}\nreceiver={self!r}\nsender={sender}\n{msg=}')

    def frameinfo(self, frame) -> None:
        self.logger.error(
            f"{frame.f_code.co_name=} {frame.f_code.co_varnames=} {frame.f_code.co_filename=} {frame.f_code.co_firstlineno=} {frame.f_locals=} {frame.f_lineno=}"
        )

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def warn(self, message: str) -> None:
        self.logger.warn(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def __enter__(self) -> None:
        # self.log_lock.acquire()
        self._last = self.log_lvl
        self.log_lvl = logging.DEBUG

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.log_lvl = self._last
        # self.log_lock.release()
