from flask import Flask,render_template
from flask import Flask
from flask import request, jsonify
from models import Time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy_utils import create_database, database_exists
from models import Time
from json import JSONEncoder
import pymysql

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default

JSONEncoder.default = _default

pymysql.install_as_MySQLdb()

url = 'mysql+pymysql://root:root@localhost:8889/TimerApp'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
engine = create_engine(url, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)

if not database_exists(url):
    create_database(url)
    metadata = MetaData(engine)
    # Create a table with the appropriate Columns
    Table("TimerEntries", metadata,
          Column('id', Integer, primary_key=True, nullable=False),
          Column('time', String(100)))
    metadata.create_all(engine)


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/getTimes')
def getTimes():

    try:
        session = Session()
        times = session.query(Time).all()
        return jsonify(times)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    finally:
        session.flush()
        session.close()


@app.route('/clearTimes')
def clearTimes():

    try:
        session = Session()
        session.query(Time).delete()
        session.commit()
        return jsonify('Times Cleared')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    finally:
        session.flush()
        session.close()


@app.route('/addTime', methods=['POST'])
def addTimePost():
    input_json = request.get_json(force=True)
    dictToReturn = {'time':input_json["time"]}
    session = Session()
    app.logger.info('try')

    try:
        newTime = Time()
        newTime.time = dictToReturn["time"]
        session.add(newTime)
        session.commit()
    except Exception as e:
        app.logger.info('try')

        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    finally:
        session.flush()
        session.close()
        return jsonify(dictToReturn)



if __name__ == '__main__':
    app.run()
