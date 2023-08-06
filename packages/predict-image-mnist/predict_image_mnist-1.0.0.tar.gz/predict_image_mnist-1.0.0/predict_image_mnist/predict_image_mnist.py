import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

def predictImage(model_path,img_path):
    model = load_model(model_path)
    img = cv2.imread(img_path) ## read the image
    g = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) ## convert the image color to gray
    r_img = cv2.resize(g,(28,28),interpolation = cv2.INTER_AREA) ## resize the image
    n_img = tf.keras.utils.normalize(r_img,axis =1 ) ## normalize the new resized image matrix
    n_img = np.array(n_img).reshape(-1,28,28,1) ##reshape the array dimensions
    pr = model.predict(n_img) ## predict the image
    return np.argmax(pr) ## return the prediction