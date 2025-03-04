from ._local import LocalHost
from ._remote import GithubPage
from ._internal import urls_from


ALLOWED = urls_from(
    remotes=[
        GithubPage("rickbarretto", "propoe2-ui"),
        # Just an example
        # GithubPage("lasicuefs", "propoe2-ui").using_domain("propoe2.com"),
        # Alternatively:
        # Website("propoe2.com")
    ],
    localhosts=[LocalHost.at(4200)],
)
