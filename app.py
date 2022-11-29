# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Add title
st.title('Introduction to Streamlit')
st.header('MPG Data Exploration')

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path='./data/mpg.csv')
mpg_df = deepcopy(mpg_df_raw) # Copy all objects except references

st.subheader('This is my dataset')
#st.table(data=mpg_df) # prints whole data as a table

# Widgets - checkbox to show data
if st.checkbox('Show Dataframe', value=False): # it automatically created the checkbox noted in the if loop!
    st.text('Data set used:')
    st.dataframe(data=mpg_df)

# Widgets - select box
years = ['All']+sorted(pd.unique(mpg_df['year']))
year = st.selectbox('Choose a year', years)

# Flow control for plotting:
# Define a dataframe depending on the year selection
if year == 'All':
    mpg_df_plot = mpg_df
else:
    mpg_df_plot = mpg_df[mpg_df['year']==year]

# Matplotlib scatter plot
m_fig,ax = plt.subplots(figsize=(10,8))
ax.scatter(mpg_df_plot['displ'], mpg_df_plot['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage", fontsize=22)
ax.set_xlabel('Displacement (Liters)', fontsize=14)
ax.set_ylabel('MPG', fontsize=14)

means = mpg_df_plot.groupby('class').mean()
ax.scatter(means['displ'], means['hwy'], alpha=0.7, color='red')

st.pyplot(m_fig)

# Plotly scatter plot
p_fig = px.scatter(mpg_df_plot, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

st.plotly_chart(p_fig)

# We can write stuff in our page
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)

# Creating a map based on lat and lon using Plotly EX
st.subheader('Point Map')
ds_geo = px.data.carshare()
ds_geo.rename({'centroid_lat': 'lat', 'centroid_lon': 'lon'}, axis=1, inplace=True)
#st.dataframe(data=ds_geo)
st.map(ds_geo)

# Sample Choropleth mapbox using Plotly GO
st.subheader("Choropleth Map")

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

plotly_map = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
plotly_map.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=2.8, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(plotly_map)