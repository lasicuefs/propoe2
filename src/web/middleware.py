from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.web.origins import urls_from, GithubPage, LocalHost


def set_allowed_origins(app: FastAPI) -> None:
    """Configures allowed origins"""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=urls_from(
            remotes=[
                GithubPage("rickbarretto", "propoe2-ui"),
                # Just an example
                # GithubPage("lasicuefs", "propoe2-ui").using_domain("propoe2.com"),
                # Alternatively:
                # Website("propoe2.com")
            ],
            localhosts=[LocalHost.at(4200)],
        ),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
