# forensictaskworker

Several workers for https://github.com/hilderonny/forensictaskbridge.

## Example

```sh
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath D:\\data\\audio\\input --whisperpath D:\\data\\whisper --whispermodel tiny --usegpu
```

## Installation

Install Python 3.11.7 (NOT 3.12 - it causes a problem with faster-whisper installation) from https://www.python.org/downloads/release/python-3117/.

Copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` into the directory `venv/Lib/site-packages/ctranslate2`.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Media transcription

If a whisper model ist not installed, then the program tries to install it at the first use. So make sure to have an internet connection the first time you try to use a model.

```
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/audio/input --whisperpath /data/faster-whisper --usegpu --whispermodel large-v2
```

## Media translation

For the first use you need to download ind install all available translation packes via

```
python argosupdate.py --argospath /data/argos-translate  
```

```
python texttranslator.py --apiurl http://127.0.0.1:5000/api/ --argospath /data/argos-translate --sourcelanguage en --targetlanguage de --usegpu
```