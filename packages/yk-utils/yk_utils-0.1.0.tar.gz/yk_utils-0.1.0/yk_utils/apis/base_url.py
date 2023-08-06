"""Base URL module.
"""


class BaseUrl:
    """Manage YooniK Face API base URL."""
    @classmethod
    def set(cls, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'
        cls.base_url = base_url

    @classmethod
    def get(cls) -> str:
        if not hasattr(cls, 'base_url'):
            cls.base_url = None
        return cls.base_url
