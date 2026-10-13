# SE_MINIPROJECT

Voice Assistant for Multimedia Controls: a simple Python assistant that controls volume, playback and tracks using voice commands. See [REQUIREMENTS.md](REQUIREMENTS.md) for the full requirements and work division.

## Project documentation

- [Software Requirements Specification (SRS)](docs/SRS.md)
- [Software Architecture and Design Specification (SAD)](docs/SAD.md)
- [Software Test Plan](docs/Test_Plan.md)

## Supported commands

Volume Up, Volume Down, Play, Pause, Resume, Next, Previous. Anything else is ignored without crashing.

## Setup

You need Python 3.12 and Git.

1. Clone the repo and go into the project folder:

```powershell
   git clone https://github.com/UjwalSanikam/SE_MINIPROJECT.git
   cd SE_MINIPROJECT
```

2. Create and activate a virtual environment (do this once, and activate it every time you open a new terminal):

```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```

   If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again. On macOS/Linux use `source .venv/bin/activate`.

3. Install the dependencies:

```powershell
   pip install -r requirements.txt
```

4. Run the tests from the repo root:

```powershell
   python -m pytest -v
```

### Adding a new dependency

Install it inside the venv, then refresh the file and commit it with your PR:

```powershell
pip install <package>
pip freeze | Out-File -Encoding utf8 requirements.txt
```

Tell the team in your PR description so everyone re-runs `pip install -r requirements.txt` after pulling.

## Project structure

```
src/
  common/          shared Command enum and MediaController interface
  command_parser/  text to Command mapping, invalid command handling
  volume/          volume control
  (more modules are added as each feature merges)
```

Each module keeps its own tests in a `tests/` folder next to the code.

## Workflow

- Branch from an up-to-date `main`, one branch per feature (`feature/<name>`).
- No direct pushes to `main`; open a PR and get at least one review from another member.
- Link the PR to its Jira user story.
- Run `python -m pytest -v` before pushing.
