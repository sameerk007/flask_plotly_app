from flask import Flask, render_template, request
import plotly
import pandas as pd
from app_logic import data_processing , plotly_plpt
from flask_caching import Cache
import json


app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

# Get the required data
processed_data = data_processing.get_processed_data()
city_list = processed_data['City'].unique()


@app.route('/')
def home():
    try:
        selected_city = request.args.get('city')
    except:
        pass

    # Filter the Data based on city
    city_data = processed_data[processed_data['City'] == selected_city]
    air_quality_attributes = ['PM2.5','NO','NO2','CO']

    # Create the figure/plot
    fig = plotly_plpt.get_plot(city_data,columns=air_quality_attributes,title=f"Air Quality for City : {selected_city}")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',graphJSON= graphJSON,CityList = city_list)


@app.route('/data')
def data():
    data = processed_data.to_html(index=False)
    return render_template('data.html', data=data)  




if __name__ == '__main__':
    app.run(debug=True)