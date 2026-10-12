import re
from typing import Optional

from src.common import Command

# Extra phrasings the speech-to-text might produce for each command.
_ALIASES = {
    "volume up": Command.VOLUME_UP,
    "increase volume": Command.VOLUME_UP,
    "volume down": Command.VOLUME_DOWN,
    "decrease volume": Command.VOLUME_DOWN,
    "play": Command.PLAY,
    "pause": Command.PAUSE,
    "resume": Command.RESUME,
    "next": Command.NEXT,
    "next track": Command.NEXT,
    "previous": Command.PREVIOUS,
    "previous track": Command.PREVIOUS,
}


def _normalize(text: str) -> str:
    """Lowercase, drop punctuation, collapse extra spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return " ".join(text.split())


def parse_command(text: Optional[str]) -> Optional[Command]:
    """Map recognized speech text to a Command.

    Returns None for empty or unsupported input (FR5), so the caller
    can ignore it or show a simple message without crashing.
    """
    if not text:
        return None
    return _ALIASES.get(_normalize(text))
