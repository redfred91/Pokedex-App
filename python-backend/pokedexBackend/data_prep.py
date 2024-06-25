import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array

def load_images_from_folder(folder, size=(128, 128)):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith("_small.png"):
            label = filename.split('_')[0]  # Extract the label (card ID) from the filename
            img = cv2.imread(os.path.join(folder, filename))
            if img is not None:
                img = cv2.resize(img, size)
                img = img_to_array(img)
                images.append(img)
                labels.append(label)
    return np.array(images), np.array(labels)

small_images_dir = '/home/redfred/Documents/Pokemon TCG/Small Images'
images, labels = load_images_from_folder(small_images_dir)

# Normalize the images
images = images.astype('float32') / 255.0

# Save the preprocessed data
np.save('images.npy', images)
np.save('labels.npy', labels)

print("Images and labels have been preprocessed and saved.")
