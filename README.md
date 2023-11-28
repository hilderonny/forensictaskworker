# background-media-translator

Background worker for transcribing and translating media files dropped in a folder.

Be aware that using this worker with GPU you need an NVidia graphics card with at leaset 6GB of RAM.

## Setup

1. Install Python 3.11 from https://www.python.org/downloads/windows/
1. Clone the repository
1. Open Terminal in the root folder of the repository and run `pip install -r .\requirements.txt`
1. For GPU usage, download https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_win_v3.7z and extract following files into the path where the CTranslate2 python package is located (e.g. **C:\Users\DEFAULT\AppData\Roaming\Python\Python311\site-packages\ctranslate2**)
    - cudnn_ops_infer64_8.dll
    - cublas64_11.dll
    - cublasLt64_11.dll
    - cudnn_cnn_infer64_8.dll
    - zlibwapi.dll

## Usage

```
python background-media-translator.py [-h] --inputpath INPUTPATH --processingpath PROCESSINGPATH --outputpath OUTPUTPATH --whisperpath WHISPERPATH --argospath ARGOSPATH [--whispermodel WHISPERMODEL] [--usegpu] [--version]
```

### Options
- `-h`, `--help`: show this help message and exit
- `--inputpath INPUTPATH`, `-i INPUTPATH`: Directory where the images to process are obtained from. Must be writable.
- `--processingpath PROCESSINGPATH`, `-p PROCESSINGPATH`: Directory where the currently processed image gets stored. Must be writable.
- `--outputpath OUTPUTPATH`, `-o OUTPUTPATH`: Directory where the output JSON files will be stored. Must be writable.
- `--whisperpath WHISPERPATH`, `-w WHISPERPATH`: Directory where the Faster-Whisper models are stored.
- `--argospath ARGOSPATH`, `-a ARGOSPATH`: Directory where the Argos Translate models are stored.
- `--whispermodel WHISPERMODEL`, `-m WHISPERMODEL`: Whisper model size to use. Can be "tiny", "base", "small" (default), "medium" or "large-v2".
- `--usegpu`, `g`: Use GPU for neural network calculations. Needs to have cuBLAS and cuDNN installed from https://github.com/Purfview/whisper-standalone-win/releases/tag/libs
- `--version`, `-v`: show program's version number and exit

## Example

```
python background-media-translator.py -i ./data/input -p ./data/processing -o ./data/output -w ./faster-whisper -a ./argos-translate -m large-v2
```