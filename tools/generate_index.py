#!/usr/bin/env python3
"""Generate and validate Markdown indexes for handbook modules."""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from urllib.parse import quote


START_MARKER = "<!-- AUTO-INDEX:START -->"
END_MARKER = "<!-- AUTO-INDEX:END -->"
H1_PATTERN = re.compile(r"^#\s+(.+?)\s*$")
NUMBERED_PATTERN = re.compile(r"^(\d+)(?:[-_. ]|$)")

LINUX_GROUPS: tuple[tuple[str, str], ...] = (
    ("Concepts", "concepts"),
    ("Labs", "labs"),
    ("Troubleshooting", "troubleshooting"),
    ("Runbooks", "runbooks"),
    ("Real World Cases", "real-world"),
    ("Cheatsheets", "cheatsheets"),
    ("Common Mistakes", "common-mistakes"),
    ("Best Practices", "best-practices"),
)
LINUX_SUBSECTIONS: tuple[str, ...] = (
    "concepts",
    "troubleshooting",
    "runbooks",
    "cheatsheets",
    "labs",
    "real-world",
    "common-mistakes",
    "best-practices",
)


class IndexError(Exception):
    """Raised when an index cannot be generated or safely applied."""


@dataclass(frozen=True)
class Target:
    """A README and the groups of directories it indexes."""

    readme: Path
    groups: tuple[tuple[str | None, Path], ...]


@dataclass
class Summary:
    """Accumulate processing results for the final CLI report."""

    updated: list[Path]
    valid: list[Path]
    skipped: list[Path]
    failed: list[tuple[Path, str]]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Maintain generated Markdown indexes in handbook READMEs."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="update stale indexes")
    mode.add_argument("--check", action="store_true", help="check without writing")
    parser.add_argument(
        "--module",
        choices=("linux",),
        help="limit processing to one module (currently only linux)",
    )
    return parser.parse_args(argv)


def repository_root() -> Path:
    """Return the repository root based on this script's location."""
    return Path(__file__).resolve().parent.parent


def linux_targets(root: Path) -> tuple[Target, ...]:
    """Build the configured Linux README targets."""
    module = root / "linux"
    main = Target(
        module / "README.md",
        tuple((heading, module / directory) for heading, directory in LINUX_GROUPS),
    )
    subsections = tuple(
        Target(module / directory / "README.md", ((None, module / directory),))
        for directory in LINUX_SUBSECTIONS
    )
    return (main, *subsections)


def markdown_files(directory: Path) -> list[Path]:
    """Return directly contained Markdown documents, excluding README.md."""
    if not directory.is_dir():
        raise IndexError(f"source directory does not exist: {directory}")
    files = [
        path
        for path in directory.iterdir()
        if path.is_file()
        and path.suffix.lower() == ".md"
        and path.name.lower() != "readme.md"
    ]
    return sorted(files, key=document_sort_key)


def document_sort_key(path: Path) -> tuple[int, int, str]:
    """Sort leading-number documents numerically, then other names alphabetically."""
    match = NUMBERED_PATTERN.match(path.stem)
    if match:
        return (0, int(match.group(1)), path.name.casefold())
    return (1, 0, path.name.casefold())


def document_title(path: Path) -> str:
    """Extract the first ATX H1, falling back to a humanized filename."""
    try:
        with path.open("r", encoding="utf-8", newline=None) as document:
            for line in document:
                match = H1_PATTERN.match(line.rstrip("\r\n"))
                if match:
                    return match.group(1).strip().rstrip("#").rstrip()
    except (OSError, UnicodeError) as exc:
        raise IndexError(f"cannot read {path}: {exc}") from exc

    name = NUMBERED_PATTERN.sub("", path.stem, count=1)
    words = re.sub(r"[-_]+", " ", name).strip()
    return words.title() or path.stem


def markdown_link(document: Path, readme: Path) -> str:
    """Create a portable relative Markdown link from a README to a document."""
    relative = os.path.relpath(document, start=readme.parent)
    return quote(Path(relative).as_posix(), safe="/-._~")


def generated_body(target: Target) -> str:
    """Render the deterministic Markdown body for one target."""
    sections: list[str] = []
    for heading, directory in target.groups:
        lines: list[str] = []
        if heading is not None:
            lines.append(f"## {heading}")
            lines.append("")
        documents = markdown_files(directory)
        if documents:
            lines.extend(
                f"- [{document_title(path)}]({markdown_link(path, target.readme)})"
                for path in documents
            )
        else:
            lines.append("_No Markdown documents found._")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def replace_generated_region(original: str, body: str) -> str:
    """Replace only the uniquely delimited generated region."""
    if original.count(START_MARKER) != 1 or original.count(END_MARKER) != 1:
        raise IndexError("README must contain exactly one start marker and one end marker")
    start = original.index(START_MARKER)
    end = original.index(END_MARKER)
    if start >= end:
        raise IndexError("auto-index markers are in the wrong order")
    content_start = start + len(START_MARKER)
    return original[:content_start] + "\n\n" + body + "\n\n" + original[end:]


def read_utf8(path: Path) -> str:
    """Read a UTF-8 text file while normalizing line endings to LF in memory."""
    try:
        with path.open("r", encoding="utf-8", newline=None) as stream:
            return stream.read()
    except (OSError, UnicodeError) as exc:
        raise IndexError(f"cannot read README: {exc}") from exc


def atomic_write(path: Path, content: str) -> None:
    """Atomically write UTF-8 content using LF line endings."""
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(content)
        os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
        os.replace(temporary, path)
    except OSError as exc:
        raise IndexError(f"cannot write README: {exc}") from exc
    finally:
        if temporary is not None:
            try:
                Path(temporary).unlink(missing_ok=True)
            except OSError:
                pass


def process_target(target: Target, write: bool, summary: Summary) -> None:
    """Generate and either validate or update a single target README."""
    try:
        original = read_utf8(target.readme)
        expected = replace_generated_region(original, generated_body(target))
        if expected == original:
            summary.valid.append(target.readme)
        elif write:
            atomic_write(target.readme, expected)
            summary.updated.append(target.readme)
        else:
            summary.skipped.append(target.readme)
    except IndexError as exc:
        summary.failed.append((target.readme, str(exc)))


def display_path(path: Path, root: Path) -> str:
    """Return a concise repository-relative path when possible."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def print_summary(summary: Summary, root: Path) -> None:
    """Print counts plus actionable paths for stale and failed targets."""
    print(
        f"Summary: updated={len(summary.updated)}, valid={len(summary.valid)}, "
        f"skipped={len(summary.skipped)}, failed={len(summary.failed)}"
    )
    for path in summary.updated:
        print(f"UPDATED {display_path(path, root)}")
    for path in summary.valid:
        print(f"VALID   {display_path(path, root)}")
    for path in summary.skipped:
        print(f"STALE   {display_path(path, root)}")
    for path, reason in summary.failed:
        print(f"FAILED  {display_path(path, root)}: {reason}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the index generator and return a process exit status."""
    args = parse_args(argv)
    root = repository_root()
    summary = Summary(updated=[], valid=[], skipped=[], failed=[])

    module_factories = {
        "linux": linux_targets,
    }

    selected_modules = (
        [args.module]
        if args.module
        else list(module_factories)
    )

    for module_name in selected_modules:
        target_factory = module_factories[module_name]

        for target in target_factory(root):
            process_target(
                target,
                write=args.write,
                summary=summary,
            )

    print_summary(summary, root)

    if summary.failed:
        return 2

    if args.check and summary.skipped:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
