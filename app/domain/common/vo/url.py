from dataclasses import dataclass
from ..exceptions import IncorrectURLString
import re

_URL_RE = re.compile(r"^https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?$")


@dataclass(frozen=True, eq=True)
class URL:
    url: str

    def __post_init__(self):
        if not _URL_RE.fullmatch(self.url):
            raise IncorrectURLString(self.url)
