from abc import ABC, abstractmethod


class SearchBase(ABC):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/58.0.3029.110 Safari/537.36"
        )
    }

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def search(self, query: str) -> list[dict]:
        """Execute a search and return a list of results."""
        pass
