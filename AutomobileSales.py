#!/usr/bin/env python
# coding: utf-8
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]


app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'left', 'color': '#000000', 'font-size': '24px'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '24px'}
        )
    ]),
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select-year',
            value='Select-year',
            style={'width': '80%', 'padding': '3px', 'font-size': '24px'})
        ),
        html.Div([
            html.Div(id='output-container', className='chart-grid')
        ]) 
    ])


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'), 
        Input(component_id='select-year', component_property='value')
    ])
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                    yearly_rec, 
                    x='Year',
                    y='Automobile_Sales',
                    title="Average Automobile Sales fluctuation over Recession Period"
                )
            )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                
        R_chart2  = dcc.Graph(
            figure=px.bar(
                    average_sales,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title="Average Automobile Sales of different vehicles over Recession Period"
                )
            )
        
        exp_rec = recession_data.groupby('Vehicle_Type', as_index=False)['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertising Expenditure of different vehicles in the Recession Period'
            )
        )

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=R_chart1),
                    html.Div(children=R_chart2)
                ],
                style={'display': 'flex'}
            ),

            html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=R_chart3),
                    html.Div(children=R_chart4)
                ],
                style={'display': 'flex'}
            )
        ]
                        
    elif (input_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
                              
        yas = data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, 
                x='Year',
                y='Automobile_Sales'
            )
        )
            
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Year', 
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {0}'.format(input_year)
            )
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            values='Advertising_Expenditure', 
            labels='Vehicle_Type')
        )

        return [
            html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=Y_chart1), 
                    html.Div(children=Y_chart2)
                ],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=Y_chart3), 
                    html.Div(children=Y_chart4)
                ], 
                style={'display': 'flex'}
            )
        ]
        
    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
