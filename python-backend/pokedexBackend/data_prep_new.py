import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import time

def load_and_augment_images_from_folder(folder, size=(224, 224), sample_size=None):
    images = []
    labels = []
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )

    print(f"Loading images from: {folder}")
    start_time = time.time()

    for i, filename in enumerate(os.listdir(folder)):
        if filename.endswith(".png"):
            if sample_size and i >= sample_size:
                break
            label = filename.split('_')[0]
            img = cv2.imread(os.path.join(folder, filename))
            if img is not None:
                img = cv2.resize(img, size)
                img = img_to_array(img)
                images.append(img)
                labels.append(label)

                # Apply data augmentation
                img = img.reshape((1,) + img.shape)
                for batch in datagen.flow(img, batch_size=1):
                    augmented_img = batch[0].astype('float32')
                    images.append(augmented_img)
                    labels.append(label)
                    break

            # Log progress every 10 images
            if (i + 1) % 10 == 0:
                elapsed_time = time.time() - start_time
                print(f"Processed {i + 1} images in {elapsed_time:.2f} seconds")

    end_time = time.time()
    print(f"Finished loading images at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time))}")
    print(f"Total loading time: {end_time - start_time} seconds")

    return np.array(images), np.array(labels)

def load_image_into_numpy_array(path):
    return np.array(cv2.imread(path))

def detect_objects(image_np, model, name_roi, number_roi, central_image_roi):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = model(input_tensor)

    detection_boxes = detections['detection_boxes'][0].numpy()
    detection_scores = detections['detection_scores'][0].numpy()
    detection_classes = detections['detection_classes'][0].numpy()

    # Filter detections based on ROIs
    filtered_boxes = []
    for i in range(detection_boxes.shape[0]):
        box = detection_boxes[i]
        score = detection_scores[i]
        if score > 0.5:
            ymin, xmin, ymax, xmax = box
            if (name_roi[0] <= ymin <= name_roi[2] and name_roi[1] <= xmin <= name_roi[3]) or \
               (number_roi[0] <= ymin <= number_roi[2] and number_roi[1] <= xmin <= number_roi[3]) or \
               (central_image_roi[0] <= ymin <= central_image_roi[2] and central_image_roi[1] <= xmin <= central_image_roi[3]):
                filtered_boxes.append((box, score, detection_classes[i]))

    return filtered_boxes

model_dir = '/home/t1000/Pokedex_Project/models/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8'
model = tf.saved_model.load(os.path.join(model_dir, 'saved_model'))

large_images_dir = '/home/t1000/Pokedex_Project/data/pokemon_card_images/large_images'
images, labels = load_and_augment_images_from_folder(large_images_dir, sample_size=100)

images = images.astype('float32') / 255.0

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(labels)

one_hot_labels = to_categorical(integer_encoded)

output_file = '/home/t1000/Pokedex_Project/data/boxes.npy'

annotations = []
start_time = time.time()

# Define ROIs for name, series number, and central image
name_roi = [0.0, 0.0, 0.2, 1.0]  # Top 20% of the image
number_roi = [0.9, 0.0, 1.0, 1.0]  # Bottom 10% of the image
central_image_roi = [0.2, 0.0, 0.7, 1.0]  # Middle 50% of the image

for filename in os.listdir(large_images_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(large_images_dir, filename)
        image_np = load_image_into_numpy_array(image_path)
        filtered_boxes = detect_objects(image_np, model, name_roi, number_roi, central_image_roi)
        
        # Process the filtered boxes
        for box, score, class_id in filtered_boxes:
            ymin, xmin, ymax, xmax = box
            (im_height, im_width, _) = image_np.shape
            (xmin, xmax, ymin, ymax) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
            annotations.append([filename, float(xmin), float(ymin), float(xmax), float(ymax)])

end_time = time.time()
print(f"Finished bounding box extraction at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time))}")
print(f"Total bounding box extraction time: {end_time - start_time} seconds")

boxes = np.array(annotations)
np.save(output_file, boxes)

output_dir = '/home/t1000/Pokedex_Project/data'
os.makedirs(output_dir, exist_ok=True)

np.save(os.path.join(output_dir, 'images.npy'), images)
np.save(os.path.join(output_dir, 'labels.npy'), one_hot_labels)

visualization_output_dir = '/home/t1000/Pokedex_Project/data/visualizations'
os.makedirs(visualization_output_dir, exist_ok=True)

def save_bounding_box_images(images, boxes, sample_size=10):
    timestamp = int(time.time())
    for i in range(sample_size):
        image = images[i]
        box = boxes[i, 1:]
        print(f"Image {i} Box coordinates: {box}")
        image = (image * 255).astype(np.uint8)
        try:
            cv2.rectangle(image, (int(float(box[0])), int(float(box[1]))), (int(float(box[2])), int(float(box[3]))), (0, 255, 0), 2)
        except ValueError as e:
            print(f"Error drawing box on image {i}: {e}")
            continue
        output_path = os.path.join(visualization_output_dir, f"image_with_box_{timestamp}_{i}.png")
        cv2.imwrite(output_path, image)

save_bounding_box_images(images, boxes, sample_size=10)
