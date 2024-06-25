import sqlite3
import requests
import os
import time
from tqdm import tqdm

# Database file path
db_path = 'pokemon_cards.db'
# Directory to save images (adjust to your external hard drive mount path)
images_dir = '/media/redfred/Expansion 2/Pokemon TCG'

# Create the directory if it does not exist
os.makedirs(images_dir, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get the image URLs from the database
cursor.execute("SELECT id, name, images FROM cards")
rows = cursor.fetchall()

total_images = len(rows)
downloaded_images = 0
failed_images = 0

# Iterate through the query results with a progress bar
for row in tqdm(rows, desc="Downloading images", unit="image"):
    card_id = row[0].replace('/', '_')  # Replace '/' with '_' to avoid directory issues
    card_name = row[1].replace('/', '_')  # Replace '/' with '_' to avoid directory issues
    images_json = row[2]

    # Extract the image URLs from the JSON object
    images_dict = eval(images_json)  # Converting string representation of dictionary to actual dictionary
    small_image_url = images_dict.get("small", "")
    large_image_url = images_dict.get("large", "")

    # Download the small image
    if small_image_url:
        try:
            response = requests.get(small_image_url, timeout=10)
            if response.status_code == 200:
                image_path = os.path.join(images_dir, f"{card_id}_{card_name}_small.png")
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                downloaded_images += 1
            else:
                print(f"Failed to download small image for {card_id} ({card_name}): {response.status_code}")
                failed_images += 1
        except Exception as e:
            print(f"Error downloading small image for {card_id} ({card_name}): {e}")
            failed_images += 1

    # Download the large image
    if large_image_url:
        try:
            response = requests.get(large_image_url, timeout=10)
            if response.status_code == 200:
                image_path = os.path.join(images_dir, f"{card_id}_{card_name}_large.png")
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                downloaded_images += 1
            else:
                print(f"Failed to download large image for {card_id} ({card_name}): {response.status_code}")
                failed_images += 1
        except Exception as e:
            print(f"Error downloading large image for {card_id} ({card_name}): {e}")
            failed_images += 1

    # Add a delay to avoid rate limiting (adjust as needed)
    time.sleep(0.1)

# Close the database connection
conn.close()

# Print the download summary
print(f"Total images processed: {total_images}")
print(f"Images successfully downloaded: {downloaded_images}")
print(f"Images failed to download: {failed_images}")
