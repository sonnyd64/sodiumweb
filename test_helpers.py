import unittest
import os, sqlite3
from helpers import *
from models import *
from unittest.mock import Mock, MagicMock
#from flask_testing import TestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class TestLastMatches(unittest.TestCase):
	"""
	Test the last_matches() function
	"""

	# Set-up work
	def setUp(self):
		global db, test_char, test_char_1, test_char_5, test_char_25	

		

		# Establish mock db
		schema_file = open('schema_test.sql', 'r').read()
		self.app = Flask(__name__)
		self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
		self.app.config['TESTING'] = True
		self.db = SQLAlchemy(self.app)
		
		# create schema
		#self.db.engine.execute(schema_file)
		sql_command = ''
		# Iterate over all lines in the sql file
		for line in schema_file:
			# Ignore comented lines
			if not line.startswith('--') and line.strip('\n'):
				# Append line to the command string
				sql_command += line.strip('\n')

				# If the command string ends with ';', it is a full statement
				if sql_command.endswith(';'):
					# Try to execute statemente and commit it
					try:
						self.db.engine.execute(sql_command)

					# Assert in case of error
					except:
						print('Ops')

					# Finally, clear command string
					finally:
						sql_command = ''
		
		# insert multiple chars for testing
		test_chars = [(1, 'Example Player (General)', 'A', 0, 0, 31, 10, None, 800, 0),
			  		(2, 'Example Player 1 Match', 'A', 0, 1, 0, 1, None, 1000, 0),
			  		(3, 'Example Player 5 Matches', 'A', 0, 5, 0, 5, None, 1000, 0),
			  		(4, 'Example Player 25 Matches', 'A', 0, 25, 0, 25, None, 1000, 0)]
		for char in test_chars:
			self.db.engine.execute("INSERT INTO chars VALUES (?,?,?,?,?,?,?,?,?,?)", char)
		# insert multiple matches for testing
		test_matches = [(None, '2013-10-07 08:23:19', 1, 2, 2, 500, 200, 'm', '', 'A',False)]
		for i in range(5): 
			test_matches.append((None, '2013-10-07 08:23:19', 1, 3, 3, 500, 500, 'm', '', 'A',False))
		for i in range(25): 
			test_matches.append((None, '2013-10-07 08:23:19', 1, 4, 4, 500, 500, 'm', '', 'A',False))
		for match in test_matches:
			self.db.engine.execute("INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?)", match)		


		# Set up test chars
		test_char = self.db.session.query(Char).get(1)
		test_char_1 = self.db.session.query(Char).get(2)
		test_char_5 = self.db.session.query(Char).get(3)
		test_char_25 = self.db.session.query(Char).get(4)

	def tearDown(self):
		self.db.session.close()

	# Test integrity of matches returned
	def test_prior_match_format(self):
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_1,1,self.db)[0][0]
		self.assertEqual(output['outcome'],"W")
		self.assertEqual(output['opponent_elo'],'800')
		self.assertEqual(output['time'],"2013-10-07 08:23")
		self.assertEqual(output['tier'],"A")
		self.assertEqual(output['odds'],"1 : 2.5")
		self.assertEqual(output['upset'],True)

	# Test last matches w/ specified #
	def test_prior_matches_specific_count(self):
		# Compare "x" against count of what's returned, confirm success = True
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_25,5,self.db)[0]
		self.assertEqual(len(output),5)

	# Test last matches w/ specified # and too few in resultset
	def test_prior_matches_specific_count(self):
		# Compare "x" greater than count of what's returned, confirm success = False
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_1,5,self.db)
		self.assertEqual(output[1],False)
		output = output[0]
		self.assertEqual(len(output),1)

	# Test last matches w/o specificed #
	def test_prior_matches_return_all(self):
		# Compare result of COUNT(*) on DB query against count of what's returned
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_25,None,self.db)[0]
		self.assertEqual(len(output),25)

	# Negative test w/ invalid char
	def test_prior_matches_no_char(self):
		with self.assertRaises(AttributeError):
			last_matches(42, 1,self.db)

	# Negative test w/ None for char
	def test_prior_matches_nonint_count(self):
		self.assertEqual(last_matches(None,1,self.db),[[],True])

	# Negative test w/ non-integer and non-None 2nd arg
	def test_prior_matches_nonint_count(self):
		with self.assertRaises(TypeError):
			last_matches(test_char, "x",self.db)

if __name__ == '__main__':
	unittest.main()