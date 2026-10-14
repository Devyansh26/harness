from pathlib import Path
import os
import subprocess
import time
from typing import Any

WORKSPACE = (Path.cwd() / "workspace").resolve()

MAX_OUTPUT_CHARS = 30_000
DEFAULT_TIMEOUT = 30
MAX_TIMEOUT = 300


def _resolve_cwd(cwd: str | None = None) -> Path:
    """Resolve a working directory relative to WORKSPACE."""
    target = (WORKSPACE / (cwd or ".")).resolve()

    if not target.is_relative_to(WORKSPACE):
        raise PermissionError("Working directory must be inside workspace")

    if not target.exists():
        raise FileNotFoundError(f"Directory not found: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Not a directory: {target}")

    return target


def run_command(
    command: str,
    cwd: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    Execute a Bash command and return a structured result.

    IMPORTANT: This runs on the host OS. Use an isolated container
    before allowing autonomous or untrusted command execution.
    """
    if not command or not command.strip():
        raise ValueError("Command cannot be empty")

    if not isinstance(timeout, int) or isinstance(timeout, bool):
        raise ValueError("Timeout must be an integer")

    if not 1 <= timeout <= MAX_TIMEOUT:
        raise ValueError(f"Timeout must be between 1 and {MAX_TIMEOUT}")

    working_dir = _resolve_cwd(cwd)
    started = time.monotonic()

    try:
        result = subprocess.run(
            command,
            shell=True,
            executable="/bin/bash",
            cwd=working_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )

        stdout = result.stdout
        stderr = result.stderr

        return {
            "command": command,
            "cwd": str(working_dir.relative_to(WORKSPACE)),
            "exit_code": result.returncode,
            "stdout": stdout[-MAX_OUTPUT_CHARS:],
            "stderr": stderr[-MAX_OUTPUT_CHARS:],
            "duration_seconds": round(time.monotonic() - started, 3),
            "timed_out": False,
        }

    except subprocess.TimeoutExpired as exc:
        def decode(value):
            if value is None:
                return ""
            if isinstance(value, bytes):
                return value.decode("utf-8", errors="replace")
            return value

        return {
            "command": command,
            "cwd": str(working_dir.relative_to(WORKSPACE)),
            "exit_code": None,
            "stdout": decode(exc.stdout)[-MAX_OUTPUT_CHARS:],
            "stderr": decode(exc.stderr)[-MAX_OUTPUT_CHARS:],
            "duration_seconds": round(time.monotonic() - started, 3),
            "timed_out": True,
            "error": f"Command timed out after {timeout} seconds",
        }


def list_directory(cwd: str | None = None) -> dict[str, Any]:
    """List files and directories in a workspace directory."""
    working_dir = _resolve_cwd(cwd)

    entries = []
    for path in sorted(working_dir.iterdir(), key=lambda p: p.name.lower()):
        entries.append({
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
        })

    return {
        "cwd": str(working_dir.relative_to(WORKSPACE)),
        "entries": entries,
    }
