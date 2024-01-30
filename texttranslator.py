PROGRAM_VERSION = '1.0.0'

print(f'Text Translator Version {PROGRAM_VERSION}')

import time
import os
import json
import requests

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--apiurl', type=str, action='store', required=True, help='Root URL of the API of the forensic task bridge to use, e.g. https://hilderonny.github.io/forensictaskbridge/api/')
parser.add_argument('--argospath', type=str, action='store', required=True, help='Directory where the Argos Translate models are stored.')
parser.add_argument('--usegpu', action='store_true', help='Use GPU for neural network calculations. Needs to have cuBLAS and cuDNN installed from https://github.com/Purfview/whisper-standalone-win/releases/tag/libs')
parser.add_argument('--version', '-v', action='version', version=PROGRAM_VERSION)
args = parser.parse_args()

# Check write access to directories
import sys
import os
APIURL = args.apiurl
if not APIURL.endswith("/"):
    APIURL = f"{APIURL}/"
print(f'Using API URL {APIURL}')

# Check existence of Argos Translate files
ARGOSPATH = args.argospath
ARGOSENDEPACKAGEPATH = os.path.join(ARGOSPATH, "packages")
if not os.access(ARGOSPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos Translate directory {ARGOSPATH}')
if not os.access(ARGOSENDEPACKAGEPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos Translate package directory {ARGOSENDEPACKAGEPATH}')
print(f'Using argos translate path {ARGOSPATH}')

USEGPU = args.usegpu
print(f'Using {"GPU" if USEGPU else "CPU"}')

# Load Argos translate
print('Loading Argos Translate')
os.environ['ARGOS_PACKAGES_DIR'] = ARGOSENDEPACKAGEPATH
device = 'cuda' if USEGPU else 'cpu'
os.environ['ARGOS_DEVICE_TYPE'] = device
global argos_translation
import argostranslate.translate
import argostranslate.package

def check_and_process():
    req = requests.get(f"{APIURL}tasks/translate/take/")
    if req.status_code == 400:
        error = req.json()["error"]
        print(error)
        return False
    elif not req.status_code == 200:
        return False
    data = req.json()
    print(data)
    sourcelanguage = data["sourcelanguage"]
    targetlanguage = data["targetlanguage"]
    texttotranslate = data["text"]
    result_to_report = {}
    from_lang = argostranslate.translate.get_language_from_code(sourcelanguage)
    to_lang = argostranslate.translate.get_language_from_code(targetlanguage)
    if from_lang is None:
        print(f"Language {sourcelanguage} is not installed. Please install it using argosupdate.py!")
        result_to_report["error"] = f"Language {sourcelanguage} is not supported"
    elif to_lang is None:
        print(f"Language {targetlanguage} is not installed. Please install it using argosupdate.py!")
        result_to_report["error"] = f"Language {targetlanguage} is not supported"
    else:
        argos_translation = from_lang.get_translation(to_lang)
        translatedtext = argos_translation.translate(texttotranslate)
        result_to_report["translatedtext"] = translatedtext
    print(json.dumps(result_to_report, indent=2))
    print('Reporting result')
    requests.post(f"{APIURL}tasks/translate/reportcompletion/{data['id']}/", json=result_to_report)
    return True

try:
    print('Ready and waiting for action')
    while True:
        text_was_processed = False
        try:
            text_was_processed = check_and_process()
        except Exception:
            pass
        if text_was_processed == False:
            time.sleep(3)
except Exception:
    pass
