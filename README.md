fav-locations
=============

This is a demo app which manages favorite locations for a given user.

This app requires
- flask http://flask.pocoo.org/
- sqlite3 and python sqlite3 bindings

Usage:
python fav_locations.py

The app can be accessed at http://127.0.0.1:5000/

Improvements:
- User login portal along with authentication
- Prevent XSS via input santization before storing in database 
- User authentication required for accessing the API
- Better user interaction in a dynamic way
- Better styling
