from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Dict, List


CATEGORY_RULES: Dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".html", ".css"},
}


@dataclass
class MoveResult:
    source: Path
    destination: Path


def get_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORY_RULES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_directory(directory: Path, move_files: bool = True) -> List[MoveResult]:
    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"Invalid directory: {directory}")

    results: List[MoveResult] = []

    for item in directory.iterdir():
        if item.is_dir():
            continue

        category = get_category(item)
        target_dir = directory / category
        target_dir.mkdir(exist_ok=True)

        target_path = target_dir / item.name
        if target_path.exists():
            stem, suffix = item.stem, item.suffix
            i = 1
            while True:
                candidate = target_dir / f"{stem}_{i}{suffix}"
                if not candidate.exists():
                    target_path = candidate
                    break
                i += 1

        results.append(MoveResult(source=item, destination=target_path))
        if move_files:
            shutil.move(str(item), str(target_path))

    return results
