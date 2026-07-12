import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_changed.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_changed", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def init_repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test User")
    (tmp_path / "README.md").write_text("initial\n")
    git(tmp_path, "add", "README.md")
    git(tmp_path, "commit", "-qm", "initial")
    return tmp_path


def write_config(repo: Path, lanes: list[dict]) -> Path:
    path = repo / "checks.json"
    path.write_text(json.dumps({"version": 1, "lanes": lanes}))
    return path


def test_select_lanes_matches_changed_paths_once():
    module = load_module()
    lanes = [
        {"name": "python", "paths": ["**/*.py", "*.py"], "command": ["python3", "-m", "pytest"]},
        {"name": "docs", "paths": ["*.md", "docs/**"], "command": ["python3", "docs_check.py"]},
    ]

    selected = module.select_lanes(lanes, ["src/app.py", "README.md", "src/lib.py"])

    assert [lane["name"] for lane in selected] == ["python", "docs"]


def test_load_config_rejects_shell_strings_and_unknown_keys(tmp_path: Path):
    module = load_module()
    config = write_config(
        tmp_path,
        [{"name": "unsafe", "paths": ["**"], "command": "rm -rf /", "extra": True}],
    )

    with pytest.raises(ValueError, match="command.*array"):
        module.load_config(config)


def test_load_config_accepts_portable_argv_commands(tmp_path: Path):
    module = load_module()
    config = write_config(
        tmp_path,
        [{"name": "tests", "paths": ["**/*.py"], "command": ["python3", "-m", "pytest"]}],
    )

    assert module.load_config(config)[0]["name"] == "tests"


def test_cli_uses_base_and_untracked_files_and_runs_lanes_concurrently(tmp_path: Path):
    repo = init_repo(tmp_path)
    base = git(repo, "rev-parse", "HEAD")
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("print('changed')\n")
    git(repo, "add", "src/app.py")
    git(repo, "commit", "-qm", "add app")
    (repo / "notes.md").write_text("untracked\n")
    wait_for_other = (
        "import pathlib,time,sys\n"
        "p=pathlib.Path(sys.argv[1]); other=pathlib.Path(sys.argv[2])\n"
        "p.write_text('ready'); deadline=time.time()+2\n"
        "while not other.exists() and time.time()<deadline: time.sleep(.02)\n"
        "print('complete log output'); sys.exit(0 if other.exists() else 9)"
    )
    config = write_config(repo, [
        {"name": "python", "paths": ["**/*.py"], "command": [sys.executable, "-c", wait_for_other, "python.ready", "docs.ready"]},
        {"name": "docs", "paths": ["*.md"], "command": [sys.executable, "-c", wait_for_other, "docs.ready", "python.ready"]},
    ])

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--config", str(config), "--base", base],
        cwd=repo, text=True, capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS python" in result.stdout
    assert "PASS docs" in result.stdout
    logs = list((repo / ".tmp" / "check-runs").glob("*/python.log"))
    assert len(logs) == 1
    assert "complete log output" in logs[0].read_text()


def test_git_changed_paths_includes_deleted_tracked_files(tmp_path: Path):
    module = load_module()
    repo = init_repo(tmp_path)
    (repo / "removed.py").write_text("old\n")
    git(repo, "add", "removed.py")
    git(repo, "commit", "-qm", "add removable file")
    (repo / "removed.py").unlink()

    assert "removed.py" in module.git_changed_paths(repo, "HEAD")


def test_git_changed_paths_preserves_non_ascii_names(tmp_path: Path):
    module = load_module()
    repo = init_repo(tmp_path)
    (repo / "café.py").write_text("changed\n")

    changed = module.git_changed_paths(repo, "HEAD")

    assert "café.py" in changed
    assert [lane["name"] for lane in module.select_lanes(
        [{"name": "python", "paths": ["*.py"], "command": ["python3", "-V"]}],
        changed,
    )] == ["python"]


def test_cli_returns_nonzero_and_summarizes_failed_lane(tmp_path: Path):
    repo = init_repo(tmp_path)
    (repo / "broken.py").write_text("changed\n")
    config = write_config(repo, [{
        "name": "failing",
        "paths": ["*.py"],
        "command": [sys.executable, "-c", "print('full failure detail'); raise SystemExit(7)"],
    }])

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--config", str(config)],
        cwd=repo, text=True, capture_output=True,
    )

    assert result.returncode == 1
    assert "FAIL failing (exit 7)" in result.stdout
    assert "SUMMARY 0 passed, 1 failed" in result.stdout
    assert "full failure detail" not in result.stdout


def test_load_config_rejects_lane_names_that_could_escape_log_directory(tmp_path: Path):
    module = load_module()
    config = write_config(tmp_path, [{
        "name": "../escape", "paths": ["**"], "command": ["python3", "-V"]
    }])

    with pytest.raises(ValueError, match="lane names"):
        module.load_config(config)


def test_load_config_rejects_lane_names_too_long_for_log_files(tmp_path: Path):
    module = load_module()
    config = write_config(tmp_path, [{
        "name": "x" * 65, "paths": ["**"], "command": ["python3", "-V"]
    }])

    with pytest.raises(ValueError, match="lane names"):
        module.load_config(config)
