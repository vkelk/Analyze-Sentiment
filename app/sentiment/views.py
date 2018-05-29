import requests
from flask import jsonify, render_template
from app.sentiment import sentiment


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
