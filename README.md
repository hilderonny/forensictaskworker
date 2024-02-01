# forensictaskworker

Several workers for https://github.com/hilderonny/forensictaskbridge.

|File|Description|
|---|---|
|`imageclassifier.py`|Classify images into 70 different tags via MobileNet Keras|
|`mediatranscriber.py`|Transcribe audio and video files using Faster Whisper|
|`texttranslator.py`|Translates text between several languages using Argos Translate|

## Example

```sh
python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath D:\\data\\audio\\input --whisperpath D:\\data\\whisper --whispermodel tiny --usegpu
```

## Installation for Windows

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

To have GPU support you need to copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` (Can be found at https://developer.nvidia.com/cudnn) into the directory `python/Lib/site-packages/ctranslate2`.

## Installation for Linux as services



## Image classification

Before the first use the MobileNet models must be downloaded. Make sure you have an internet connection and run the following script.

```
python\python mobilenetupdate.py --mobilenetpath /mobilenet
```

Next you can run the worker with this command.

```
python\python imageclassifier.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/input --mobilenetpath /mobilenet --targetlanguage de
```

## Media transcription

If a whisper model ist not installed, then the program tries to install it at the first use. So make sure to have an internet connection the first time you try to use a model and you created a directory where the faster-whisper models can be stored. 

```
python/python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/input --whisperpath /faster-whisper --usegpu --whispermodel large-v2
```

## Text translation

For the first use you need to download ind install all available translation packes via the followinf command. Make sure that the `argospath` directory exists.

```
python/pythonpython argosupdate.py --argospath /argos-translate  
```

The worker can be run this way.

```
python/pythonpython texttranslator.py --apiurl http://127.0.0.1:5000/api/ --argospath /argos-translate --sourcelanguage en --targetlanguage de --usegpu
```