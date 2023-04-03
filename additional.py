from typing import TypedDict, NamedTuple
from strenum import StrEnum
from enum import auto
from dataclasses import dataclass


class StagesList(StrEnum):
    connecting = auto()
    loggining = auto()
    registration = auto()


class InfoList(StrEnum):
    app_closed = auto()
    log_in_data = auto()
    register_data = auto()


class SendingData(TypedDict):
    text_to_cmd: list[str]
    set_stage: StagesList | None
    informing: list[InfoList] | None


class Options(TypedDict):
    language: dict[str]


def decode_json(j):
    if j['set_stage'] is not None:
        j['set_stage'] = StagesList(j['set_stage'])
    for i, inf in enumerate(j['informing']):
        j['informing'][i] = InfoList(inf)
    return j


@dataclass
class Window:
    width: int = 1200
    height: int = 600


class Color(NamedTuple):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BG = (42, 43, 46)
    BOLD = (0, 0, 0, 60)
    YELLOW = (255, 255, 0)


class Language(NamedTuple):
    ini: dict[str, str]
    OPT_SELECT_LANG: str
    CONFIRM: str
    SERV_CONNECTING: str
