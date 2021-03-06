from flask import Flask, render_template, request

from app.sentiment import sentiment
from app import config


def create_app(config=config.base_config):
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(sentiment, url_prefix='/analyzesentiment')

    @app.route('/', methods=['GET'])
    def index():
        """Returns the applications index page."""
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return 'This route does not exist {}'.format(request.url), 404

    if app.config['DEBUG'] is True:
        print(app.url_map)

    return app
