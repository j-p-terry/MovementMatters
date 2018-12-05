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

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

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


pairs = []
for origin in origins:
	for destination in destinations:
		pairs.append((origin, destination))

# Read in data
groups = {}
for pair in pairs:
	groups[pair] = pd.read_csv('./data/grouped_' + str(pair) + '.csv', skipinitialspace=True)
	groups[pair] = groups[pair][features]

# Get relevant data
sent = np.array([])
for origin in origins:
	total = 0
	for destination in destinations:
		total += groups[(origin, destination)].Value.sum()
	sent = np.append(sent, total)

avg_sent = np.array([])
for origin in origins:
	total = 0
	for destination in destinations:
		total += groups[(origin, destination)].Value.sum()/(groups[pair].Year.max() - groups[pair].Year.min())
	avg_sent = np.append(avg_sent, total)


dead = np.array([])
for origin in origins:
	total = 0
	for destination in destinations:
		total += groups[(origin, destination)].deaths.sum()
	dead = np.append(dead, total)

avg_dead = np.array([])
for origin in origins:
	total = 0
	for destination in destinations:
		total += groups[(origin, destination)].deaths.sum()/(groups[pair].Year.max() - groups[pair].Year.min())
	avg_dead = np.append(avg_dead, total)


arrived = np.array([])
for destination in destinations:
	total = 0
	for origin in origins:
		total += groups[(origin, destination)].Value.sum()
	arrived = np.append(arrived, total)

avg_arrived = np.array([])
for destination in destinations:
	total = 0
	for origin in origins:
		total += groups[(origin, destination)].Value.sum()/(groups[pair].Year.max() - groups[pair].Year.min())
	avg_arrived = np.append(avg_arrived, total)

dest_lats = [coordinates[dest][0] for dest in destinations] 
dest_lons = [coordinates[dest][1] for dest in destinations] 
org_lats = [coordinates[org][0] for org in origins] 
org_lons = [coordinates[org][1] for org in origins]

sent_each_year_by_orig = []
relative_sizes = []
for origin in origins:
	this_origin = []
	these_sizes = []
	for year in years:
		total = 0
		year = int(year)
		for destination in destinations:
			try:
				total += groups[(origin, destination)].query('Year == @year').Value.sum()
			except:
				total += 0
		this_origin.append(total)
	for i in range(len(years)):
		these_sizes.append(0.5e2*this_origin[i]/max(this_origin))
	sent_each_year_by_orig.append(this_origin)
	relative_sizes.append(these_sizes)

relative_sizes2 = [[] for i in range(len(years))]
for i in range(len(relative_sizes)):
	for ii in range(len(relative_sizes[i])):
		relative_sizes2[ii].append(relative_sizes[i][ii])

sent_each_year = [[] for i in range(len(years))]
year_sizes = [[] for i in range(len(years))]
for i in range(len(sent_each_year_by_orig)):
	for ii in range(len(sent_each_year_by_orig[i])):
		sent_each_year[ii].append(sent_each_year_by_orig[i][ii])
# 		year_sizes[ii].append(relative_sizes[i][ii])
for i in range(len(sent_each_year)):
	for ii in range(len(sent_each_year[i])):
		if max(sent_each_year[i]) != 0:
			year_sizes[i].append(50*sent_each_year[i][ii]/max(sent_each_year[i]))
		else:
			year_sizes[i].append(0)

dead_each_year = []
for year in years:
	this_year = []
	for origin in origins:
		total = 0
		for destination in destinations:
			try:
				total += groups[(origin, destination)].query('Year == @year').deaths.unique()[0]
				break
			except:
				total += 0
		this_year.append(total)
	dead_each_year.append(this_year)


dead_dic = {}
for i in range(len(years)-1):
	dead_dic[years[i]] = dead_each_year[i]
df_d = pd.DataFrame(dead_dic, index=origins)

sent_dic = {}
for i in range(len(years)-1):
	sent_dic[years[i]] = sent_each_year[i]
df_s = pd.DataFrame(sent_dic, index=origins)



# 
# for destination in destinations:


arr_each_year_by_dest = []
relative_sizes_arr = []
for destination in destinations:
	this_dest = []
	these_sizes = []
	for year in years:
		total = 0
		year = int(year)
		for origin in origins:
			try:
				total += groups[(origin, destination)].query('Year == @year').Value.sum()
			except:
				total += 0
		this_dest.append(total)
	for i in range(len(years)):
		these_sizes.append(0.5e2*this_dest[i]/max(this_dest))
	arr_each_year_by_dest.append(this_dest)
	relative_sizes_arr.append(these_sizes)
relative_sizes_arr2 = [[] for i in range(len(years))]
for i in range(len(relative_sizes_arr)):
	for ii in range(len(relative_sizes_arr[i])):
		relative_sizes_arr2[ii].append(relative_sizes_arr[i][ii])
arr_each_year = [[] for i in range(len(years))]
for i in range(len(arr_each_year_by_dest)):
	for ii in range(len(arr_each_year_by_dest[i])):
		arr_each_year[ii].append(arr_each_year_by_dest[i][ii])

totals = {}
for origin in origins:
	totals[origin] = []

for j in range(len(origins)):
	for i in range(len(years)):
		this_year = []
		a_year = years[i]
		for ii in range(len(destinations)):
			if arr_each_year[i][ii] != 0:
				sent_to = groups[(origins[j], destinations[ii])].\
							query('Year == @a_year').Value.sum()
				this_year.append(sent_to)
			else:
				this_year.append(0)
		totals[origins[j]].append(this_year)

df_t = pd.DataFrame(index = years)

for i in range(len(origins)):
	df_t[origins[i]] = totals[origins[i]] 



'''Graphs with sliders'''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	dcc.Graph(id='graph-with-slider'),
	dcc.Slider( # Makes slider
		id='year-slider',
		min=2000,
		max=2017,
		value=2000,
# 		marks=years[:len(years) - 1]
		marks={str(year): str(year) for year in years[:len(years)-1]}
	)
])


@app.callback(
	dash.dependencies.Output('graph-with-slider', 'figure'),
	[dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):

	'''Updates the figure when the slider is moved'''

	# Gets data based off of the year that the slider is on
	filtered_df = df_t.loc[selected_year, :]
	traces = []

	'''Filters by continent'''
	for i in origins: # filter by country
# 		percentages = filtered_df[i] # filter by country
		total = filtered_df[i]
		traces.append(go.Scatter(
			x=[j for j in range(1, 7)],
			y=total,
# 			text=(stat.pearsonr(sent_by_country,dead_by_country),stat.spearmanr(sent_by_country,dead_by_country)),
# 			text = total,
			mode='markers',
			opacity=0.7,
			marker={
				'size': 15,
				'line': {'width': 0.5, 'color': 'white'}
			},
			name=i
		))

	return {
		'data': traces,
		'layout': go.Layout(
			xaxis={'title': 'Receiving Country', 'tickvals':[1,2,3,4,5,6], \
					'ticktext':destinations},
			yaxis={'title': 'Total From Origin'},
			margin={'l': 70, 'b': 40, 't': 10, 'r': 70},
			legend={'x': 0, 'y': 1},
			hovermode='closest'
		)
	}




if __name__ == '__main__':
	app.run_server(debug=True)
































