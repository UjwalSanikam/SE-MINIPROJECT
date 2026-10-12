from enum import Enum


class Command(Enum):
    """Every command the assistant understands (FR2, FR3, FR4)."""

    VOLUME_UP = "volume up"
    VOLUME_DOWN = "volume down"
    PLAY = "play"
    PAUSE = "pause"
    RESUME = "resume"
    NEXT = "next"
    PREVIOUS = "previous"
