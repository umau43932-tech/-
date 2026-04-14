#!/usr/bin/env python3
"""ファイルを拡張子ごとに整理するCLIアプリ。"""

from __future__ import annotations

import argparse
import shutil
from collections import defaultdict
from pathlib import Path

CATEGORY_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".html", ".css"},
}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "others" if ext else "no_extension"


def unique_destination(target_dir: Path, filename: str) -> Path:
    candidate = target_dir / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    i = 1
    while True:
        new_name = f"{stem}_{i}{suffix}"
        candidate = target_dir / new_name
        if not candidate.exists():
            return candidate
        i += 1


def organize_files(source: Path, dry_run: bool = False, recursive: bool = False) -> dict[str, int]:
    if not source.exists() or not source.is_dir():
        raise ValueError(f"有効なディレクトリではありません: {source}")

    pattern = "**/*" if recursive else "*"
    moved_count: dict[str, int] = defaultdict(int)

    for item in source.glob(pattern):
        if not item.is_file():
            continue

        category = category_for(item)
        target_dir = source / category

        if item.parent == target_dir:
            continue

        destination = unique_destination(target_dir, item.name)

        if dry_run:
            print(f"[DRY RUN] {item} -> {destination}")
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} -> {category}/{destination.name}")

        moved_count[category] += 1

    return dict(moved_count)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="フォルダ内のファイルをカテゴリ別に整理します")
    parser.add_argument("source", type=Path, help="整理対象のディレクトリ")
    parser.add_argument("--dry-run", action="store_true", help="実際には移動せず結果だけ表示")
    parser.add_argument("--recursive", action="store_true", help="サブフォルダも含めて整理")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = organize_files(args.source, dry_run=args.dry_run, recursive=args.recursive)

    if not result:
        print("移動対象ファイルはありませんでした。")
        return

    print("\n整理完了:")
    for category, count in sorted(result.items()):
        print(f"- {category}: {count}件")


if __name__ == "__main__":
    main()
