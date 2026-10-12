from enum import Enum
from typing import Callable

from src.common import MediaController


class PlaybackState(Enum):
    """Playback states tracked by PlaybackControl."""

    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class PlaybackControl:
    """Playback feature (FR3): play, pause and resume via the media backend.

    The state is the last *successfully requested* state, i.e. what this
    class last asked the backend to do and the backend accepted without
    raising. It is not independently verified against a real media player.
    """

    def __init__(self, controller: MediaController):
        self._controller = controller
        self._state = PlaybackState.STOPPED

    @property
    def state(self) -> PlaybackState:
        return self._state

    def play(self) -> str:
        return self._run("Play", self._controller.play, PlaybackState.PLAYING, "Playback started")

    def pause(self) -> str:
        return self._run("Pause", self._controller.pause, PlaybackState.PAUSED, "Playback paused")

    def resume(self) -> str:
        return self._run(
            "Resume", self._controller.resume, PlaybackState.PLAYING, "Playback resumed"
        )

    def _run(
        self,
        name: str,
        action: Callable[[], None],
        new_state: PlaybackState,
        success_message: str,
    ) -> str:
        """Call the backend; change state only on success, never crash the app."""
        try:
            action()
        except Exception as exc:
            return f"{name} failed: {exc}"
        self._state = new_state
        return success_message
