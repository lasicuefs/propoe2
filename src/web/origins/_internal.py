from ._remote import RemoteOrigin
from ._local import LocalHost


def urls_from(
    remotes: list[RemoteOrigin] = [], localhosts: list[LocalHost] = []
) -> list[str]:
    """Applies both HTTP and HTTPS schema to origins

    Example
    -------

            app = FastAPI()
            app.add_middleware(
                CORSMiddleware,
                allow_origins= urls_from(
                    remotes=[
                        GithubPages("username", "repository"),
                        Website("mywebsite.com")
                    ],
                    locals=[
                        LocalHost.at(ANGULAR_PORT), # port: int = 4200
                        LocalHost.at(REACT_PORT),
                        LocalHost.at(VUE_PORT),
                        LocalHost.at(SVELTE_PORT),
                    ]
                ),
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

    """

    flatten = lambda xs: [x for sub in xs for x in sub]  # noqa: E731
    origins = remotes + flatten(map(list, localhosts))

    HTTPs = [f"http://{origin}" for origin in origins]
    HTTPSs = [f"http://{origin}" for origin in origins]

    return HTTPs + HTTPSs
