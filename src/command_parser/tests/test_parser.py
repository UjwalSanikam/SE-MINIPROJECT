import pytest

from src.command_parser import parse_command
from src.common import Command


@pytest.mark.parametrize(
    "text, expected",
    [
        ("volume up", Command.VOLUME_UP),
        ("Volume Down", Command.VOLUME_DOWN),
        ("play", Command.PLAY),
        ("PAUSE", Command.PAUSE),
        ("resume", Command.RESUME),
        ("next", Command.NEXT),
        ("previous", Command.PREVIOUS),
    ],
)
def test_supported_commands(text, expected):
    assert parse_command(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Volume Up!", Command.VOLUME_UP),
        ("  next   track ", Command.NEXT),
        ("increase volume", Command.VOLUME_UP),
    ],
)
def test_normalization_and_aliases(text, expected):
    assert parse_command(text) == expected


@pytest.mark.parametrize("text", ["dance", "volume sideways", "", "   ", None])
def test_unsupported_input_returns_none(text):
    assert parse_command(text) is None
