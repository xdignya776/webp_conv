import os
import shutil
from PIL import Image

# Supported RAW formats
RAW_EXTENSIONS = ('.nef', '.dng', '.cr2', '.arw', '.rw2', '.orf', '.raf', '.sr2')

def organize_and_convert_images(base_dir):
    raw_dir = os.path.join(base_dir, 'raw_files')
    jpg_dir = os.path.join(base_dir, 'jpg_files')
    webp_dir = os.path.join(jpg_dir, 'webp_converted')

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(jpg_dir, exist_ok=True)
    os.makedirs(webp_dir, exist_ok=True)

    for filename in os.listdir(base_dir):
        file_path = os.path.join(base_dir, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        # Move RAW files
        if ext in RAW_EXTENSIONS:
            shutil.move(file_path, os.path.join(raw_dir, filename))
            print(f"Moved RAW: {filename}")
        # Move JPG files
        elif ext in ('.jpg', '.jpeg'):
            dest_path = os.path.join(jpg_dir, filename)
            shutil.move(file_path, dest_path)
            print(f"Moved JPG: {filename}")

    # Convert JPG to WebP
    for filename in os.listdir(jpg_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            jpg_path = os.path.join(jpg_dir, filename)
            webp_path = os.path.join(webp_dir, os.path.splitext(filename)[0] + '.webp')

            try:
                with Image.open(jpg_path) as img:
                    img = img.convert("RGB")
                    img.save(webp_path, "webp", quality=80, method=6)
                    print(f"Converted to WebP: {filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python convert_to_webp.py /path/to/image-folder")
    else:
        organize_and_convert_images(sys.argv[1])