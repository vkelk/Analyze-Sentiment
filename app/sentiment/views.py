import json
import os
import requests
import uuid

from flask import jsonify, render_template, request, Markup, flash
from werkzeug.utils import secure_filename, CombinedMultiDict

from app.config import base_config
from app.sentiment import sentiment
from .forms import FileForm
from .audio2text import audio_to_flac, speech_recognition


@sentiment.route('/', methods=['GET', 'POST'])
@sentiment.route('/analyzesentiment', methods=['GET', 'POST'])
def index():
    form = FileForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        f = form.file_input.data
        filename = secure_filename(str(uuid.uuid4())[:8] + f.filename)
        file_location = os.path.join(
            base_config.UPLOAD_FOLDER, filename
            )
        f.save(file_location)
        temp_audio_file = audio_to_flac(file_location)
        if temp_audio_file:
            try:
                results = speech_recognition(
                    temp_audio_file,
                    base_config.API_KEY_SPEACH2TEXT
                    )
                text_results = '\n'.join(results['data'])
            except Exception as e:
                print(type(e), str(e))
                message = Markup(
                    "<strong>Error!</strong> Could not extract text from the file")
                flash(message, 'warning')
                text_results = None
        else:
            message = Markup(
                "<strong>Error!</strong> Incorrect input file format.")
            flash(message, 'danger')
            text_results = None
        return render_template(
            'index.html',
            form=form,
            text_results=text_results
            )
    """Returns the applications index page."""
    return render_template('index.html', form=form)


@sentiment.route('/getSentiment/<text>')
def getSentiment(text):
    api_url = 'http://text-processing.com/api/sentiment/'
    r = requests.post(api_url, data={'text': text})
    return jsonify(r.json())


@sentiment.route('/getLanguage/<text>')
def getLanguage(text):
    api_key = base_config.API_KEY_LANG
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
    bugreportwords = ['wrong', 'incorrect', 'not showing', 'slow', 'cannot',
        'error', 'not updating', 'challenge', "can't", 'did not load', 'missing',
        'no update', 'does not display', 'get rid', "can't view", 'system down',
        "can't update", 'difficult', 'doesnt work', 'issue', 'bug']
    featurewords = ['add', 'would love', 'no way', 'would like', 'possible',
        'would be nice', 'a way to', 'need to', 'suggest', 'be able to',
        'give options', 'should be', 'being able', 'ability', 'need', 'feature']
    instructionwords = ['how do i', 'not clear']
    jargon = ['ACW', 'ADP', 'AEBT', 'AET', 'AHT', 'ANI', 'BAU', 'BPO', 'BTC',
        'BTOP', 'BTSC', 'BU', 'CBA', 'CBR', 'CCCS', 'CCM', 'COPQ', 'CPT',
        'CR&M', 'CSI', 'CT', 'CTI', 'DNIS', 'EXL', 'GBCC', 'GBP', 'GCG', 'GDS',
        'GPR', 'GSR', 'GTT', 'HBS', 'ICM', 'IRD', 'IVR', 'JAR', 'KPI', 'LM',
        'LRP', 'MCV', 'MLRB', 'MMD', 'MMS', 'MU', 'NIVR', 'NOC', 'OBT', 'OLBT',
        'ONS', 'PA', 'PA', 'PBX', 'PCC', 'PMO', 'PMP', 'PMP', 'PNR', 'SCCM',
        'SD', 'SDL', 'SDM', 'SDN', 'SDO', 'SIT', 'SLC', 'SLM', 'SQP', 'TC',
        'TER', 'TL', 'TSF', 'VDN', 'VR', 'WAH', 'WBS', 'WFM', 'WIA', 'TM', 'LOA']

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
