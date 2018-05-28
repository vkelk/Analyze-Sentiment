import requests
from flask import jsonify
from app.sentiment import sentiment


@sentiment.route('/getSentiment/<text>')
def getSentiment(text):
    api_url = 'http://text-processing.com/api/sentiment/'
    r = requests.post(api_url, data={'text': text})
    return jsonify(r.json())
