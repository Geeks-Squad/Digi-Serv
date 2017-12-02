from keras.models import load_model
import cv2
import numpy as np
from keras import backend as K


def cnn_predict(path):
    img_width = 150
    img_height = 150
    if K.image_data_format() == 'channels_first':
        input_shape = (1, 3, img_width, img_height)
    else:
        input_shape = (1, img_width, img_height, 3)

    # Processing input image
    file = cv2.imread(path)
    file = cv2.resize(file, (img_height, img_height))
    file = np.array(file).reshape(input_shape)

    # Predicting the input image
    model = load_model('savepoint.h5')
    yFit = model.predict(file, batch_size=1)
    return yFit
