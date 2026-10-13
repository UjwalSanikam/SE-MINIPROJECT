# Software Test Plan

**Project:** Voice Assistant for Multimedia Controls  
**Version:** 1.0-draft  
**Date:** 12 October 2026  
**Status:** Draft—pending team and instructor approval  
**References:** SRS v1.0-draft; SAD v1.0-draft

## 1. Introduction

### 1.1 Purpose

This plan defines how the project team will verify that the voice assistant meets its SRS requirements and handles failure conditions safely.

### 1.2 Scope

Testing covers voice input, text normalisation, command recognition, command dispatch, volume/playback/track features, backend-error handling, response time, and static security checks. It covers automated unit and integration tests plus a short manual test using a real microphone and media player.

### 1.3 References and definitions

Requirements use the identifiers in `docs/SRS.md`. Test cases use the identifiers below. STT means speech-to-text; RTM means Requirements Traceability Matrix.

## 2. Test items

- `src/voice_input/` — microphone capture and STT handling
- `src/command_parser/` — normalisation, aliases, unsupported input
- `src/volume/` — volume increase/decrease requests
- `src/playback/` — play/pause/resume requests and state
- `src/track/` — next/previous requests
- `src/media_backend/` — operating-system/media-player adapter
- `src/main.py` — dispatcher and command loop
- `.github/workflows/` — continuous validation

## 3. Features to be tested

| Feature | SRS requirements |
| --- | --- |
| Capture and recognition | FR-01 to FR-04 |
| Text normalisation and allow-list parsing | FR-05, FR-13, SR-03 |
| Volume control | FR-06, FR-07 |
| Playback control | FR-08 to FR-10 |
| Track control | FR-11, FR-12 |
| Dispatcher and backend resilience | FR-14, FR-15, NFR-02, SR-04 |
| Performance and modularity | NFR-01, NFR-03 |
| CI/security and privacy checks | NFR-04, NFR-05, SR-01, SR-02, SR-05 |

## 4. Features not to be tested

- Accuracy, availability, or internal implementation of a third-party cloud STT service.
- Hardware-driver and operating-system implementation of a microphone or media player.
- Actual media decoding, playlist management, user accounts, or storage.
- Security controls outside the project repository, such as GitHub account authentication.

## 5. Test approach and strategy

### 5.1 Security validation

- Run Bandit against production source and Flake8 against all source modules.
- Review dependencies for declared/pinned versions before the release.
- Verify that parser tests reject unexpected text and that no direct shell command is formed from recognised speech.
- Inspect normal-operation code and logs to confirm it does not save audio/transcripts or write secrets.
- Inject STT, microphone, and backend failures; confirm no traceback, unintended backend call, or process termination.

### 5.2 Test levels and types

| Level/type | Method | Owner |
| --- | --- | --- |
| Unit | Pytest with fakes/mocks for recognizer and `MediaController`. | Module owner |
| Integration | Run dispatcher with a fake recognizer and fake backend. | Integration owner |
| System/manual | Speak each command into the target microphone and observe media control. | Whole team |
| Performance | Time 100 parser/dispatcher runs using a deterministic fake recognizer. | Rohan |
| Static/security | Run `flake8`, `bandit`, and dependency review in CI. | Ujwal |

### 5.3 Entry and exit criteria

**Entry:** source is merged or in a reviewable PR; dependencies install; fakes/mocks exist for unavailable hardware; expected results are documented.

**Exit:** all planned tests execute; 100% of High-priority FR tests pass; no open critical/high defect; security checks pass; RTM has a test for every SRS requirement; any known platform limitation is documented.

## 6. Test environment

| Area | Configuration |
| --- | --- |
| OS | Developer laptop supported by the chosen backend |
| Runtime | Python 3.12+ virtual environment |
| Test tools | pytest, unittest.mock, Flake8, Bandit |
| Hardware test | Default microphone, speakers/headphones, a controllable media player |
| CI | GitHub Actions running on pull requests and pushes to `main` |
| Test doubles | Fake recognizer, microphone factory, and `MediaController` |

## 7. Test schedule

| Milestone | Target |
| --- | --- |
| Finalise test cases and traceability | Before Sprint 1 starts |
| Implement unit tests alongside each feature | During Sprint 1 |
| Add CI and run security validation | During Sprint 1 |
| Integrate real backend and manual system test | Sprint 2 |
| Regression, test summary, and sign-off | Before development freeze |

## 8. Test deliverables

- This test plan and requirements traceability matrix
- Pytest test modules and manual test evidence
- CI run links/logs
- Defect list and final test summary

## 9. Roles and responsibilities

| Role | Assigned member | Responsibility |
| --- | --- | --- |
| Test coordinator | Rohan | Maintain RTM, performance evidence, and test summary. |
| Quality/security owner | Ujwal | Static checks, dependency/security validation. |
| CI owner | Venkatesh | GitHub Actions and coverage/test reports. |
| Sprint/defect coordinator | Yashas | Board status, backlog and defect tracking. |
| All feature owners | Whole team | Add and run tests for their feature. |

## 10. Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| No microphone/PyAudio on CI | Voice test cannot use physical audio | Use injected fakes for automated tests; reserve device test for manual validation. |
| STT provider/network unavailable | Recognition fails | Test the safe failure path and show a concise result. |
| OS media APIs differ | Backend not portable | Isolate OS-specific code in `media_backend`; test feature modules against the interface. |
| Late integration | Features work only separately | Add dispatcher integration test early and demo it each sprint. |
| Missing CI evidence | Quality cannot be shown | Add Actions workflow before feature PRs are merged. |

## 11. Test cases

| ID | Requirement(s) | Preconditions | Steps / input | Expected result |
| --- | --- | --- | --- | --- |
| TC-01 | FR-01, FR-02 | Fake microphone and recognizer return `Volume Up`. | Call `capture()`. | Returns trimmed `Volume Up`; recognizer receives timeout limits. |
| TC-02 | FR-03 | Fake recognizer raises timeout. | Call `capture()`. | Returns no text; no exception escapes. |
| TC-03 | FR-04, NFR-02, SR-04 | Fakes raise `UnknownValueError` and service error. | Call `capture()` for each failure. | Safe no-text result; application remains usable. |
| TC-04 | FR-05 | Parser available. | Parse `  Volume Up! `. | Returns `VOLUME_UP`. |
| TC-05 | FR-06, FR-07 | Fake backend records calls. | Dispatch Volume Up and Volume Down. | Exactly one matching backend action per command. |
| TC-06 | FR-08 to FR-10 | Fake backend records calls. | Dispatch Play, Pause, Resume. | Matching methods called and playback state changes after success. |
| TC-07 | FR-11, FR-12 | Fake backend records calls. | Dispatch Next and Previous. | Matching track method called exactly once. |
| TC-08 | FR-13, SR-03 | Fake backend records calls. | Parse/dispatch `dance` and punctuation-only input. | Unsupported result; zero backend calls. |
| TC-09 | FR-14 | Fake recognizer and fake backend installed. | Run one dispatcher cycle for every supported command. | Each input reaches one, and only one, feature operation. |
| TC-10 | FR-15, NFR-02 | Backend method raises `RuntimeError`. | Invoke a feature operation. | Clear failure result; state is preserved where applicable; no crash. |
| TC-11 | NFR-01 | Deterministic fakes installed. | Run 100 capture-to-dispatch iterations and time them. | At least 95 complete in under two seconds after recognised text. |
| TC-12 | NFR-03 | Source tree available. | Review feature-module imports. | Features only depend on `MediaController`; OS calls are in backend. |
| TC-13 | NFR-04, NFR-05, SR-05 | CI workflow configured. | Open a PR. | Pytest, Flake8, and Bandit run and report status. |
| TC-14 | NFR-06 | CLI executable. | Trigger successful, unsupported, and failure paths. | Every path presents an understandable concise message. |
| TC-15 | SR-01, SR-02 | Source/log configuration available. | Review code and generated logs after test. | No audio/transcript/secrets/device identifier stored or logged. |

## 12. Traceability summary

The SRS RTM maps every FR, NFR, and security requirement to TC-01 through TC-15. Test execution status will be updated to Pass/Fail/Blocked in the final test summary rather than assumed in this draft.

