import json
import os
import requests
from flask import jsonify, render_template
from dotenv import load_dotenv
from app.sentiment import sentiment


load_dotenv('.env')


@sentiment.route('/')
@sentiment.route('/analyzesentiment')
def index():
    """Returns the applications index page."""
    return render_template('index.html')


@sentiment.route('/getSentiment/<text>')
def getSentiment(text):
    api_url = 'http://text-processing.com/api/sentiment/'
    r = requests.post(api_url, data={'text': text})
    return jsonify(r.json())


@sentiment.route('/getLanguage/<text>')
def getLanguage(text):
    api_key = os.getenv("API_KEY_LANG")
    endpoint = 'https://ws.detectlanguage.com/0.2/detect'
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer %s' % api_key
        }
    data = {'q': text}
    r = requests.post(endpoint, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        return jsonify({"error": "Something went wrong with the API"})
    return jsonify(r.json()['data'])


@sentiment.route('/getJargon/<text>')
def getJargon(text):
    bugreportwords = ['wrong', 'incorrect', 'not showing', 'slow', 'cannot', 'error', 'not updating', 'challenge', 
        "can't", 'did not load', 'missing', 'no update', 'does not display', 'get rid', "can't view", 'system down', 
        "can't update", 'difficult', 'doesnt work', 'issue', 'bug']
    featurewords = ['add', 'would love', 'no way', 'would like', 'possible', 'would be nice', 'a way to', 'need to',
        'suggest', 'be able to', 'give options', 'should be', 'being able', 'ability', 'need', 'feature']
    instructionwords = ['how do i', 'not clear']
    jargon = ['ACW', 'ADP', 'AEBT', 'AET', 'AHT', 'ANI', 'BAU', 'BPO', 'BTC', 'BTOP', 'BTSC', 'BU', 'CBA', 'CBR', 
        'CCCS', 'CCM', 'COPQ', 'CPT', 'CR&M', 'CSI', 'CT', 'CTI', 'DNIS', 'EXL', 'GBCC', 'GBP', 'GCG', 'GDS', 'GPR',
        'GSR', 'GTT', 'HBS', 'ICM', 'IRD', 'IVR', 'JAR', 'KPI', 'LM', 'LRP', 'MCV', 'MLRB', 'MMD', 'MMS', 'MU', 'NIVR',
        'NOC', 'OBT', 'OLBT', 'ONS', 'PA', 'PA', 'PBX', 'PCC', 'PMO', 'PMP', 'PMP', 'PNR', 'SCCM', 'SD', 'SDL', 'SDM',
        'SDN', 'SDO', 'SIT', 'SLC', 'SLM', 'SQP', 'TC', 'TER', 'TL', 'TSF', 'VDN', 'VR', 'WAH', 'WBS', 'WFM', 'WIA',
        'TM','LOA']

    requesttypethis = 'Unknown'
    jargonthis = 'False'
    messagethis = text

    if messagethis is not None:
        if any(s in messagethis for s in bugreportwords):
            requesttypethis = 'Bug Report'
        if any(s in messagethis for s in featurewords):
            requesttypethis = 'Feature Request'
        if any(s in messagethis for s in instructionwords):
            requesttypethis = 'Instructions Needed'
        if any(s in messagethis for s in jargon):
            jargonthis = 'True'

    data = {"requesttypethis": requesttypethis, "jargonthis": jargonthis}
    return jsonify(data)
