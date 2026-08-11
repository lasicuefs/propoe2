"""Configuation of environment variables.

Usage
-----

Set the environment variables before the server initialization,
let Pydantic take care about all the rest.

        # Set the env var
        $  MY_VAR="Something"

        # Initialize the server
        $ fastapi dev src/web
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for Environment variables management.

    External Documentation Resources
    --------------------------------
    Environment Variables usage:
        <https://fastapi.tiangolo.com/environment-variables>

    Settings class usage:
        <https://fastapi.tiangolo.com/advanced/settings>

    Variables
    ---------
    PROPOE_PRODUCTION=FALSE
        Enables or disables features of Propoe when its in Production.

    """

    propoe_production: bool = False

    @property
    def in_production(self) -> bool:
        """Alias to propoe_production"""
        return self.propoe_production

    @property
    def in_dev(self) -> bool:
        """Is in development mode"""
        return not self.in_production


@lru_cache
def settings() -> Settings:
    """Returns a ``Settings``'s instance.

    Caches the instantiation of ``Settings``
    to avoid rebuilding it each time it's created.

    """
    return Settings()


__all__ = ["settings"]
