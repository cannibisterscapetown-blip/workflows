#!/usr/bin/env python3
"""
Utility to resize and compress images so they are within Claude API limits.

Claude API limits:
  - Max image size: 5MB (base64-encoded ~3.75MB raw)
  - Max dimensions: 8000 x 8000 px
  - Supported formats: JPEG, PNG, GIF, WEBP
"""
import io
import os
import sys
from PIL import Image

MAX_BYTES = 3_500_000   # ~3.5 MB raw keeps base64 well under 5 MB
MAX_DIM = 4096          # Generous but safe upper bound for each axis
JPEG_QUALITY = 85


def prepare_for_claude(source_path: str, dest_path: str | None = None) -> str:
    """
    Resize and compress an image so it can be sent to Claude API.

    Returns the path to the processed image (dest_path if given, otherwise
    overwrites source with a temp file, saves alongside original as
    <name>_claude.<ext>).
    """
    with Image.open(source_path) as img:
        # Convert palette / CMYK to RGBA or RGB
        if img.mode in ("P", "CMYK"):
            img = img.convert("RGBA" if "transparency" in img.info else "RGB")

        # Downscale if either dimension exceeds MAX_DIM
        if img.width > MAX_DIM or img.height > MAX_DIM:
            img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

        # Choose output format: keep PNG only if source is PNG and small enough
        src_ext = os.path.splitext(source_path)[1].lower()
        use_jpeg = src_ext not in (".png", ".gif", ".webp")

        # If destination not specified, derive it
        if dest_path is None:
            base, ext = os.path.splitext(source_path)
            out_ext = ".jpg" if use_jpeg else ext
            dest_path = f"{base}_claude{out_ext}"

        # Iteratively reduce quality until file fits within MAX_BYTES
        quality = JPEG_QUALITY
        while True:
            buf = io.BytesIO()
            if use_jpeg or img.mode == "RGB":
                save_img = img.convert("RGB")
                save_img.save(buf, format="JPEG", quality=quality, optimize=True)
            else:
                img.save(buf, format="PNG", optimize=True)

            size = buf.tell()
            if size <= MAX_BYTES or quality <= 20:
                break
            quality -= 10

        with open(dest_path, "wb") as f:
            f.write(buf.getvalue())

    print(
        f"✅  {os.path.basename(source_path)} "
        f"({os.path.getsize(source_path) // 1024}KB) → "
        f"{os.path.basename(dest_path)} ({os.path.getsize(dest_path) // 1024}KB)"
    )
    return dest_path


def prepare_directory(directory: str = ".") -> None:
    """Prepare all images in a directory."""
    exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    processed = 0
    for fname in os.listdir(directory):
        base, ext = os.path.splitext(fname)
        if ext.lower() not in exts:
            continue
        if base.endswith("_claude"):
            continue  # Already processed
        src = os.path.join(directory, fname)
        if os.path.getsize(src) <= MAX_BYTES:
            continue  # Already small enough
        prepare_for_claude(src)
        processed += 1
    if processed == 0:
        print("All images are already within Claude API size limits.")
    else:
        print(f"\nPrepared {processed} image(s).")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No args → process current directory
        prepare_directory(".")
    elif len(sys.argv) == 2:
        path = sys.argv[1]
        if os.path.isdir(path):
            prepare_directory(path)
        else:
            prepare_for_claude(path)
    elif len(sys.argv) == 3:
        prepare_for_claude(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 prepare_image_for_claude.py [source_image | directory] [dest_image]")
        sys.exit(1)
