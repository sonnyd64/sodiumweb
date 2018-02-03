from app import db
from models import *

#	last_matches()
# 	Function to pull x-number of recent *completed* matches by a character
#	If x=blank, will pull all matches in DB
def last_matches(char, x=None, db=db):
	matches = []
	success = False
	for match in last_stg:
		outcome = "?"
		upset = match.upset
		tier = match.tier
		outcome = "W" if match.winner_char == char else "L"
		odds = match.odds(char)
		if match.red == char:
			opponent_elo = str(match.blue.elo)
			opponent = match.blue
		else:
			opponent_elo =  str(match.red.elo)
			opponent = match.red
		time = str(match.timestamp)[0:16]
		matches.append({'outcome': outcome, 'opponent_elo': opponent_elo, 'opponent': opponent, 'time': time, 'tier': tier, "odds": odds, "upset": upset})

	# Pass back success = False if fewer than requested rows were returned
	if len(matches) == x: success = True
	if x == None: success = True
	return [matches, success]