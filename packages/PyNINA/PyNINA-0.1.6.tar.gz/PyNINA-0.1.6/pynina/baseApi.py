from typing import Any, Dict

from aiohttp import ClientSession, ClientConnectionError


class BaseAPI:
    """Class to perform CMI API requests"""

    def __init__(self, session: ClientSession = None):
        """Constructor for BaseAPI."""
        self.session = session

    async def _makeRequest(self, url: str):
        """Retrieve data from API."""
        internalSession: bool = False
        if self.session is None:
            internalSession = True
            self.session = ClientSession()

        try:
            async with self.session.get(url) as res:
                if res.status != 200:
                    raise ApiError(f"Invalid response: {res.status}")

                json: Dict[str, Any] = await res.json()
                if internalSession:
                    await self.session.close()
                    self.session = None
                return json
        except ClientConnectionError:
            if internalSession:
                await self.session.close()
                self.session = None
            raise ApiError(f"Could not connect to Api")


class ApiError(Exception):
    """Raised when API request ended in error."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status
