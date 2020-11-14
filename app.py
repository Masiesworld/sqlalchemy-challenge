import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database 
Base = automap_base()
Base.prepare(engine, reflect=True)

# connect to tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    """Return the JSON representation of your dictionary."""
    session = Session(engine)
    results_prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcp_scores = []
    for p in prcp_query:
        my_dict = {}
        my_dict[prcp_query[0]] = prcp_query[1]
        prcp_scores.append(my_dict)

    return jsonify(prcp_scores)

@app.route("/api/v1.0/stations")
"""Return a JSON list of stations from the dataset."""
def station():
    session = Session(engine)
    results_station = session.query(Station.station, Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    station = []
    for station, name, lat,lon,ele in results_station:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = lon
        station_dict["elevation"] = ele
        station.append(station_dict)

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    """
    Query the dates and temperature observations of the most active station 
    for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year.
    """
    session = Session(engine)
    latest_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    previous_year = (dt.datetime.strptime(lastest_day,'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    
    sel = [Measurement.date,Measurement.tobs]
    results_date = session.query(*sel).filter(Measurement.date >= previous_year).order_by(Measurement.date).all()
    session.close()

    tobs = []
    for date, tobs in results_date:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)



@app.route("/api/v1.0/<start>")
"""
Return a JSON list of the minimum temperature, the average temperature, 
and the max temperature for a given start or start-end range.

When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
greater than and equal to the start date.
"""
session = Session(engine)
start_date = dt.datetime.strptime(start, %Y-%m-%d)
sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
results_startdate = session.query(*sel).filter(Measurement.date >= start_date).group_by(Measurement.date).all()
session.close()

date_info = []
for date,min,avg,max in results_startdate:
    start_dict = {}
    start_dict['Date'] = date
    start_dict['TMIN'] = min
    start_dict['TAVG'] = avg
    start_dict['TMAX'] = max
    date_info.append(start_dict)

return jsonify(date_info)



@app.route("/api/v1.0/<start>/<end>")
"""When given the start and the end date, calculate the TMIN, TAVG, 
and TMAX for dates between the start and end date inclusive."""
session = Session(engine)
start_date = dt.datetime.strptime(start, %Y-%m-%d)
end_date = dt.datetime.strptime(end, %Y-%m-%d)

sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
results_startdate = session.query(*sel).filter(Measurement.date >= start_date).\
                    filter(Measurement.date <= end_date).\
                    group_by(Measurement.date).all()
session.close()

date_info = []
for date,min,avg,max in results_startdate:
    startend_dict = {}
    startend_dict['Date'] = date
    startend_dict['TMIN'] = min
    startend_dict['TAVG'] = avg
    startend_dict['TMAX'] = max
    date_info.append(startend_dict)

return jsonify(date_info)


if __name__ == "__main__":
    app.run(debug=True)
