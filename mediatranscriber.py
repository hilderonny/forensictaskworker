PROGRAM_VERSION = '1.0.0'

print(f'Media Transcriber Version {PROGRAM_VERSION}')

import time
import os
import json
import datetime
import requests

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--apiurl', type=str, action='store', required=True, help='Root URL of the API of the forensic task bridge to use, e.g. https://hilderonny.github.io/forensictaskbridge/api/')
parser.add_argument('--sharepath', type=str, action='store', required=True, help='Directory path where the media files to process are accessible.')
parser.add_argument('--whisperpath', type=str, action='store', required=True, help='Directory where the Faster-Whisper models are stored.')
parser.add_argument('--whispermodel', type=str, default='small', action='store', help='Whisper model size to use. Can be "tiny", "base", "small" (default), "medium", "large-v2" or "large-v3".')
parser.add_argument('--usegpu', action='store_true', help='Use GPU for neural network calculations. Needs to have cuBLAS and cuDNN installed from https://github.com/Purfview/whisper-standalone-win/releases/tag/libs')
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

# Check existence of Whisper files
WHISPERPATH = args.whisperpath
if not os.access(WHISPERPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper path {WHISPERPATH}')
print(f'Using whisper path {WHISPERPATH}')

WHISPERMODEL = args.whispermodel
print(f'Using whisper model {WHISPERMODEL}')
USEGPU = args.usegpu
print(f'Using {"GPU" if USEGPU else "CPU"}')

# Load Faster Whisper
print('Loading Faster Whisper')
from faster_whisper import WhisperModel    
compute_type = 'float16' if USEGPU else 'int8'
device = 'cuda' if USEGPU else 'cpu'
whisper_model = WhisperModel( model_size_or_path = WHISPERMODEL, device = device, local_files_only = False, compute_type = compute_type, download_root = WHISPERPATH )

def process_file(file_path):
    start_time = datetime.datetime.now()
    result = {}
    try:
        print('Processing file ' + file_path)
        print('Transcribing')
        transcribe_segments_generator, transcribe_info = whisper_model.transcribe(file_path, task = 'transcribe')
        transcribe_segments = list(map(lambda segment: { 'start': segment.start, 'end': segment.end, 'text': segment.text }, transcribe_segments_generator))
        original_language = transcribe_info.language
        result['language'] = original_language
        result['original'] = { 'segments': transcribe_segments, 'fulltext':  ' '.join(map(lambda segment: segment['text'], transcribe_segments)) }
        if original_language == 'en': # Englisch muss nicht ins Englische uebersetzt werden
            result['en'] = result['original']
        else:
            print('Translating into english')
            translation_segments_generator_en, _ = whisper_model.transcribe(file_path, task = 'translate')
            translation_segments_en = list(map(lambda segment: { 'start': segment.start, 'end': segment.end, 'text': segment.text }, translation_segments_generator_en))
            result['en'] = { 'segments':  translation_segments_en, 'fulltext':  ''.join(map(lambda segment: segment['text'], translation_segments_en)) }
    except Exception as ex:
        print(ex)
        result['error'] = str(ex)
    end_time = datetime.datetime.now()
    result['duration'] = (end_time - start_time).total_seconds()
    return result

def check_and_process_files():

    req = requests.get(f"{APIURL}tasks/transcribe/take/{WHISPERMODEL}/")
    if req.status_code == 400:
        error = req.json()["error"]
        print(error)
        return False
    elif not req.status_code == 200:
        return False
    data = req.json()
    print(data)
    processing_file_path = os.path.join(SHAREPATH, data["filename"])
    result = process_file(processing_file_path)
    if "error" in result:
        print(result["error"])
        return False
    result_to_report = {}
    result_to_report["language"] = result["language"]
    result_to_report["originaltext"] = result["original"]["fulltext"]
    result_to_report["englishtext"] = result["en"]["fulltext"]
    result_to_report["duration"] = result["duration"]
    if (result["error"]):
        result_to_report["error"] = result["error"]
    print(json.dumps(result_to_report, indent=2))
    print('Reporting result')
    requests.post(f"{APIURL}tasks/transcribe/reportcompletion/{data['id']}/", json=result_to_report)
    return True

try:
    print('Ready and waiting for action')
    while True:
        file_was_processed = False
        try:
            file_was_processed = check_and_process_files()
        except Exception:
            pass
        if file_was_processed == False:
            time.sleep(3)
except Exception:
    pass
