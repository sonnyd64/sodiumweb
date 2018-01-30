# SodiumBot Web Front-End
Utilizing Flask, PostgreSQL, SQLAlchemy, Bootstrap, NoSleep.js, FontAwesome, Jailer (for dev/test DB subsets)

## To-do:
* ~~Connect to local DB and expose existing data via SQLAlchemy~~
* ~~Basic data output via Flask/Jinja2~~
	* ~~Character data pages~~
	* Add tier change history, tourn wins to index and char pages
	* Alert for prior matchups
	* Move CSS to separate file
	* ~~Data table construction for match data instead of strings~~
	* Match data pages (bettor/bet info, char data)
* **[IN PROGRESS] Unit testing (Look into Flask-Testing for Flask-SQLAlchemy)**
* Note writing functionality
	* Add note field to chars
* Create lower-privileged user for data consumption
* Live updating: AJAX not auto-refresh
* Live console feed from bot
* Extract remote char id for image
* Determine how to migrate/stage data in heroku/across dev machines (sample extract?)