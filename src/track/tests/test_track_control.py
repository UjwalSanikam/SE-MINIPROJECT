from unittest.mock import create_autospec

import pytest

from src.common import MediaController
from src.track import TrackControl


@pytest.fixture
def controller():
    return create_autospec(MediaController, instance=True)


@pytest.fixture
def track(controller):
    return TrackControl(controller)


def test_next_calls_backend_once(track, controller):
    msg = track.next()
    controller.next_track.assert_called_once_with()
    assert msg == "Track skipped to next"


def test_previous_calls_backend_once(track, controller):
    msg = track.previous()
    controller.previous_track.assert_called_once_with()
    assert msg == "Track returned to previous"


@pytest.mark.parametrize(
    "operation, backend_method, label",
    [
        ("next", "next_track", "Next track"),
        ("previous", "previous_track", "Previous track"),
    ],
)
def test_backend_failure_returns_message_without_crashing(
    track, controller, operation, backend_method, label
):
    getattr(controller, backend_method).side_effect = RuntimeError("backend unavailable")

    msg = getattr(track, operation)()

    assert label in msg
    assert "failed" in msg
    assert "backend unavailable" in msg
