from flask import Blueprint, render_template
live = Blueprint('live', __name__, url_prifix='/live')

@live.route('/')
def index():
  renturn render_template('live/index.html')
  
