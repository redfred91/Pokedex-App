import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

images = np.load('/home/t1000/Pokedex_Project/data/images.npy')
labels = np.load('/home/t1000/Pokedex_Project/data/labels.npy')

_, X_test, _, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

model = tf.keras.models.load_model('/home/t1000/Pokedex_Project/models/pokemon_card_classifier.h5')

loss, accuracy = model.evaluate(X_test, y_test, verbose=2)
with open('/home/t1000/Pokedex_Project/models/evaluation_log.txt', 'w') as f:
    f.write(f'Test loss: {loss}\n')
    f.write(f'Test accuracy: {accuracy}\n')

def capture_feedback(predictions, labels, threshold=0.2):
    incorrect_indices = np.where(predictions.max(axis=1) < threshold)[0]
    with open('/home/t1000/Pokedex_Project/models/evaluation_feedback_log.txt', 'w') as f:
        if len(incorrect_indices) > 0:
            for idx in incorrect_indices:
                f.write(f"Review image {idx}: predicted {np.argmax(predictions[idx])}, true label {labels[idx]}\n")
        else:
            f.write("No low confidence predictions to review.\n")

predictions = model.predict(X_test)
capture_feedback(predictions, y_test, threshold=0.2)
