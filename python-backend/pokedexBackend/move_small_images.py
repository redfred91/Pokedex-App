import os
import shutil

# Define the source directory and the new directory for small images
source_dir = '/home/redfred/Documents/Pokemon TCG'
small_images_dir = '/home/redfred/Documents/Pokemon TCG/Small Images'

# Create the directory for small images if it doesn't exist
os.makedirs(small_images_dir, exist_ok=True)

# Iterate over the files in the source directory
for filename in os.listdir(source_dir):
    # Check if the file is a small image
    if '_small' in filename:
        # Construct full file path
        src_file = os.path.join(source_dir, filename)
        dest_file = os.path.join(small_images_dir, filename)

        # Move the file to the new directory
        shutil.move(src_file, dest_file)

print("Small images have been moved successfully.")
