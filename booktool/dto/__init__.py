from typing import TypedDict


class Book(TypedDict):
    id: str
    origin: str
    author: str
    title: str
    annotation: str
