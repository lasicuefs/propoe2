from ._local import LocalHost
from ._remote import GithubPages, Website
from ._internal import urls_from


__all__ = ["urls_from", "GithubPages", "Website", "LocalHost"]
