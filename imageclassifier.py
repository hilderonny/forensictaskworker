PROGRAM_VERSION = '1.0.0'

print(f'Image classifier Version {PROGRAM_VERSION}')

import datetime
import json
import time
import numpy
import requests

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--apiurl', type=str, action='store', required=True, help='Root URL of the API of the forensic task bridge to use, e.g. https://hilderonny.github.io/forensictaskbridge/api/')
parser.add_argument('--sharepath', type=str, action='store', required=True, help='Directory path where the image files to process are accessible.')
parser.add_argument('--mobilenetpath', type=str, action='store', required=True, help='Directory where the MobileNetV3 Model and settings are stored.')
parser.add_argument('--targetlanguage', type=str, default='en', action='store', help='Language of the output tags. Can be "en" (default) or "de".')
parser.add_argument('--version', '-v', action='version', version=PROGRAM_VERSION)
args = parser.parse_args()

# Check access to directories
import sys
import os
APIURL = args.apiurl
if not APIURL.endswith("/"):
    APIURL = f"{APIURL}/"
print(f'Using API URL {APIURL}')
SHAREPATH = args.sharepath
if not os.access(SHAREPATH, os.R_OK | os.W_OK):
    sys.exit(f'ERROR: Cannot read share path {SHAREPATH}')
print(f'Using share path {SHAREPATH}')
MOBILENETPATH = args.mobilenetpath
TARGETLANGUAGE = args.targetlanguage
#LABELFILEPATH = os.path.join(MOBILENETPATH, f'imagenet.{TARGETLANGUAGE}.names')
KERASPATH = os.path.join(MOBILENETPATH, 'keras')
MODELFILEPATH = os.path.join(MOBILENETPATH, 'mobilenetv3large_model.keras')
if not os.access(MOBILENETPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read MobileNet directory {MOBILENETPATH}')
#if not os.access(LABELFILEPATH, os.R_OK):
#    sys.exit(f'ERROR: Cannot read MobileNet label file {LABELFILEPATH}')
if not os.access(KERASPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Keras directory {KERASPATH}')
if not os.access(MODELFILEPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read MobileNet model file {MODELFILEPATH}')
print(f'Using MobileNat path {MOBILENETPATH}')

# Load classification labels
#print(f'Loading labels for language {TARGETLANGUAGE}')
#CLASSES = {}
#with open(LABELFILEPATH, mode='r', encoding='utf-8') as f:
#    for line in f.readlines():
#        stripped_line = line.strip()
#        id, text = stripped_line[:9], stripped_line[10:]
#        CLASSES[id] = text

# Import TensorFlow and MobileNet
print('Loading TensorFlow and MobileNet V3')
os.environ['KERAS_HOME'] = os.path.join(KERASPATH)
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input, decode_predictions

# Load MobileNet model
print('Loading model')
MODEL = load_model(MODELFILEPATH, compile=False)

def process_file(file_path):
    start_time = datetime.datetime.now()
    result = {}
    try:
        img = image.load_img(file_path, target_size=(224, 224))
        imageArray = image.img_to_array(img)
        expandedImageArray = numpy.expand_dims(imageArray, axis=0)
        preprocessedImage = preprocess_input(expandedImageArray)
        predictions = MODEL.predict(preprocessedImage)
        best_predictions = decode_predictions(predictions, top=10)[0]
        first_prediction = best_predictions[0]
        result["predictions"] = [prediction[1] for prediction in best_predictions]
        result["class"] = first_prediction[0]
        #result["name"] = CLASSES[first_prediction[0]]
        result["probability"] = float(first_prediction[2])
    except Exception as ex:
        print(ex)
        result["error"] = str(ex)
    end_time = datetime.datetime.now()
    result["duration"] = (end_time - start_time).total_seconds()
    return result

def check_and_process_files():

    req = requests.get(f"{APIURL}tasks/classifyimage/take/")
    if req.status_code == 400:
        error = req.json()["error"]
        print(error)
        return False
    elif not req.status_code == 200:
        return False
    data = req.json()
    print(data)
    processing_file_path = os.path.join(SHAREPATH, data["filename"])
    result_to_report = process_file(processing_file_path)
    print(json.dumps(result_to_report, indent=2))
    print('Reporting result')
    requests.post(f"{APIURL}tasks/classifyimage/reportcompletion/{data['id']}/", json=result_to_report)
    return True


print('Ready and waiting for action')
while True:
    file_was_processed = False
    try:
        file_was_processed = check_and_process_files()
    except Exception:
        pass
    if file_was_processed == False:
        time.sleep(3)
