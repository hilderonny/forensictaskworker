@ECHO OFF
git pull
python\python mediatranscriber.py --apiurl http://192.168.0.152:30000/api/ --whisperpath \faster-whisper --whispermodel large-v2 --usegpu --sharepath X:\data\forensictaskbridge\input