import os
import sys
import shutil
from datetime import datetime

def backup_files(source_dir, dest_dir):
    # Check if source directory exists
    if not os.path.isdir(source_dir):
        print(f"❌ Error: Source directory '{source_dir}' does not exist.")
        return

    # Check if destination directory exists
    if not os.path.isdir(dest_dir):
        print(f"❌ Error: Destination directory '{dest_dir}' does not exist.")
        return

    # Iterate through all files in the source directory
    for filename in os.listdir(source_dir):
        src_file = os.path.join(source_dir, filename)

        # Proceed only if it's a file (ignore folders)
        if os.path.isfile(src_file):
            dest_file = os.path.join(dest_dir, filename)

            # If a file with the same name already exists, append timestamp
            if os.path.exists(dest_file):
                base, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f"{base}_{timestamp}{ext}"
                dest_file = os.path.join(dest_dir, new_filename)

            try:
                shutil.copy2(src_file, dest_file)
                print(f"✅ Copied: {filename} → {dest_file}")
            except Exception as e:
                print(f"❌ Failed to copy '{filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python backup.py /path/to/source /path/to/destination")
        sys.exit(1)

    source_path = sys.argv[1]
    destination_path = sys.argv[2]

    backup_files(source_path, destination_path)
