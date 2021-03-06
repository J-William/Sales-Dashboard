"""
	Sales Report Dashboard

"""

from asyncio.windows_events import NULL
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Using a basic CSS stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Clear layout and don't display exceptions until callback
app.config.suppress_callback_exceptions = True

# Read in the data	
data = pd.read_csv('sales.csv')
# Get the list of states for the dropdown
states = sorted(list(data['State'].unique()))


# Application layout
app.layout = html.Div(children=[
	# Title
	html.H1('Sales Reporting Dashboard'),
	# Row 1
	html.Div([
		# Graph 1
		html.Div([
				html.H5('Profit by Segment and State'),
				dcc.Dropdown(
						id='segment-input',
						options=[{'label': i, 'value': i} for i in states],
						placeholder="Select a state",
						style= {'width': 300, 'padding': 3}
						),
				dcc.Graph(id='segment-plot')
				], style= {'padding': 3}, className='six columns'),
		# Graph 2
		html.Div([
				html.H5('Ship Mode Requested by State'),
				dcc.Dropdown(
						id='ship-input',
						options=[{'label': i, 'value': i} for i in states],
						placeholder="Select a state",
						style= {'width': 300, 'padding': 3}
						),
				dcc.Graph(id='ship-plot')
				], style= {'padding': 3}, className='six columns')
	], className='twelve columns'),
	# Row 2
	html.Div([
		# Graph 3
		html.Div([
				"Input: ",
				dcc.Dropdown(
						id='del-input',
						options=[{'label': i, 'value': i} for i in states],
						placeholder="Select a state",
						style= {'width': 300, 'padding': 3}
						),
				dcc.Graph(id='del-plot')
				], style= {'padding': 3}, className='six columns'),
		# Graph 4
		html.Div([
							"Input: ",
				dcc.Dropdown(
						id='sale-input',
						options=[{'label': i, 'value': i} for i in states],
						placeholder="Select a state",
						style= {'width': 300, 'padding': 3}
						),
				dcc.Graph(id='sale-plot')
			], style= {'padding': 3}, className='six columns')
	], className='twelve columns')

])
	


# Callback for the top left bar chart of profit by segment and state
@app.callback(Output(component_id='segment-plot', component_property='figure'),
				Input(component_id='segment-input', component_property='value'))
def get_segment_graph(segment_input):
	if not segment_input:
		return NULL

	segment_data = data.copy()

	# Get the data for the selected state
	segment_data = segment_data.groupby(['State', 'Segment'])['Profit'].sum().reset_index()
	segment_data = segment_data[segment_data['State'] == segment_input]

	# Build the bar chart
	bar_fig = px.bar(segment_data, x='Segment', y='Profit')

	return bar_fig


# Callback for the top right pie chart of ship mode requested by state
@app.callback(Output(component_id='ship-plot', component_property='figure'),
				Input(component_id='ship-input', component_property='value'))
def get_shipment_graph(ship_input):
	if not ship_input:
		return NULL

	ship_data = data.copy()
	# Get the required dataset from the sales data 
	ship_data = ship_data.groupby('State')['Ship Mode'].value_counts()

	ship_data = ship_data[ship_input]
	ship_data = ship_data.to_frame()
	ship_data = ship_data.rename(columns={'Ship Mode': 'Mode', 'Ship Mode': 'Value'})
	ship_data.reset_index(inplace=True)
	# Build the pie chart 
	ship_fig = px.pie(ship_data, values='Value', names='Ship Mode')

	return ship_fig


# Callback for the bottom left scatter plot of delivery times by state
@app.callback(Output(component_id='del-plot', component_property='figure'),
				Input(component_id='del-input', component_property='value'))
def get_delivery_graph(del_input):
	if not del_input:
		return NULL

	del_data = data.copy()
	# Get the required dataset
	del_data = del_data[del_data['State'] == del_input]
	# build the figure
	del_figure = px.scatter(del_data, x='Order Date', y='Delivery Time')

	return del_figure


@app.callback(Output(component_id='sale-plot', component_property='figure'),
				Input(component_id='sale-input', component_property='value'))
def get_sales_graph(sale_input):
	if not sale_input:
		return NULL

	sale_data = data.copy()

	sale_data = sale_data.groupby(['Category', 'State'])['Sales'].sum().reset_index()
	sale_data = sale_data[sale_data['State']==sale_input]

	sale_fig = px.pie(sale_data, values='Sales', names='Category')

	return sale_fig


# Run the app
if __name__ == '__main__':
	app.run_server()