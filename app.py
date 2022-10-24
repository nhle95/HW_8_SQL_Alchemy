import re
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.metadata.tables 
Base.classes.keys() # Get the table names

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Most active stations 1 year tobs: /api/v1.0/tobs<br/>"
        f"Input the day you want to see: /api/v1.0/<start><br/>"
        f"Input the range of days you want to see: /api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    sel = [Measurement.date,Measurement.prcp]
    query_result = session.query(*sel).all()
    session.close()

    precipitation_list = []
    for date, prcp in query_result:
        precipitation = {}
        precipitation["Date"] = date
        precipitation["Precipitation"] = prcp
        precipitation_list.append(precipitation)
    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    query_result = session.query(*sel).all()
    session.close()

    stations_list = []
    for station,name,lat,lon,el in query_result:
        stations = {}
        stations["Station"] = station
        stations["Name"] = name
        stations["Lat"] = lat
        stations["Lon"] = lon
        stations["Elevation"] = el
        stations_list.append(stations)

    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    converted_recent_date = dt.datetime.strptime(most_recent[0], '%Y-%m-%d')
    one_year_ago = converted_recent_date - dt.timedelta(days =366)
    sel = [Measurement.date,Measurement.tobs]
    query_result = session.query(*sel).filter(Measurement.date >= query_date).all()
    session.close()

    tobs_list = []
    for date, tob in query_result:
        tobs = {}
        tobs["Date"] = date
        tobs["Tob"] = tob
        tobs_list.append(tobs)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>/<end>')
def start_to_end(start, end):
    session = Session(engine)
    sel =[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    query_result = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs_list = []
    for min,avg,max in query_result:
        tobs = {}
        tobs["Min"] = min
        tobs["Average"] = avg
        tobs["Max"] = max
        tobs_list.append(tobs)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    sel =[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    query_result = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()

    tobs_list = []
    for min,avg,max in query_result:
        tobs = {}
        tobs["Min"] = min
        tobs["Average"] = avg
        tobs["Max"] = max
        tobs_list.append(tobs)

    return jsonify(tobs_list)
if __name__ == '__main__':
    app.run(debug=True)