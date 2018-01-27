import os, sys, datetime
from helpers import *
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DEBUG = app.config['DEBUG']
TESTING = app.config['TESTING']
db = SQLAlchemy(app)


from models import *

@app.route('/', methods=['GET', 'POST'])
def index():
	errors = []
	results = []
	red_last5 = []
	blue_last5 = []
	try:
		latest = db.session.query(Match).order_by(Match.id.desc()).first()
		red_last5 = last_matches(latest.red, 5)
		blue_last5 = last_matches(latest.blue, 5)
	except:
		if TESTING or DEBUG: print(sys.exc_info())
		errors.append("Unable to query database.")
	return render_template('index.html', errors=errors, red=latest.red, blue=latest.blue, match=latest, red_last5=red_last5, blue_last5=blue_last5)

@app.route('/char/<id>', methods=['GET', 'POST'])
def char_view(id):
	errors = []
	results = []
	try:
		latest = db.session.query(Match).order_by(Match.id.desc()).first()
		char = db.session.query(Char).filter(Char.id == id).one_or_none()
		results = last_matches(char)
	except:
		if TESTING or DEBUG: print(sys.exc_info())
		errors.append("Unable to query database.")
	return render_template('char_view.html', errors=errors, results=results, char=char, red=latest.red, blue=latest.blue, match=latest)

if __name__ == '__main__':
	if len(sys.argv) != 1:
		 if sys.argv[1] == 'public': app.run(host='0.0.0.0')
	else:
		app.run(debug=True)