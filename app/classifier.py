import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import ImageFile, Image
try:
    import ImageFile, Image
except:
    from PIL import ImageFile, Image
from numpy import expand_dims
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50
from app.classes import classes
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import requests
import shutil # save img locally
import cv2
import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("models/fine_tune_model_best.hdf5")
file_name = 'images/food-image.jpg'

def deleteImage():
    os.remove(file_name)

def downloadImage(image_url):
    res = requests.get(image_url, stream = True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

def getPrediction(img_bytes, model):
    # Loads the image and transforms it to (224, 224, 3) shape
    original_image = Image.open(img_bytes)
    original_image = original_image.convert('RGB')
    original_image = original_image.resize((224, 224), Image.NEAREST)
    
    numpy_image = image.img_to_array(original_image)
    image_batch = expand_dims(numpy_image, axis=0)

    processed_image = preprocess_input(image_batch, mode='caffe')
    preds = model.predict(processed_image)
    
    return preds

def classifyImage(image_url):
    downloadImage(image_url)
    prediction = getPrediction(file_name, model)
    indices = np.argsort(prediction[0])[-5:][::-1]
    result = []
    for index in indices:
        pred = {
            'slug': classes[index]
        }
        result.append(pred)
    deleteImage()
    return result