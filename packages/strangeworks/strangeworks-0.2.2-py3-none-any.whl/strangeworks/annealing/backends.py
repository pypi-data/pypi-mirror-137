__plugin_urls = {
    "aws": "/plugin/aws",
}


class Backend:
    def __init__(
        self,
        id: str = None,
        provider_id: str = None,
        name: str = None,
        provider_slug: str = None,
        remote_backend_id: str = None,
        plugin_url: str = None,
    ):
        self.__id = id
        self.__provider_id = provider_id
        self.__name = name
        self.__provider_slug = provider_slug
        self.__remote_backend_id = remote_backend_id
        self.__plugin_url = plugin_url

    @classmethod
    def from_cgw(cls, backend: dict) -> "Backend":
        if backend.get("type", "") != "annealing":
            return None
        id = backend.get("id", "")
        provider_id = backend.get("providerId", "")
        name = backend.get("name", "")
        provider_slug = backend.get("providerSlug", "")
        remote_backend_id = backend.get("remoteBackendId", "")
        return cls(
            id=id,
            provider_id=provider_id,
            name=name,
            provider_slug=provider_slug,
            remote_backend_id=remote_backend_id,
            plugin_url=__plugin_urls.get(provider_slug, None),
        )
