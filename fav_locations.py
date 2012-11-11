import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash, json, jsonify

# configuration
DATABASE = 'fav_locations.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

DB_FILE_PATH = os.path.join(os.getcwd(), app.config['DATABASE'])

def connect_db():
	return sqlite3.connect(DB_FILE_PATH)

def init_db():
	# creates the schema in the db if not present
	if not os.path.exists(DB_FILE_PATH):
		cur = connect_db()
		query_file = open(os.path.join(os.getcwd(), 'initialize_db.sql'))
		cur.executescript(query_file.read())

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def homepage():
	return render_template('homepage.html')
	 
@app.route('/show_all_locations/')
def display_locations():
	return render_template('show_locations.html')

@app.route('/create_location/')
def create_new_location():
	return render_template('create_location.html')

@app.route('/location/create/', methods = ['POST'])
def insert_new_location():
	g.db.execute('insert into locations (user_id, lat, long, address, name) \
		values (?, ?, ?, ?, ?)', [
		request.form['user_id'],
		request.form['lat'], 
		request.form['long'], 
		request.form['address'], 
		request.form['name']])
	g.db.commit()
	return jsonify(message= "location added")

@app.route('/location/show/all/')
def show_all_locations():
	cur = g.db.execute('select * from locations')
	col_names = ['location_id', 'user_id', 'lat', 'long', 'address', 'name']
	locations = [dict(zip(col_names, row)) for row in cur.fetchall()]	
	return jsonify(locations=locations)

@app.route('/location/show/<location_id>/')
def show_given_location(location_id):
	cur = g.db.execute('select * from locations where id = ?', [location_id])
	data = cur.fetchone()	
	locations = []
	if data:
		col_names = ['location_id', 'user_id', 'lat', 'long', 'address', 'name']
		locations = [dict(zip(col_names, data))]
	return jsonify(locations=locations)

@app.route('/location/remove/<location_id>/')
def remove_location(location_id):
	g.db.execute('delete from locations where id = ?', [location_id])
	g.db.commit()
	return jsonify(message= "location deleted")

@app.route('/location/update/', methods = ['POST'])
def update_location():
	g.db.execute('update locations set user_id = ?, lat = ?, long = ?, address = ?, name = ? where id = ?',  	
		[request.form['user_id'],
		request.form['lat'], 
		request.form['long'], 
		request.form['address'], 
		request.form['name'],
		request.form['id']])
	g.db.commit()
	return jsonify(message= "location updated")

if __name__ == '__main__':
	init_db()
	app.run(host='0.0.0.0')
