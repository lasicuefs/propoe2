from ._local import LocalHost
from ._remote import GithubPage, Website
from ._internal import urls_from


__all__ = ["urls_from", "GithubPage", "Website", "LocalHost"]
