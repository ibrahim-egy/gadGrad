import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array, load_img
import numpy as np

model = load_model('../model.h5', compile=False)


def detect(path):
    img_path = path

    img = load_img(img_path, target_size=(224, 224))
    print(img.size)
    # Preprocess the image
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.inception_resnet_v2.preprocess_input(x)

    # Get the model's prediction for the image
    pred = model.predict(x, verbose=1)
    y_pred = np.argmax(pred, axis=1)
    class_labels = ['Autistic', 'Non Autistic']
    class_name = class_labels[int(y_pred)]

    return class_name
