import pandas as pd
import os
from geopy.geocoders import Nominatim

this_dir = os.path.dirname(__file__)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(this_dir, "../data/city_day.csv"))
    return df



def get_lat_lon(place_name:'str'):
    "given a city/place name rerutn the lattitude and longitude "
    geolocator = Nominatim(user_agent='flask_app')
    location = geolocator.geocode(place_name)

    latitude = location.latitude
    longitude = location.longitude
    return ({'latitude':latitude ,'longitude':longitude })




def process_data() -> pd.DataFrame:
    df = load_data()

    # Change any datatype
    #Convert to Datetime formar
    df['Date'] = pd.to_datetime(df['Date'])

    #Get a Monthly Data
    df['month_year'] = df['Date'].dt.to_period('M')
    grouped_monthly_df = df.groupby(['City','month_year'])[['PM2.5','PM10', 'NO','NO2','CO']].sum().reset_index()

    #Get the city Location
    city_df = pd.DataFrame({'City':df['City'].unique()})
    city_df[['latitude','longitude']] = city_df['City'].apply(lambda x:pd.Series(get_lat_lon(x)))
    # Merge the info with grouped_monthly_df

    grouped_monthly_df = pd.merge(grouped_monthly_df,city_df,on='City')

    return grouped_monthly_df



def get_processed_data():
    file_path = os.path.join(this_dir, "../data/output/processed_data.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        temp_df = process_data()
        temp_df.to_csv(file_path,index=False)
        get_processed_data()


    