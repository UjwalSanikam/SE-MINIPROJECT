from typing import Callable

from src.common import MediaController


class TrackControl:
    """Track feature (FR4): next and previous track via the media backend."""

    def __init__(self, controller: MediaController):
        self._controller = controller

    def next(self) -> str:
        return self._run("Next track", self._controller.next_track, "Track skipped to next")

    def previous(self) -> str:
        return self._run(
            "Previous track",
            self._controller.previous_track,
            "Track returned to previous",
        )

    def _run(self, name: str, action: Callable[[], None], success_message: str) -> str:
        """Call the backend; never let a backend error crash the application."""
        try:
            action()
        except Exception as exc:
            return f"{name} failed: {exc}"
        return success_message
