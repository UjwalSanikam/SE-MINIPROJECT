import time

import pytest
import speech_recognition as sr

from src.voice_input import VoiceInput


class FakeMicrophone:
    def __enter__(self):
        return object()

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class FakeRecognizer:
    def __init__(self, result="Volume Up"):
        self.result = result
        self.listen_args = None

    def listen(self, source, timeout, phrase_time_limit):
        self.listen_args = (source, timeout, phrase_time_limit)
        return "audio"

    def recognize_google(self, audio):
        return self.result


def build_voice_input(recognizer):
    return VoiceInput(
        recognizer=recognizer,
        microphone_factory=FakeMicrophone,
        listen_timeout=2.0,
        phrase_time_limit=3.0,
    )


def test_capture_returns_trimmed_transcription():
    recognizer = FakeRecognizer("  Volume Up  ")

    assert build_voice_input(recognizer).capture() == "Volume Up"
    assert recognizer.listen_args[1:] == (2.0, 3.0)


@pytest.mark.parametrize(
    "error",
    [
        sr.WaitTimeoutError,
        sr.UnknownValueError,
        sr.RequestError,
        OSError,
        AttributeError,
    ],
)
def test_capture_returns_none_for_unusable_input(error):
    class ErrorRecognizer(FakeRecognizer):
        def listen(self, source, timeout, phrase_time_limit):
            if error is sr.WaitTimeoutError:
                raise error()
            return super().listen(source, timeout, phrase_time_limit)

        def recognize_google(self, audio):
            if error is sr.UnknownValueError:
                raise error()
            raise error("speech service unavailable")

    assert build_voice_input(ErrorRecognizer()).capture() is None


def test_capture_returns_none_for_blank_transcription():
    assert build_voice_input(FakeRecognizer("   ")).capture() is None


@pytest.mark.parametrize("name", ["listen_timeout", "phrase_time_limit"])
def test_invalid_timeouts_are_rejected(name):
    kwargs = {name: 0}

    with pytest.raises(ValueError):
        VoiceInput(microphone_factory=FakeMicrophone, **kwargs)


def test_valid_capture_completes_within_response_target():
    started = time.perf_counter()

    assert build_voice_input(FakeRecognizer()).capture() == "Volume Up"

    assert time.perf_counter() - started < 2
