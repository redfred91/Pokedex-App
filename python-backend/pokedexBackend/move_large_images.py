import os
import shutil

# Define the source directory and the new directory for large images
source_dir = '/home/redfred/Documents/Pokemon TCG'
large_images_dir = '/home/redfred/Documents/Pokemon TCG/Large Images'

# Create the directory for large images if it doesn't exist
os.makedirs(large_images_dir, exist_ok=True)

# Iterate over the files in the source directory
for filename in os.listdir(source_dir):
    # Check if the file is a large image
    if '_large' in filename:
        # Construct full file path
        src_file = os.path.join(source_dir, filename)
        dest_file = os.path.join(large_images_dir, filename)

        # Move the file to the new directory
        shutil.move(src_file, dest_file)

print("Large images have been moved successfully.")
