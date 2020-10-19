################################################################
# Dependencies 
################################################################

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request, render_template
from sqlalchemy.sql import text
import json
from sqlalchemy import JSON
from sqlalchemy import type_coerce
from sqlalchemy.dialects import mysql

import sys
# sys.path.insert(1, '..')

from config import username, password, port, db_name

################################################################
# Database Setup
################################################################

Base = automap_base()

engine = create_engine(f"postgresql://{username}:{password}@127.0.0.1:{port}/{db_name}")

Base.prepare(engine, reflect=True)

accident_db= Base.classes.accidents_usa_v2_db

session = Session(engine)

conn = engine.connect()

################################################################
# Flask Setup
################################################################

app = Flask(__name__, template_folder='')


@app.route('/hello_world')
def test_hello():
    return "Hello_World!"

@app.route('/')
def main_page():

    return render_template('index.html') #index.html main page

@app.route('/zipquery', methods=['GET', 'POST'])
def zip_query_sql(): # pass js variable how?
    # month_fetch = "March"

    test_var_js = request.args.get('get_zip')

    s = text(f'SELECT "Severity" , COUNT("Severity") FROM  "accidents_usa_v2_db" WHERE "Zipcode" = {test_var_js} GROUP BY "Severity";')

    # s = text(f'SELECT * FROM accidents_usa_v2_db WHERE "Month" = {test_var_js};')

    zip_fetch = conn.execute(s).fetchall()

    # return jsonify(zip_fetch)

    return jsonify({'result': [dict(row) for row in zip_fetch]})

@app.route('/zipcount', methods=['GET', 'POST'])
def zip_count_sql(): # pass js variable how?
    # month_fetch = "March"

    test_count_js = request.args.get('get_count')

    count = text(f'SELECT "Month", Count("Month") FROM accidents_usa_v2_db WHERE "Zipcode" = {test_count_js} GROUP BY "Month";')

    count_fetch = conn.execute(count).fetchall()

    return jsonify({'result': [dict(row) for row in count_fetch]})

if __name__ == '__main__':
    # app = Flask(__name__, template_folder='../')
    app.run(debug=True)