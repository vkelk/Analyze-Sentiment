from flask import Blueprint

sentiment = Blueprint('sentiment', __name__, template_folder='templates')

from . import views
