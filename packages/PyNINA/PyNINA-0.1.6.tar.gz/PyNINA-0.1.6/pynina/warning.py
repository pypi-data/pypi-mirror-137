import datetime
from typing import Dict, Any, Optional

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .const import ReadOnlyClass, ENDPOINT_WARNING_DETAIL


class Warning(BaseAPI, metaclass=ReadOnlyClass):
    """Class to reflect a warning."""
    def __init__(self, data: Dict[str, Any], session: ClientSession = None):
        """Initialize."""
        super().__init__(session)

        self.id: str = data["payload"]["id"]
        self.headline: str = data["payload"]["data"]["headline"]
        self.description: str = ""
        self.sender: str = ""
        self.sent: str = data["sent"]
        self.start: Optional[str] = data.get("start", None)
        self.expires: Optional[str] = data.get("expires", None)

        self.raw: Dict[str, Any] = data

    def isValid(self) -> bool:
        """Test if warning is valid."""
        if self.expires is not None:
            currDate: datetime = datetime.datetime.now().timestamp()
            expiresDate = datetime.datetime.fromisoformat(self.expires).timestamp()
            return currDate < expiresDate
        return True

    async def getDescription(self):
        """Get the details of a warning."""
        url: str = ENDPOINT_WARNING_DETAIL + self.id + ".json"
        data = await self._makeRequest(url)

        infos = data["info"][0]

        self.description = infos["description"]

        if "senderName" in infos:
            self.sender = infos["senderName"]

    def __repr__(self) -> str:
        return f"{self.id} ({self.sent}): [{self.sender}] {self.headline}, {self.description}"
