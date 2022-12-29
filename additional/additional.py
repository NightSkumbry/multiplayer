from dataclasses import dataclass


@dataclass
class Prefixes:
    text: str = 'txt:'
    command: str = 'com:'
    check_connection: str = 'con:'
