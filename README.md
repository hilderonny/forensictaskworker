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
Lib/site-packages
```

and run the following commands from the repository directory

```
python/python get-pip.py
python/python -m pip install -r requirements.txt
```

To have GPU support you need to copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` (Can be found at https://developer.nvidia.com/cudnn) into the directory `python/Lib/site-packages/ctranslate2`.

## Installation for Linux as services

```
sudo apt install -y git python3.11-env ocl-icd-libopencl1 nvidia-cuda-toolkit nvidia-utils-510-server nvidia-utils-535-server
git clone https://github.com/hilderonny/forensictaskworker.git
cd forensictaskworker
python3.11 -m venv python-venv
source python-venv/bin/activate
pip install -r requirements.txt
```

A restart may be required. Setup an internet connection and download the required ANN models.

```
 ./python-venv/bin/python ./argosupdate.py --argospath /argos-translate/
 ./python-venv/bin/python ./mobilenetupdate.py --mobilenetpath /mobilenet/
```

Create shell scripts for the several workers with the following contents.

**imageclassifier.sh**:

```
#!/bin/sh

./python-venv/bin/python ./imageclassifier.py --apiurl http://127.0.0.1:30000/api/ --sharepath /data/input --mobilenetpath /mobilenet
```

**mediatranscriber.sh**:

```
#!/bin/sh

export LD_LIBRARY_PATH=`./python-venv/bin/python -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'`
export CUDA_VISIBLE_DEVICES=0

./python-venv/bin/python ./mediatranscriber.py --apiurl http://127.0.0.1:30000/api/ --sharepath /data/input --whisperpath /faster-whisper --usegpu --whispermodel large-v2
```

**texttranslator.sh**:

```
#!/bin/sh

export LD_LIBRARY_PATH=`./python-venv/bin/python -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'`
export CUDA_VISIBLE_DEVICES=0

./python-venv/bin/python ./texttranslator.py --apiurl http://127.0.0.1:30000/api/ --argospath /argos-translate --usegpu
```

Next create Systemd service files.

**/etc/systemd/system/forensictaskworker_imageclassifier.service**:

```
[Unit]
Description=Forensic Task Worker - Image Classifier

[Service]
ExecStart=/forensictaskworker/imageclassifier.sh
Restart=always
User=user
WorkingDirectory=/forensictaskworker/

[Install]
WantedBy=multi-user.target
```

**/etc/systemd/system/forensictaskworker_mediatranscriber.service**:

```
[Unit]
Description=Forensic Task Worker - Media Transcriber

[Service]
ExecStart=/forensictaskworker/mediatranscriber.sh
Restart=always
User=user
WorkingDirectory=/forensictaskworker/

[Install]
WantedBy=multi-user.target
```

**/etc/systemd/system/forensictaskworker_texttranslator.service**:

```
[Unit]
Description=Forensic Task Worker - Text Translator

[Service]
ExecStart=/forensictaskworker/texttranslator.sh
Restart=always
User=user
WorkingDirectory=/forensictaskworker/

[Install]
WantedBy=multi-user.target
```

You can now test the workers by running their shell scripts. This is highly recommended because `imageclassifier` and `mediatranscriber` download additional files at the first work. So make sure tio have an internet connection at this time.

Finally register and start the services.

```
chmod +x ./*.sh

sudo systemctl daemon-reload

sudo systemctl enable forensictaskworker_imageclassifier.service
sudo systemctl enable forensictaskworker_mediatranscriber.service
sudo systemctl enable forensictaskworker_texttranslator.service

sudo systemctl start forensictaskworker_imageclassifier.service
sudo systemctl start forensictaskworker_mediatranscriber.service
sudo systemctl start forensictaskworker_texttranslator.service
```

## Image classification

Before the first use the MobileNet models must be downloaded. Make sure you have an internet connection and run the following script.

```
python\python mobilenetupdate.py --mobilenetpath /mobilenet
```

Next you can run the worker with this command. On first run the worker downloads a file needed for class identification from https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json so make sure you have an internet connection.

```
python/python imageclassifier.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/input --mobilenetpath /mobilenet
```

## Media transcription

If a whisper model ist not installed, then the program tries to install it at the first use. So make sure to have an internet connection the first time you try to use a model and you created a directory where the faster-whisper models can be stored. 

```
python/python mediatranscriber.py --apiurl http://127.0.0.1:5000/api/ --sharepath /data/input --whisperpath /faster-whisper --usegpu --whispermodel large-v2
```

## Text translation

For the first use you need to download ind install all available translation packes via the followinf command. Make sure that the `argospath` directory exists.

```
python/python argosupdate.py --argospath /argos-translate  
```

The worker can be run this way.

```
python/python texttranslator.py --apiurl http://127.0.0.1:5000/api/ --argospath /argos-translate --usegpu
```
