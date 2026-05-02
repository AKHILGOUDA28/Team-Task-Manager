import os
import shutil

def move_all_files():
    source_dir = os.path.join(os.getcwd(), 'backend')
    dest_dir = os.getcwd()

    if not os.path.exists(source_dir):
        print(f"Error: source directory '{source_dir}' does not exist. Already moved?")
        return

    print(f"Moving all files from: {source_dir} -> {dest_dir}")

    # Walk through backend folder
    for root, dirs, files in os.walk(source_dir):
        # Determine target directory
        rel_path = os.path.relpath(root, source_dir)
        target_root = dest_dir if rel_path == "." else os.path.join(dest_dir, rel_path)

        # Create subdirectories if needed
        if not os.path.exists(target_root):
            os.makedirs(target_root)

        for filename in files:
            source_file = os.path.join(root, filename)
            target_file = os.path.join(target_root, filename)

            # Do not overwrite if it's identical or existing
            if os.path.exists(target_file):
                try:
                    os.remove(target_file)
                except OSError:
                    pass

            shutil.move(source_file, target_file)
            print(f" Moved: {os.path.relpath(target_file, dest_dir)}")

    # Clean up empty folders inside source_dir
    try:
        shutil.rmtree(source_dir)
        print("\n Successfully removed the 'backend' folder.")
    except Exception as e:
        print(f"\n Warning while removing 'backend' folder: {e}")

    print("\n All files successfully moved up to the root folder!")

if __name__ == '__main__':
    move_all_files()
