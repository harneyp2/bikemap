from flask import *
from flask import g
import sqlite3

from bike_scraper.core import *
from bike_scraper.analysis import GatherData
from bike_scraper.averages import *

app = Flask(__name__)

DATABASE = 'bike_scraper/bikedata.db'
jsonFetcher = GatherData()
scraper = BikeScraper()
ave = averager()

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/getjson/<sid>')
def jsonstuff(sid):
    cur = get_db().cursor()
    row = ave.getDayAverage(cur, sid,'Monday')
    print(row)
    jsonFile = jsonFetcher.generate_json(row)
    return jsonFile
    

@app.route('/')
def hello_world():
    return render_template('bikemap.html')

    

if __name__ == '__main__':
    app.run(debug = True)