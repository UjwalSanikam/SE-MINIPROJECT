from unittest.mock import create_autospec

import pytest

from src.common import MediaController
from src.playback import PlaybackControl, PlaybackState


@pytest.fixture
def controller():
    return create_autospec(MediaController, instance=True)


@pytest.fixture
def playback(controller):
    return PlaybackControl(controller)


def test_initial_state_is_stopped(playback):
    assert playback.state is PlaybackState.STOPPED


def test_play_calls_backend_once_and_sets_playing(playback, controller):
    msg = playback.play()
    controller.play.assert_called_once_with()
    assert playback.state is PlaybackState.PLAYING
    assert msg == "Playback started"


def test_pause_calls_backend_once_and_sets_paused(playback, controller):
    playback.play()
    msg = playback.pause()
    controller.pause.assert_called_once_with()
    assert playback.state is PlaybackState.PAUSED
    assert msg == "Playback paused"


def test_resume_calls_backend_once_and_sets_playing(playback, controller):
    playback.play()
    playback.pause()
    msg = playback.resume()
    controller.resume.assert_called_once_with()
    assert playback.state is PlaybackState.PLAYING
    assert msg == "Playback resumed"


def test_state_property_is_read_only(playback):
    with pytest.raises(AttributeError):
        playback.state = PlaybackState.PLAYING


@pytest.mark.parametrize(
    "operation, label",
    [("play", "Play"), ("pause", "Pause"), ("resume", "Resume")],
)
@pytest.mark.parametrize("start", list(PlaybackState))
def test_backend_failure_returns_message_and_preserves_state(
    playback, controller, operation, label, start
):
    playback._state = start  # arrange a known prior state
    getattr(controller, operation).side_effect = RuntimeError("backend unavailable")

    msg = getattr(playback, operation)()

    assert playback.state is start
    assert label in msg
    assert "failed" in msg
    assert "backend unavailable" in msg
