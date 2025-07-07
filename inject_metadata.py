
#!/usr/bin/env python3

import os
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from tqdm import tqdm
import argparse

SUPPORTED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp', '.bmp',
    '.mp4', '.mov', '.avi', '.3gp', '.mkv', '.wmv'
}

IMAGE_TAGS = {
    'AllDates': 'dateTaken',
    'Description': 'description',
    'GPSLatitude': 'latitude',
    'GPSLongitude': 'longitude',
    'Rating': 'rating'
}

VIDEO_TAGS = {
    'CreateDate': 'dateTaken',
    'Description': 'description',
    'GPSLatitude': 'latitude',
    'GPSLongitude': 'longitude',
    'Rating': 'rating'
}

def find_sidecar_strict(media_file: Path):
    base_name = media_file.name
    json_path_lower = media_file.with_name(f"{base_name}.json")
    json_path_upper = media_file.with_name(f"{base_name}.JSON")
    if json_path_lower.exists():
        return json_path_lower
    if json_path_upper.exists():
        return json_path_upper
    return None

def process_file(media_file, delete_sidecar=False):
    sidecar_file = find_sidecar_strict(media_file)
    if not sidecar_file:
        return False, False, "No sidecar"

    try:
        with open(sidecar_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except json.JSONDecodeError:
        return False, False, "Invalid JSON"

    date_taken = metadata.get('dateTaken')
    future_date = False
    if date_taken:
        try:
            dt = datetime.fromisoformat(date_taken.replace("Z", "+00:00"))
            if dt > datetime.now(tz=timezone.utc):
                future_date = True
        except ValueError:
            return False, False, "Invalid date format"

    ext = media_file.suffix.lower()
    is_video = ext in {'.mp4', '.mov', '.avi', '.3gp', '.mkv', '.wmv'}
    tag_map = VIDEO_TAGS if is_video else IMAGE_TAGS

    cmd = ['exiftool', '-overwrite_original']
    for exif_tag, json_key in tag_map.items():
        if json_key in metadata:
            value = metadata[json_key]
            cmd.append(f"-{exif_tag}={value}")
    cmd.append(str(media_file))

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    success = result.returncode == 0

    if success and delete_sidecar:
        try:
            sidecar_file.unlink()
        except OSError:
            pass

    return success, future_date, None

def process_directory(directory, delete_sidecars=False):
    media_files = [p for p in Path(directory).rglob('*') if p.suffix.lower() in SUPPORTED_EXTENSIONS]
    modified_count = 0
    future_dates = []
    skipped_files = []

    for media_file in tqdm(media_files, desc="Processing media files"):
        success, future_date, reason = process_file(media_file, delete_sidecars)
        if success:
            modified_count += 1
        elif future_date:
            future_dates.append(str(media_file))
        elif reason:
            skipped_files.append((str(media_file), reason))

    print(f"\n✅ Metadata written to {modified_count} files.")
    if future_dates:
        print(f"⚠️  Suspicious future dates found in {len(future_dates)} files:")
        for f in future_dates:
            print("   -", f)
    if skipped_files:
        print(f"⚠️  Skipped {len(skipped_files)} files due to errors:")
        for f, reason in skipped_files:
            print(f"   - {f}: {reason}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Immich sidecar metadata to media files using ExifTool.")
    parser.add_argument("directory", help="Directory containing media files and .JSON sidecars")
    parser.add_argument("--delete-sidecars", action="store_true", help="Delete JSON sidecars after applying metadata")
    args = parser.parse_args()
    process_directory(args.directory, args.delete_sidecars)
