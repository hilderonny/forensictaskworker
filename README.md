# mediatranscriber

Audio transcription worker for https://github.com/hilderonny/forensictaskbridge.

## Example

```sh
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath D:\\data\\audio\\input --whisperpath D:\\data\\whisper --whispermodel tiny --usegpu
```

## Installation

Install Python 3.11 (NOT 3.12 - it causes a problem with faster-whisper installation) from https://www.python.org/downloads/release/python-3117/.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` into the directory `venv/Lib/site-packages/ctranslate2`.

```
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/audio/input --whisperpath /data/faster-whisper --usegpu --whispermodel large-v2
```