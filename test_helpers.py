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

		# Confirm the old test db doesn't exist, delete and alert if so
		# [TODO: Why is tearDown() not executing on failed tests?]
		if os.path.isfile('unittest.db'):
			os.remove('unittest.db')
			print("Test db was not cleaned up last run!")		

		# Establish mock db
		schema_file = open('schema_test.sql', 'r').read()
		conn = sqlite3.connect("file::memory:?cache=shared")
		cursor = conn.cursor()
		# create schema
		cursor.executescript(schema_file)

		# insert multiple chars for testing
		test_chars = [(1, 'Example Player (General)', 'A', 0, 0, 31, 10, None, 800, 0),
			  		(2, 'Example Player 1 Match', 'A', 0, 1, 0, 1, None, 1000, 0),
			  		(3, 'Example Player 5 Matches', 'A', 0, 5, 0, 5, None, 1000, 0),
			  		(4, 'Example Player 25 Matches', 'A', 0, 25, 0, 25, None, 1000, 0)]
		cursor.executemany("INSERT INTO chars VALUES (?,?,?,?,?,?,?,?,?,?)", test_chars)
		# insert multiple matches for testing
		test_matches = [(None, '2013-10-07 08:23:19', 1, 2, 2, 500, 200, 'm', '', 'A',False)]
		for i in range(5): 
			test_chars.append((None, '2013-10-07 08:23:19', 1, 3, 3, 500, 500, 'm', '', 'A',False))
		for i in range(25): 
			test_chars.append((None, '2013-10-07 08:23:19', 1, 4, 4, 500, 500, 'm', '', 'A',False))
		cursor.executemany("INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?)", test_matches)		
		# save data to database
		conn.commit()
		conn.close()

		# Connect SQLAlchemy [TO-DO: Roll the above into SQLAlchemy]
		self.app = Flask(__name__)
		self.app.config['SQLALCHEMY_DATABASE_URI'] = "file::memory:?cache=shared"
		self.app.config['TESTING'] = True
		self.db = SQLAlchemy(self.app)

		# Set up test chars
		test_char = self.db.session.query(Char).get(1)
		test_char_1 = self.db.session.query(Char).get(2)
		test_char_5 = self.db.session.query(Char).get(3)
		test_char_25 = self.db.session.query(Char).get(4)

	def tearDown(self):
		print("Deleting mock db!")
		self.db = None
		#os.remove('unittest.db')		

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
		output = last_matches(test_char_25,5)
		self.assertEqual(1,1)

	# Test last matches w/ specified # and too few in resultset
	def test_prior_matches_specific_count(self):
		# Compare "x" greater than count of what's returned, confirm success = False
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_1,5)
		self.assertEqual(1,1)

	# Test last matches w/o specificed #
	def test_prior_matches_return_all(self):
		# Compare result of COUNT(*) on DB query against count of what's returned
		# !!! NEED TO FINISH !!!
		output = last_matches(test_char_25)
		self.assertEqual(1,1)

	# Negative test w/ invalid char
	def test_prior_matches_no_char(self):
		with self.assertRaises(AttributeError):
			last_matches(42, 1)

	# Negative test w/ None for char
	def test_prior_matches_nonint_count(self):
		self.assertEqual(last_matches(None),[[],True])

	# Negative test w/ non-integer and non-None 2nd arg
	def test_prior_matches_nonint_count(self):
		with self.assertRaises(TypeError):
			last_matches(test_char, "x")

if __name__ == '__main__':
	unittest.main()