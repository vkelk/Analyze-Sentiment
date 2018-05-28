from flask import Flask, render_template

from app.sentiment import sentiment
from app import config


def create_app(config=config.base_config):
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(sentiment)

    @app.route('/', methods=['GET'])
    def index():
        """Returns the applications index page."""
        return render_template('index.html')

    if app.config['DEBUG'] == True:
        print(app.url_map)

    return app
