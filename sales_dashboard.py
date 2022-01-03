"""
	Sales Report Dashboard

"""

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3

# Using a basic CSS stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Clear layout and don't display exceptions until callback
app.config.suppress_callback_exceptions = True


# Use to retrieve sales data from the database
def get_data():
	conn = sqlite3.connect('sales.db')
	data = pd.read_sql_query("SELECT * FROM sales", conn)
	conn.close()
	return data


# Get the list of states from the db for the dropdown
conn = sqlite3.connect('sales.db')
STATES = pd.read_sql_query("SELECT * FROM states", conn)
STATES = sorted(list(STATES['State']))
conn.close()



# Application layout
app.layout = html.Div(children=[
	# Title
	html.H1('Sales Report'),
	# Row 1
	html.Div([
		# Graph 1
		html.Div([
				"Input: ",
				dcc.Dropdown(
						id='segment-input',
						options=[{'label': i, 'value': i} for i in STATES],
						placeholder="Select a state",
						style= {'width': 500, 'padding': 3}
						),
				dcc.Graph(id='segment-plot')
				], style= {'padding': 3}, className='six columns'),
		# Graph 2
		html.Div([
				"Input: ",
				dcc.Dropdown(
						id='input2',
						options=[{'label': i, 'value': i} for i in STATES],
						placeholder="Select a state",
						style= {'width': 500, 'padding': 3}
						),
				dcc.Graph(id='plot2')
				], style= {'padding': 3}, className='six columns')
	], className='twelve columns'),
	# Row 2
	html.Div([
		# Graph 3
		html.Div([
				"Input: ",
				dcc.Dropdown(
						id='input3',
						options=[{'label': i, 'value': i} for i in STATES],
						placeholder="Select a state",
						style= {'width': 500, 'padding': 3}
						),
				dcc.Graph(id='plot3')
				], style= {'padding': 3}, className='six columns'),
		# Graph 4
		html.Div([
							"Input: ",
				dcc.Dropdown(
						id='input4',
						options=[{'label': i, 'value': i} for i in STATES],
						placeholder="Select a state",
						style= {'width': 500, 'padding': 3}
						),
				dcc.Graph(id='plot4')
			], style= {'padding': 3}, className='six columns')
	], className='twelve columns')

])
	



@app.callback(Output(component_id='segment-plot', component_property='figure'),
				Input(component_id='segment-input', component_property='value'))
def get_graph(state):
	# Get the data for the selected state
	df = get_data()
	data = df.groupby(['State', 'Segment'])['Profit'].sum().reset_index()
	data = data[data['State'] == state]

	# Build the graph
	bar_fig = px.bar(data, x='Segment', y='Profit', title="{} Profit by Segment".format(state))

	return bar_fig






# Run the app
if __name__ == '__main__':
	app.run_server()