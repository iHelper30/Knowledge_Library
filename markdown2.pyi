
from typing import Any

class Markdown2:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def convert(self, text: str, **kwargs: Any) -> str: ...
    def convert_to_html(self, text: str, **kwargs: Any) -> str: ...
