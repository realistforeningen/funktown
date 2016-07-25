from pony.orm import Database

db = Database()
db.bind('sqlite', 'app.db')

