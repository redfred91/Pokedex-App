import os
import shutil
import numpy as np
import tensorflow as tf
from datetime import datetime
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, CSVLogger

def archive_logs(log_dir, archive_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for log_file in ['training_log.txt', 'feedback_log.txt']:
        src = os.path.join(log_dir, log_file)
        if os.path.exists(src):
            dst = os.path.join(archive_dir, f"{log_file}_{timestamp}")
            shutil.move(src, dst)

log_dir = '/home/t1000/Pokedex_Project/models'
archive_dir = '/home/t1000/Pokedex_Project/models/archive'

archive_logs(log_dir, archive_dir)

if not tf.config.list_physical_devices('GPU'):
    raise SystemError('GPU device not found')

physical_devices = tf.config.list_physical_devices('GPU')
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)

policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

tf.keras.backend.clear_session()

images = np.load('/home/t1000/Pokedex_Project/data/images.npy')
labels = np.load('/home/t1000/Pokedex_Project/data/labels.npy')
boxes = np.load('/home/t1000/Pokedex_Project/data/boxes.npy')

X_train, X_test, y_train, y_test, b_train, b_test = train_test_split(images, labels, boxes, test_size=0.2, random_state=42)

train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator()

train_generator = train_datagen.flow(X_train, [y_train, b_train], batch_size=32)
validation_generator = test_datagen.flow(X_test, [y_test, b_test], batch_size=32)

input_layer = Input(shape=(224, 224, 3))
base_model = MobileNet(weights='imagenet', include_top=False, input_tensor=input_layer)
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x_class = Dense(512, activation='relu')(x)
x_class = Dense(labels.shape[1], activation='softmax', dtype='float32', name='class_output')(x_class)
x_box = Dense(512, activation='relu')(x)
x_box = Dense(4, activation='sigmoid', dtype='float32', name='box_output')(x_box)

model = Model(inputs=input_layer, outputs=[x_class, x_box])

model.compile(optimizer='adam',
              loss={'class_output': 'categorical_crossentropy', 'box_output': 'mse'},
              metrics={'class_output': 'accuracy', 'box_output': 'mse'})

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
csv_logger = CSVLogger(os.path.join(log_dir, 'training_log.txt'), append=False)

history = model.fit(train_generator, validation_data=validation_generator, epochs=50, callbacks=[early_stopping, csv_logger])

model.save(os.path.join(log_dir, 'pokemon_card_classifier.h5'))

def capture_feedback(predictions, labels, boxes, threshold=0.2):
    class_preds, box_preds = predictions
    incorrect_indices = np.where(class_preds.max(axis=1) < threshold)[0]
    feedback_file = os.path.join(log_dir, 'feedback_log.txt')
    with open(feedback_file, 'w') as f:
        if len(incorrect_indices) > 0:
            for idx in incorrect_indices:
                f.write(f"Review image {idx}: predicted {np.argmax(class_preds[idx])}, true label {labels[idx]}, predicted box {box_preds[idx]}, true box {boxes[idx]}\n")
        else:
            f.write("No low confidence predictions to review.\n")

predictions = model.predict(X_test)
capture_feedback(predictions, y_test, b_test, threshold=0.2)
