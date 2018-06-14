#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os
import subprocess
import uuid
import requests
import json


def speech_recognition(speech_file, api_key, lang_code='en-US', encoding='FLAC'):
    encoding_types = ["ENCODING_UNSPECIFIED",
                      "LINEAR16",
                      "FLAC",
                      "MULAW",
                      "AMR",
                      "AMR_WB",
                      "OGG_OPUS",
                      "SPEEX_WITH_HEADER_BYTE"]
    if encoding not in encoding_types:
        raise Exception('Wrong encoding. It should be in list [%s]' % ', '.join(encoding_types))
    endpoint = 'https://speech.googleapis.com/v1/speech:recognize?key=%s' % api_key
    headers = {'content-type': 'application/json',
               'X-Mashape-Key': api_key}
    with open(speech_file, 'rb') as f:
        speech_content = base64.b64encode(f.read())
    data = {
        'config': {
            'languageCode': lang_code,
            'encoding': encoding,
            'sampleRateHertz': '44100'
        },
        'audio': {
            'content': speech_content.decode('utf-8')
        }
    }
    r = requests.post(endpoint, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    response = json.loads(r.text)
    texts = []
    for res in response['results']:
        alternatives = res['alternatives']
        text_dict = max(alternatives, key=lambda k: k['confidence'])
        texts.append(text_dict['transcript'])
    return texts


def audio_to_flac(src, tmp_folder='/tmp'):
    tmp_file = '%s.flac' % str(uuid.uuid4())[:8]
    tmp = os.path.join(tmp_folder, tmp_file)
    FNULL = open(os.devnull, 'w')
    subprocess.call(['ffmpeg', '-i', src, '-ac', '1', '-af', 'aformat=s16:44100', tmp, '-y'], stdout=FNULL,stderr=subprocess.STDOUT)
    return tmp
