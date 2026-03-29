import os
from PIL import Image

dataset_path = "dataset"

valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")

deleted = 0

for root, dirs, files in os.walk(dataset_path):
    for file in files:
        file_path = os.path.join(root, file)

        # Step 1: Extension check
        if not file.lower().endswith(valid_extensions):
            print("❌ Removing non-image:", file_path)
            os.remove(file_path)
            deleted += 1
            continue

        # Step 2: Try opening image
        try:
            with Image.open(file_path) as img:
                img.convert("RGB")  # force valid format
        except:
            print("❌ Removing corrupt image:", file_path)
            os.remove(file_path)
            deleted += 1

print(f"✅ Cleaning done! Removed {deleted} bad files")