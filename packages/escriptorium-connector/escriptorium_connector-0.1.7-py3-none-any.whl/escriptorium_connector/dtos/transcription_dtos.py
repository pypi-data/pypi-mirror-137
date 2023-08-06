from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass
from escriptorium_connector.dtos.super_dtos import PagenatedResponse
from typing import Union, List
from datetime import datetime
from dataclasses import field


@dataclass(init=True, frozen=True)
class PostAbbreviatedTranscription:
    name: str


@dataclass(init=True, frozen=True)
class GetAbbreviatedTranscription:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class PostTranscription:
    line: int
    transcription: int
    content: str
    graphs: Union[str, None] = None


@dataclass(init=True, frozen=True)
class GetTranscription:
    pk: int
    line: int
    transcription: int
    content: str
    versions: List[str]  # TODO: Check that this is correct
    version_author: str
    version_source: str
    version_updated_at: datetime
    graphs: Union[str, None] = None


@dataclass
class GetTranscriptions(PagenatedResponse):
    results: List[GetTranscription] = field(default_factory=list)
