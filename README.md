# forensictaskworker

Several workers for https://github.com/hilderonny/forensictaskbridge.

|File|Description|
|---|---|
|`mediatranscriber.py`|Transcribe audio and video files using Faster Whisper|
|`texttranslator.py`|Translates text between several languages using Argos Translate|

## Example

```sh
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath D:\\data\\audio\\input --whisperpath D:\\data\\whisper --whispermodel tiny --usegpu
```

## Installation

Install Python 3.11.7 (NOT 3.12 - it causes a problem with faster-whisper installation) from https://www.python.org/downloads/release/python-3117/.
The best is to download the portable version into a `python` subdirectory and also download https://bootstrap.pypa.io/get-pip.py.

Next insert the following lines into the file `python/python311._pth`

```
Scripts
Lib\site-packages
```

and run the following commands from the repository directory

```
python/python get-pip.py
python/python -m pip install -r requirements.txt
```

Copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` into the directory `python/Lib/site-packages/ctranslate2`.

## Media transcription

If a whisper model ist not installed, then the program tries to install it at the first use. So make sure to have an internet connection the first time you try to use a model.

```
python/python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/input --whisperpath /faster-whisper --usegpu --whispermodel large-v2
```

## Media translation

For the first use you need to download ind install all available translation packes via

```
python/pythonpython argosupdate.py --argospath /argos-translate  
```

```
python/pythonpython texttranslator.py --apiurl http://127.0.0.1:5000/api/ --argospath /argos-translate --sourcelanguage en --targetlanguage de --usegpu
```