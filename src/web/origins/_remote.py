"""Remote Pages Settings"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


def doesnt_contain_schema(url: str) -> bool:
    return ":" not in url


class RemoteOrigin(ABC):
    @abstractmethod
    def __str__(self) -> str: ...


@dataclass
class Website(RemoteOrigin):
    """Origin for remote website"""

    origin: str

    def __post_init__(self):
        assert doesnt_contain_schema(self.origin)

    def __str__(self) -> str:
        return self.origin


@dataclass
class GithubPages(RemoteOrigin):
    """Origin for Github Pages"""

    user: str
    repo: str
    custom_domain: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.custom_domain, str):
            assert doesnt_contain_schema(self.custom_domain)

    def using_domain(self, domain: str) -> "GithubPages":
        """GithubPage using a custom ``domain``"""
        return GithubPages(self.user, self.repo, domain)

    def __str__(self) -> str:
        """Returns the origin from Github's Page"""
        if isinstance(self.custom_domain, str):
            return self.custom_domain

        return f"{self.user}.github.io/{self.repo}"
