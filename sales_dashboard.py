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


# Create a dash app
app = dash.Dash(__name__)

# Clear layout and don't display exceptions until callback
app.config.suppress_callback_exceptions = True

# Retrieve the data from the database
def get_data():
	conn = sqlite3.connect('sales.db')
	data = pd.read_sql_query("SELECT * FROM sales", conn)
	conn.close()
	return data
	






# Application layout
app.layout = html.Div(children=[

	html.H1('Sales Report'),
	html.Div([
			"Input: ",
			dcc.Input(id='input', value='Alabama', type='text')
			]),
	dcc.Graph(id='plot1')
])
	



@app.callback(Output(component_id='plot1', component_property='figure'),
				Input(component_id='input', component_property='value'))
def get_graph(state):
	# Get the data for the selected state
	df = get_data()
	data = df.groupby(['State', 'Segment'])['Profit'].sum().reset_index()
	data = data[data['State'] == 'Alabama']

	# Build the graph
	bar_fig = px.bar(data, x='Segment', y='Profit', title="{} Profit by Segment".format(state))

	return bar_fig






# Run the app
if __name__ == '__main__':
	app.run_server()