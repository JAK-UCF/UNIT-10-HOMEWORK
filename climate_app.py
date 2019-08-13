# imports
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify

# create app
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

max_date = '2017-08-23'
start_date = '2016-08-24'
inception_date = '2010-01-01'

# define what to do when user visits index
@app.route("/")
def home():
    print("Server received a request for 'index' page.")
    return (
            f"<h1>Welcome to the Climate App!</h1>"
            f"<h2>Below are the current available routes for the Climate App:</h2>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/stations<br>"
            f"/api/v1.0/tobs<br><br><br>"
            f"<h3>User Selected Start and End Dates  -  ROUTE:</h3>"
            f"/api/v1.0/<start><br><br>"
            f"<h3>User Selected Start and End Dates  -  INSTRUCTIONS:</h3>\
                <strong>\
                1 - Choose dates between January 01, 2010 and August 23, 2017.<br>\
                2 - Enter dates in YYYY-MM-DD format.<br><br>\
                </strong>\
                After the final forward slash (/) in the 'User Selected Start and End Dates' route above, you may:<br><br>\
                A:<br>\
                Enter a <strong>start date</strong> only.<br>\
                <strong>EXAMPLE: /api/v1.0/2017-02-06</strong><br><br>\
                OR<br><br>\
                B:<br>\
                Enter <strong>start and end dates</strong>.<br>\
                *Seperate the start and end dates with a forward slash (/).<br>\
                <strong>EXAMPLE: /api/v1.0/2017-02-06/2017-04-10</strong><br><br><br>"            
    )

# define route '/api/v1.0/precipitation'
@app.route("/api/v1.0/precipitation")
def precip():
    '''Return precipitation activity by date.'''
    print("Server received a request for the Precipitation page.")

    precipitation_query = session.query(Measurement.date, Measurement.prcp)
    precipitation_activity_list = []
    for result in precipitation_query:
        precipitation_dict = {}
        precipitation_dict[result.date] = result.prcp
        precipitation_activity_list.append(precipitation_dict)
    
    return jsonify(precipitation_activity_list)


# define route '/api/v1.0/stations'
@app.route("/api/v1.0/stations")
def stations():
    '''Return station information.'''
    print("Server received a request for the Stations page.")
    
    station_query = session.query(Station)
    station_list = []
    for result in station_query:
        station_dict = {}
        station_dict['station_query_id'] = result.id
        station_dict['elevation'] = result.elevation
        station_dict['lat'] = result.latitude
        station_dict['long'] = result.longitude
        station_dict['name'] = result.name
        station_dict['station'] = result.station
        station_list.append(station_dict)
        
    return jsonify(station_list)


# define route '/api/v1.0/tobs'
@app.route("/api/v1.0/tobs")
def tobs():
    '''Return temperature observations for the last year (365 days). Returns most recent observation date first.'''
    print("Server received a request for the Temperature Observations page.")
    
    start_date = '2016-08-24'
        
    temperature_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.date.desc())
    temp_observation_list = []
    for result in temperature_query:
        temperature_dict = {}
        temperature_dict[result.date] = result.tobs
        temp_observation_list.append(temperature_dict)

    return jsonify(temp_observation_list)


# define route '/api/v1.0/<start>'
@app.route("/api/v1.0/<start>")
def temp_maths(start):
    '''Calculate the TMIN, TAVG, and TMAX for dates after start date (inclusive).''' 
    print("Server received a request for the Temperature Calculations (Start Only) page.")

    temperature_queries = []
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start)
    tmin_dict = {}
    tmin_dict['min_temp'] = tmin[0]
    temperature_queries.append(tmin_dict)
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start)
    tmax_dict = {}
    tmax_dict['max_temp'] = tmax[0]
    temperature_queries.append(tmax_dict)
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start)
    tavg_dict = {}
    tavg_dict['avg_temp'] = tavg[0]
    temperature_queries.append(tavg_dict)    
    
    return jsonify(temperature_queries)


# define route '/api/v1.0/<start>/<end>'
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    '''Calculate the TMIN, TAVG, and TMAX for dates between start and end (inclusive).'''
    print("Server received a request for the Temperature Calculations (Date Range) page.")

    temperature_queries = []
    min_temp = session.query(func.min(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end))
    min_temp_dict = {}
    min_temp_dict['min_temp'] = min_temp[0]
    temperature_queries.append(min_temp_dict)
    max_temp = session.query(func.max(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end))
    max_temp_dict = {}
    max_temp_dict['max_temp'] = max_temp[0]
    temperature_queries.append(max_temp_dict)
    avg_temp = session.query(func.avg(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end))
    avg_temp_dict = {}
    avg_temp_dict['avg_temp'] = avg_temp[0]
    temperature_queries.append(avg_temp_dict)

    return jsonify(temperature_queries)


if __name__ == "__main__":
    app.run(debug=True)