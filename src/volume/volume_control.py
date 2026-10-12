from typing import Callable

from src.common import MediaController


class VolumeControl:
    """Volume feature (FR2): increase or decrease volume via the media backend."""

    def __init__(self, controller: MediaController, steps: int = 1):
        if steps < 1:
            raise ValueError("steps must be at least 1")
        self._controller = controller
        self._steps = steps

    def increase(self) -> str:
        return self._run(self._controller.volume_up, "Volume increased")

    def decrease(self) -> str:
        return self._run(self._controller.volume_down, "Volume decreased")

    def _run(self, action: Callable[[], None], success_message: str) -> str:
        """Call the backend `steps` times; never let a backend error crash the app."""
        try:
            for _ in range(self._steps):
                action()
        except Exception as exc:
            return f"Volume change failed: {exc}"
        return success_message
