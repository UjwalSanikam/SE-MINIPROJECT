from abc import ABC, abstractmethod


class MediaController(ABC):
    """Contract between the feature modules and the media backend.

    The backend implements these; volume, playback and track modules call them.
    """

    @abstractmethod
    def volume_up(self) -> None: ...

    @abstractmethod
    def volume_down(self) -> None: ...

    @abstractmethod
    def play(self) -> None: ...

    @abstractmethod
    def pause(self) -> None: ...

    @abstractmethod
    def resume(self) -> None: ...

    @abstractmethod
    def next_track(self) -> None: ...

    @abstractmethod
    def previous_track(self) -> None: ...
