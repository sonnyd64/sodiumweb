import os, sys, datetime
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
		results.append(latest.red)
		results.append(latest.blue)
		red_last5_stg = db.session.query(Match).filter(db.or_(Match.red == latest.red, Match.blue == latest.red)).filter(Match.winner != None).order_by(Match.id.desc())[0:5]
		blue_last5_stg = db.session.query(Match).filter(db.or_(Match.red == latest.blue, Match.blue == latest.blue)).filter(Match.winner != None).order_by(Match.id.desc())[0:5]
		for match in red_last5_stg:
			outcome = "?"
			outcome = "Won" if match.winner_char == latest.red else "Lost"
			opponent = match.blue.name + " [" + match.blue.tier.replace(" ","") + ":" + str(match.blue.elo) + "]" if match.red == latest.red else match.red.name + " [" + match.red.tier.replace(" ","") + ":" + str(match.red.elo) + "]"
			time = str(match.timestamp)[0:19]
			red_last5.append({'outcome': outcome, 'opponent': opponent, 'time': time})
		for match in blue_last5_stg:
			outcome = "?"
			outcome = "Won" if match.winner_char == latest.blue else "Lost"
			opponent = match.blue.name + " [" + match.blue.tier.replace(" ","") + ":" + str(match.blue.elo) + "]" if match.red == latest.blue else match.red.name + " [" + match.red.tier.replace(" ","") + ":" + str(match.red.elo) + "]"
			time = str(match.timestamp)[0:19]
			blue_last5.append({'outcome': outcome, 'opponent': opponent, 'time': time})
	except:
		if TESTING or DEBUG: print(sys.exc_info())
		errors.append("Unable to query database.")
	return render_template('index.html', errors=errors, results=results, red=latest.red, blue=latest.blue, match=latest, red_last5=red_last5, blue_last5=blue_last5)

if __name__ == '__main__':
	if len(sys.argv) != 1:
		 if sys.argv[1] == 'public': app.run(host='0.0.0.0')
	else:
		app.run(debug=True)