import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array, load_img
import numpy as np


def detect(path):
    # Load the trained model from the .h5 file
    model = load_model('../model.h5', compile=False)

    # Load the image
    img_path = path

    img = load_img(img_path, target_size=(224, 224))

    # Preprocess the image
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.inception_resnet_v2.preprocess_input(x)

    # Get the model's prediction for the image
    pred = model.predict(x, verbose=1)
    # print(pred)
    y_pred = np.argmax(pred, axis=1)
    class_labels = ['autistic', 'non_autistic']
    class_name = class_labels[int(y_pred)]

    print('The predicted class is:', class_name)
    return class_name
