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
		upset = match.upset
		outcome = "W" if match.winner_char == char else "L"
		odds = match.odds(char)
		if match.red == char:
			opponent_elo = str(match.blue.elo)
			opponent = match.blue
		else:
			opponent_elo =  str(match.red.elo)
			opponent = match.red
		time = str(match.timestamp)[0:16]
		last5.append({'outcome': outcome, 'opponent_elo': opponent_elo, 'opponent': opponent, 'time': time, "odds": odds, "upset": upset})
	return last5