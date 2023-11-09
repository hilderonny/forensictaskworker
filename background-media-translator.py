import time
import os
import json
import datetime
import shutil
import stat

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--inputpath', '-i', type=str, action='store', required=True, help='Directory where the images to process are obtained from. Must be writable.')
parser.add_argument('--processingpath', '-p', type=str, action='store', required=True, help='Directory where the currently processed image gets stored. Must be writable.')
parser.add_argument('--outputpath', '-o', type=str, action='store', required=True, help='Directory where the output JSON files will be stored. Must be writable.')
parser.add_argument('--whisperpath', '-w', type=str, action='store', required=True, help='Directory where the Faster-Whisper models are stored.')
parser.add_argument('--argospath', '-a', type=str, action='store', required=True, help='Directory where the Argos Translate models are stored.')
parser.add_argument('--whispermodel', '-m', type=str, default='small', action='store', help='Whisper model size to use. Can be "tiny", "base", "small" (default), "medium" or "large-v2".')
args = parser.parse_args()

# Check write access to directories
import sys
import os
INPUTPATH = args.inputpath
PROCESSINGPATH = args.processingpath
OUTPUTPATH = args.outputpath
if not os.access(INPUTPATH, os.R_OK | os.W_OK):
    sys.exit(f'ERROR: Cannot read and write input directory {INPUTPATH}')
if not os.access(PROCESSINGPATH, os.R_OK | os.W_OK):
    sys.exit(f'ERROR: Cannot read and write processing directory {PROCESSINGPATH}')
if not os.access(OUTPUTPATH, os.R_OK | os.W_OK):
    sys.exit(f'ERROR: Cannot read and write output directory {OUTPUTPATH}')

# Check existence of Whisper files
WHISPERPATH = args.whisperpath
WHISPERTINYMODELPATH = os.path.join(WHISPERPATH, 'models--guillaumekln--faster-whisper-tiny')
WHISPERBASEMODELPATH = os.path.join(WHISPERPATH, 'models--guillaumekln--faster-whisper-base')
WHISPERSMALLMODELPATH = os.path.join(WHISPERPATH, 'models--guillaumekln--faster-whisper-small')
WHISPERMEDIUMMODELPATH = os.path.join(WHISPERPATH, 'models--guillaumekln--faster-whisper-medium')
WHISPERLARGEV2MODELPATH = os.path.join(WHISPERPATH, 'models--guillaumekln--faster-whisper-large-v2')
if not os.access(WHISPERPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper directory {WHISPERPATH}')
if not os.access(WHISPERTINYMODELPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper tiny model directory {WHISPERTINYMODELPATH}')
if not os.access(WHISPERBASEMODELPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper base model directory {WHISPERBASEMODELPATH}')
if not os.access(WHISPERSMALLMODELPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper small model directory {WHISPERSMALLMODELPATH}')
if not os.access(WHISPERMEDIUMMODELPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper medium model directory {WHISPERMEDIUMMODELPATH}')
if not os.access(WHISPERLARGEV2MODELPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Whisper large V2 model directory {WHISPERLARGEV2MODELPATH}')

# Check existence of Argos Translate files
ARGOSPATH = args.argospath
ARGOSENDEPACKAGEPATH = os.path.join(ARGOSPATH, 'packages/en_de')
if not os.access(ARGOSPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos Translate directory {ARGOSPATH}')
if not os.access(ARGOSENDEPACKAGEPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos Translate EN->DE model directory {ARGOSENDEPACKAGEPATH}')

# Load Faster Whisper
print('Loading Faster Whisper')
from faster_whisper import WhisperModel    
compute_type = 'int8'
whisper_model = WhisperModel( model_size_or_path = args.whispermodel, device = 'cpu', local_files_only = False, compute_type = compute_type, download_root = args.whisperpath )

# Load Argos translate
print('Loading Argos Translate')
os.environ["ARGOS_PACKAGES_DIR"] = os.path.join(args.argospath, "packages")
os.environ["ARGOS_DEVICE_TYPE"] = 'cpu'
global argos_translation
import argostranslate.translate
argos_translation = argostranslate.translate.get_translation_from_codes('en', 'de')

def translate_into_german(segments_en):
    translation_segments_de = list(map(lambda segment: { 'start': segment['start'], 'end': segment['end'], 'text': argos_translation.translate(segment['text']) }, segments_en))
    return translation_segments_de

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
        if original_language == 'de': # Deutsch brauchen wir weder uebersetzen noch in Englisch
            result['en'] = None
            result['de'] = result['original']
        elif original_language == 'en': # Englisch muss nicht ins Englische uebersetzt werden
            result['en'] = result['original']
            print('Translating into german')
            segments_de = translate_into_german(result['en']['segments'])
            result['de'] = { 'segments': segments_de, 'fulltext':  ' '.join(map(lambda segment: segment['text'], segments_de)) }
        else:
            print('Translating into english')
            translation_segments_generator_en, _ = whisper_model.transcribe(file_path, task = 'translate')
            translation_segments_en = list(map(lambda segment: { 'start': segment.start, 'end': segment.end, 'text': segment.text }, translation_segments_generator_en))
            result['en'] = { 'segments':  translation_segments_en, 'fulltext':  ''.join(map(lambda segment: segment['text'], translation_segments_en)) }
            print('Translating into german')
            segments_de = translate_into_german(result['en']['segments'])
            result['de'] = { 'segments': segments_de, 'fulltext':  ' '.join(map(lambda segment: segment['text'], segments_de)) }
    except Exception as ex:
        print(ex)
        result['exception'] = str(ex)
    finally:
        print('Deleting file ' + file_path)
        os.remove(file_path)
        pass
    end_time = datetime.datetime.now()
    result['duration'] = (end_time - start_time).total_seconds()
    return result

def check_and_process_files():
    file_was_processed = False
    for file_name in os.listdir(INPUTPATH):
        input_file_path = os.path.join(INPUTPATH, file_name)
        if os.path.isfile(input_file_path):
            try:
                # Erst mal Datei aus INPUT Verzeichnis bewegen, damit andere Prozesse diese nicht ebenfalls verarbeiten
                processing_file_path = os.path.join(PROCESSINGPATH, file_name)
                shutil.move(input_file_path, processing_file_path)
                os.chmod(processing_file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO ) # Let the background process delete the file afterwards
                # Datei verarbeiten
                result = process_file(processing_file_path)
                json_result = json.dumps(result, indent=2)
                output_file_path = os.path.join(OUTPUTPATH, file_name + '.json')
                print('Writing output file ' + output_file_path)
                output_file = os.open(output_file_path, os.O_RDWR|os.O_CREAT)
                os.write(output_file, str.encode(json_result))
                os.close(output_file)
                print(json_result)
                file_was_processed = True
                return file_was_processed # Let the program wait a moment and recheck the uplopad directory
            except Exception as ex:
                print(ex)
            finally: # Hat nicht geklappt. Eventuell hat ein anderer Prozess die Datei bereits weg geschnappt. Egal.
                return
    return file_was_processed

try:
    print('Ready and waiting for action')
    while True:
        file_was_processed = check_and_process_files()
        if file_was_processed == False:
            time.sleep(3)
finally:
    pass
