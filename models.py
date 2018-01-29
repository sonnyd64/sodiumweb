from app import db

class Char(db.Model):
	__tablename__ = 'chars'

	team = "?"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	_tier = db.Column("tier", db.CHAR(3))
	streak = db.Column(db.Integer)
	wins = db.Column(db.Integer)
	losses = db.Column(db.Integer)
	matches_at_tier = db.Column(db.Integer)
	elo = db.Column(db.Integer)
	tourny_wins = db.Column(db.Integer)
	last_match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
	last_match = db.relationship("Match",  foreign_keys=[last_match_id])

	@property
	def tier(self):
		return self._tier.replace(" ","")

	@tier.setter
	def tier(self, tier):
		self._tier = str(tier)

	def __repr__(self):
		return '<id {} - {}>'.format(self.id, self.name)

class Match(db.Model):
	__tablename__ = 'matches'

	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.TIMESTAMP(timezone=True))
	tier = db.Column(db.CHAR(3))
	red_money = db.Column(db.Integer)
	blue_money = db.Column(db.Integer)
	mode = db.Column(db.CHAR(1))
	notes = db.Column(db.String())
	
	red_char = db.Column(db.Integer, db.ForeignKey('chars.id'))
	red = db.relationship("Char", foreign_keys=[red_char])
	blue_char = db.Column(db.Integer, db.ForeignKey('chars.id'))
	blue = db.relationship("Char", foreign_keys=[blue_char])
	winner = db.Column(db.Integer, db.ForeignKey('chars.id'))
	winner_char = db.relationship("Char", foreign_keys=[winner])

	def get_red_exp(self):
		return round(100*(1.0 / (1.0 + pow(10, ((self.blue.elo - self.red.elo) / 400)))),2);

	def get_blue_exp(self):
		return round(100*(1.0 / (1.0 + pow(10, ((self.red.elo - self.blue.elo) / 400)))),2);

	@property
	def upset(self):
		if self.winner_char == self.red:
			if self.red_money > self.blue_money: return False
			if self.red_money < self.blue_money: return True
		elif self.winner_char == self.blue:
			if self.red_money < self.blue_money: return False
			if self.red_money > self.blue_money: return True
		else:
			return False;

	def odds(self, char):
		if char == self.red:
			odds = self.red_money / self.blue_money
			if self.red_money > self.blue_money:
				return "{:.1f} : 1".format(odds)
			if self.red_money <= self.blue_money:
				return "1 : {:.1f}".format(1/odds)
		elif char == self.blue:
			odds = self.blue_money / self.red_money
			if self.red_money <= self.blue_money:
				return "{:.1f} : 1".format(odds)
			if self.red_money > self.blue_money:
				return "1 : {:.1f}".format(1/odds)
		else:
			return False;

#	def __init__(self, url, result_all, result_no_stop_words):
#		self.url = url
#		self.result_all = result_all
#		self.result_no_stop_words = result_no_stop_words

	def __repr__(self):
		return '<id {} - {}>'.format(self.id, self.timestamp)