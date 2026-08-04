#!/usr/bin/env python3
"""Build public, optimized gallery images from the private handoff library."""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).parent
SOURCE = ROOT / "images" / "_library" / "cases"
OUTPUT = ROOT / "images" / "gallery"
FULL_MAX = (1280, 1280)
THUMB_SIZE = (480, 360)


def save_webp(source: Path, destination: Path, size: tuple[int, int], quality: int, crop: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        if crop:
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        else:
            image.thumbnail(size, Image.Resampling.LANCZOS)
        image.save(destination, "WEBP", quality=quality, method=6)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing private source library: {SOURCE}")

    sources = sorted(SOURCE.rglob("*.webp"))
    for source in sources:
        relative = source.relative_to(SOURCE)
        save_webp(source, OUTPUT / "full" / relative, FULL_MAX, quality=68, crop=False)
        if source.stem == "01":
            save_webp(source, OUTPUT / "thumbs" / relative, THUMB_SIZE, quality=65, crop=True)

    full_files = list((OUTPUT / "full").rglob("*.webp"))
    thumb_files = list((OUTPUT / "thumbs").rglob("*.webp"))
    total_bytes = sum(path.stat().st_size for path in full_files + thumb_files)
    print(f"Built {len(full_files)} full images and {len(thumb_files)} thumbnails ({total_bytes / 1048576:.1f} MB)")


if __name__ == "__main__":
    main()
