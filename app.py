import os, sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DEBUG = app.config['DEBUG']
TESTING = app.config['TESTING']
db = SQLAlchemy(app)


from models import *

def loadSession():
	""""""
	metadata = db.metadata
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

@app.route('/', methods=['GET', 'POST'])
def index():
	errors = []
	results = []
	try:
		latest = db.session.query(Match).order_by(Match.id.desc()).first()
		results.append(latest.red)
		results.append(latest.blue)
	except:
		if TESTING or DEBUG: print(sys.exc_info())
		errors.append("Unable to query database.")
	return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
	app.run()