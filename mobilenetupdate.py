import time
import os
import json
import datetime
import requests

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mobilenetpath', type=str, action='store', required=True, help='Directory where the MobileNetV3 Model and settings are stored.')
args = parser.parse_args()

# Check write access to directories
import sys
import os

# Check existence of Argos Translate files
MOBILENETPATH = args.mobilenetpath
KERASPATH = os.path.join(MOBILENETPATH, 'keras')
MODELFILEPATH = os.path.join(MOBILENETPATH, 'mobilenetv3large_model.keras')
if not os.access(MOBILENETPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read MobileNet directory {MOBILENETPATH}')
print(f'Using MobileNet path {MOBILENETPATH}')

print('Updating MobileNet')
os.environ['KERAS_HOME'] = KERASPATH

import tensorflow.keras.applications as applications
model = applications.MobileNetV3Large(weights='imagenet', include_top=True)
model.save(MODELFILEPATH)
