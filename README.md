# background-media-translator

Background worker for transcribing and translating media files dropped in a folder. 

## Setup

1. Install Python 3.11 from https://www.python.org/downloads/windows/
1. Clone the repository
1. Open Terminal in the root folder of the repository and run `pip install -r .\requirements.txt`

## Usage

```
python background-media-translator.py [-h] --inputpath INPUTPATH --processingpath PROCESSINGPATH --outputpath OUTPUTPATH --whisperpath WHISPERPATH --argospath ARGOSPATH  [--whispermodel WHISPERMODEL] [--version]
```

### Options
- `-h`, `--help`: show this help message and exit
- `--inputpath INPUTPATH`, `-i INPUTPATH`: Directory where the images to process are obtained from. Must be writable.
- `--processingpath PROCESSINGPATH`, `-p PROCESSINGPATH`: Directory where the currently processed image gets stored. Must be writable.
- `--outputpath OUTPUTPATH`, `-o OUTPUTPATH`: Directory where the output JSON files will be stored. Must be writable.
- `--whisperpath WHISPERPATH`, `-w WHISPERPATH`: Directory where the Faster-Whisper models are stored.
- `--argospath ARGOSPATH`, `-a ARGOSPATH`: Directory where the Argos Translate models are stored.
- `--whispermodel WHISPERMODEL`, `-m WHISPERMODEL`: Whisper model size to use. Can be "tiny", "base", "small" (default), "medium" or "large-v2".
- `--version`, `-v`: show program's version number and exit

## Example

```
python background-media-translator.py -i ./data/input -p ./data/processing -o ./data/output -w ./faster-whisper -a ./argos-translate -m large-v2
```