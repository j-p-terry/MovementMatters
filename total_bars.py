#
# Scatter_Markdown.py
#

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import seaborn as sb
import plotly
import dash
import plotly.plotly as ply
from plotly.graph_objs import *
from scipy.io import netcdf
import scipy.stats as stat

# plotly.tools.set_credentials_file(username='jpterry', api_key='jC0hHrhZQhOys3ypgeg8')


origins = ["DR_Congo", "Afghanistan", "Syria", "Myanmar", "Sudan"]
destinations = ["USA", "UK", "France", "Canada", "Italy", "Germany"]

org_codes = ["COD", "AFG", "SYR", "MMR", "SDN"]
dest_codes = ["USA", "GBR", "FRA", "CAN", "ITA","DEU"]

years = [2000 + i for i in range(19)]

features = ['destination',
 'Origin',
 'applied',
 'accepted',
 'Rejected',
 'decisions',
 'Year',
 'Month',
 'Value',
 'deaths',
 'last_month',
 'two_months_ago',
 'next_month',
 'two_months_later']


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

combos = []
for year in years:
	for month in months:
		combos.append((month, year))


coordinates = {}
coordinates["Syria"] = (34.8, 38.997)
coordinates["DR_Congo"] = (-4.0383, 21.759)
coordinates["Afghanistan"] = (33.939, 67.71)
coordinates["Sudan"] = (12.863, 30.218)
coordinates["Myanmar"] = (21.9162, 95.956)

coordinates["USA"] = (37.09, -95.713)
coordinates["UK"] = (55.378, -3.436)
coordinates["France"] = (46.228, 2.214)
coordinates["Germany"] = (51.166, 10.4515)
coordinates["Italy"] = (41.872, 12.5674)
coordinates["Canada"] = (56.1304, -106.3468)


marker_places= [12*i for i in range(18)]
tick_labs = [str(year) for year in years]

pairs = []
for origin in origins:
	for destination in destinations:
		pairs.append((origin, destination))

# Read in data
df = pd.read_csv('./data/all_merged.csv', skipinitialspace=True)

symbols = {'USA': 'triangle-down', 'UK': 'square', 'Germany': 'cross', 'France': 'triangle-up',\
			'Italy':'star', 'Canada': 'circle'}

shapes = np.array([symbols[country] for country in destinations])


markers = []
for index, row in df.iterrows():
	markers.append(symbols[row["destination"]])
df['shapes'] = markers


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	# Graph of data
	dcc.Graph(
		id='trends',
		figure={
			'data': [
				go.Scatter(
					x=[j for j in range(12*18)],
					y=df[df['Origin'] == i]['Value'],
					text=df[df['Origin'] == i]['destination'],
					mode='markers',
					opacity=0.7,
					legendgroup = i,
					marker={
						'size': 12,
						'line': {'width': 0.5, 'color': 'white'},
						'symbol': df[df['Origin'] == i]['shapes']
					},
					name=i
				) for i in df.Origin.unique()
			],
			'layout': go.Layout(
				xaxis={'title': 'Month', 'tickvals':marker_places, 'ticktext':tick_labs},
				yaxis={'title': 'Refugees Accepted'},
				margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
				legend={'x': 0, 'y': 1},
				hovermode='closest'
			)
		}
	),
	dcc.Graph(
		id='next-month',
		figure={
			'data': [
				go.Bar(
					x=[j for j in range(1,19)],
					y=df[df['Origin'] == i].deaths.unique(),
# 					text=df[df['Origin'] == i]['destination'],
# 					mode='markers',
					opacity=0.7,
# 					marker={
# 						'size': 12,
# 						'line': {'width': 0.5, 'color': 'white'}#,
# 						'symbol': df[df['Origin'] == i]['shapes']
# 					},
					name=i
				) for i in df.Origin.unique()
			],
			'layout': go.Layout(
				xaxis={'title': 'Month', 'tickvals':[j for j in range(1,19)], 'ticktext':tick_labs},
				yaxis={'title': 'Battle Deaths'},
				margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
				legend={'x': 0, 'y': 1},
				barmode='stack',
				hovermode='closest'
			)
		}
	)

])



if __name__ == '__main__':
	app.run_server(debug=True)