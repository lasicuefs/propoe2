"""Localhosts settings"""

from dataclasses import dataclass
from typing import Iterator


@dataclass
class LocalHost:
    """Local Host Origins

    Example
    -------

            host = LocalHost.at(4200)
            assert ["127.0.0.1:4200", "localhost:4200"] == map(list, host)

    """
    port: int

    def __post_init__(self) -> None:
        self.hosts = ["127.0.0.1", "localhost"]

    @staticmethod
    def at(port: int) -> "LocalHost":
        """New LocalHost at ``port``"""
        return LocalHost(port)

    def __iter__(self) -> Iterator[str]:
        return iter([f"{host}:{self.port}" for host in self.hosts])
