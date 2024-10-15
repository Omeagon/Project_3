# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import plotly.express as px
import plotly.io as pio

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
#PostgreSQL credentials information
#Make sure psycopg2-binary is installed
#Update information as needed; may be a dynamic way to hide this info?
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
database = 'indycar'

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
indydata_2024 = Base.classes.indydata_2024

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
#This can likely be cleaned up to make a more user friendly appearance using a HTML template?
#Just getting basic layout in with routes.
#Made an educated suggestion for route location's based on graphics; feel free to change as needed
def welcome(): 
    """2024 IndyCar Season Evaluation"""
    return (
        f"<div style='font-size: 30px;'>"
        f"<strong>2024 IndyCar Season Evaluation:</strong>"
        f"<div style='font-size: 25px;'>"
        f"<strong>Graphics Content and Route Locations:</strong><br/><br/>"

        # Rob branch/route; update as needed.
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Championship Points by League (F1, IndyCar, IMSA)</strong><br/>" 
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Route Location: /IndyCar/points/Driver-Name<br/><br/>"

        # Laura branch/route; update as needed
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Average Speed by Track Type and Race</strong><br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Route Location: /IndyCar/speed<br/><br/>"

        # Jane's first branch/route; update as needed
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Number of Pit Stops per Race</strong><br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Route Location: /IndyCar/pitstops/Driver-Name<br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Enter the chosen driver to see the statistics by race.<br/><br/>"
        
        # Jane's second branch/route; update as needed
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Number of Laps Each Driver Completed per Race</strong><br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>" 
        f"Route Location: /IndyCar/lapscompeleted/Driver-Name<br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Enter the chosen driver to see the statistics by race.<br/><br/>"
        
        # James branch/route; update as needed
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Laps Led by Driver - Individual Race or Full Season</strong><br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Route Location: /IndyCar/lapsled/Race-Number<br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Enter the chosen race number (1-17) or All to see the statistics.<br/><br/>"
        
        # Ross branch/route; updated to include my graph of end less start
        # Positive represents ending higher than started; negative represents position loss
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>Average Start and End Position by Driver</strong><br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Route Location: /IndyCar/position/Driver-Name<br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Enter the chosen driver to see the statistics by race.<br/><br/>"
        
        f"<div style='text-indent: 0px; font-size: 20px;'>"
        f"<strong>View Underlying Data</strong><br/>"  
        f"<div style='text-indent: 20px; font-size: 15px;'>"      
        f"Route Location: /data<br/>"
        f"<div style='text-indent: 20px; font-size: 15px;'>"
        f"Returns underly data for graphics."
    )


#################################################
# Rob branch/route; update as needed.
#################################################
@app.route("/IndyCar/points")
def route1():
# Jsonify data to be returned    
    return jsonify()


#################################################
# Laura branch/route; update as needed
#################################################
@app.route("/IndyCar/speed")
def route2():
# Jsonify data to be returned    
    return jsonify()


#################################################
# Jane's first branch/route; update as needed
#################################################
@app.route("/IndyCar/pitstops/<driver>")
def pitstops(driver):
    results = session.query(
        indydata_2024.race_num,
        indydata_2024.race_city,
        indydata_2024,num_pit_stop
    ).filter(indydata_2024,driver == driver).order_by(indydata_2024.race_num).all()

#Prepare data for graph
data = []
for row in results:
    race_lable = f"{row.race_num}-{row.race_city}"
    data.append({
        'race_label':race_label,
        'num_pit_stop':row.num_pit_stop
    })
graph_data = pd.DataFrame(data)
fig = px.line(graph_data, x='race_label', y='num_pit_stop', title=f"Number of Pit Stops per {driver} by Race")
fig.update_layout(
    xaxis_title='Race Number and Location',
    yaxis_title='Number of Pit Stops'
)

graph_html = pio.to_html(fig, full_html=False)

#Return 
return render_template('pitstops.html', graph_html=graph_html)
# Jsonify data to be returned    
    return jsonify()


#################################################
# Jane's second branch/route; update as needed
#################################################
@app.route("/IndyCar/lapscompleted/<driver>")
def laps_completed(driver):

    results = session.query(
        indydata_2024.race_num,
        indydata_2024.race_city,
        indydata_2024.laps
    ).filter(indydata_2024.driver == driver).order_by(indydata_2024.race_num).all()
    
    data =[]
    for row in results:
        race_label = f"{row.race_num}-{row.race_city}"
        data.append({
            'race_label':race_label,
            'laps':row.laps
        })
graph_data = pd.DataFrame(data)

 fig = px.line(graph_data, x='race_label', y='laps', title=f"Number of Laps Completed by {driver} per Race")
    fig.update_layout(
        xaxis_title='Race Number and Location',
        yaxis_title='Laps Completed'
    )

    # Convert the figure to HTML
    graph_html = pio.to_html(fig, full_html=False)

    
    return render_template('laps_completed.html', graph_html=graph_html)
# Jsonify data to be returned    
    return jsonify()


#################################################
# James branch/route; update as needed
#################################################
@app.route("/IndyCar/lapsled/<race>")
def route5():
# Jsonify data to be returned    
    return jsonify()


#################################################
# Ross returns a line graph of end less start; kept formatting simple.
# Allows user to select the driver they wish to see.
#################################################
@app.route("/IndyCar/position/<driver>")
def position_change(driver):
    results = session.query(
        indydata_2024
    ).filter(indydata_2024.driver == driver
    ).order_by(indydata_2024.race_num).all()
    data = []
    for row in results:
        position_change = row.rank - row.start
        race_label = f"{row.race_num}-{row.race_city}"
        data.append({
            'race_label': race_label,
            'position_change': position_change
        })
    
    graph_data = pd.DataFrame(data)
    fig = px.line(graph_data, x='race_label', y='position_change', title = f"{driver}'s Performance by Race from Start to Finish")
    fig.update_layout(
        xaxis_title = 'Race number and location',
        yaxis_title = 'Change in position (start to finish)'
    )
    graph_html = pio.to_html(fig, full_html = False)

# Return chart   
    return render_template('position_change.html', graph_html=graph_html)


#################################################
# Returns jsonified underlying data.
#################################################
@app.route("/data")
def get_data():
    results = session.query(
        indydata_2024
    ).all()
    data = []
    for row in results:
        data.append({
            'race_num': row.race_num,
            'race_city': row.race_city,
            'rank': row.rank,
            'driver': row.driver,
            'car_no': row.car_no,
            'start': row.start,
            'laps': row.laps,
            'total_time': row.total_time,
            'laps_led': row.laps_led,
            'status': row.status,
            'avg_speed': row.avg_speed,
            'num_pit_stop': row.num_pit_stop,
            'points': row.points,
            'points_f1': row.points_f1,
            'points_IMSA': row.points_imsa
        })

# Jsonify data to be returned    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)