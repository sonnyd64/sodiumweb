from app import db
from models import *

#	last_matches()
# 	Function to pull x-number of recent *completed* matches by a character
#	If x=blank, will pull all matches in DB
def last_matches(char, x=None):
	last5 = []
	last_stg = db.session.query(Match).filter(db.or_(Match.red == char, Match.blue == char)).filter(Match.winner != None).order_by(Match.id.desc())[0:x]
	for match in last_stg:
		outcome = "?"
		outcome = "Won" if match.winner_char == char else "Lost"
		opponent = match.blue.name + " [" + match.blue.tier.replace(" ","") + ":" + str(match.blue.elo) + "]" if match.red == char else match.red.name + " [" + match.red.tier.replace(" ","") + ":" + str(match.red.elo) + "]"
		time = str(match.timestamp)[0:19]
		last5.append({'outcome': outcome, 'opponent': opponent, 'time': time})
	return last5