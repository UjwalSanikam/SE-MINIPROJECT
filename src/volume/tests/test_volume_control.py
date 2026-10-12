import pytest

from src.common import MediaController
from src.volume import VolumeControl


class FakeController(MediaController):
    def __init__(self, fail=False):
        self.up_calls = 0
        self.down_calls = 0
        self.fail = fail

    def volume_up(self):
        if self.fail:
            raise RuntimeError("backend unavailable")
        self.up_calls += 1

    def volume_down(self):
        if self.fail:
            raise RuntimeError("backend unavailable")
        self.down_calls += 1

    def play(self): ...
    def pause(self): ...
    def resume(self): ...
    def next_track(self): ...
    def previous_track(self): ...


def test_increase_calls_backend_once_by_default():
    fake = FakeController()
    msg = VolumeControl(fake).increase()
    assert fake.up_calls == 1
    assert msg == "Volume increased"


def test_decrease_calls_backend_once_by_default():
    fake = FakeController()
    msg = VolumeControl(fake).decrease()
    assert fake.down_calls == 1
    assert msg == "Volume decreased"


def test_step_size_repeats_backend_calls():
    fake = FakeController()
    VolumeControl(fake, steps=3).increase()
    assert fake.up_calls == 3


def test_backend_error_does_not_crash():
    msg = VolumeControl(FakeController(fail=True)).increase()
    assert msg.startswith("Volume change failed")


@pytest.mark.parametrize("steps", [0, -1])
def test_invalid_steps_rejected(steps):
    with pytest.raises(ValueError):
        VolumeControl(FakeController(), steps=steps)
