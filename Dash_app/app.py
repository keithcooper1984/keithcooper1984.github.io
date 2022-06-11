#####################################################################
# Libraries

import dash
from dash import dcc, html
from dash.dependencies import Input, Output


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#####################################################################
# CSS
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

main_style = {
    'backgroundColor': colors['background'], 
    'font-family': 'sans-serif', 
    'textAlign': 'center',
    'color': colors['text']}

dropdown_style = {
    'backgroundColor': '#119DFF', 
    'font-family': 'sans-serif', 
    'textAlign': 'center',
    'color': 'black'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': 'black',
    'color': 'white',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

graph_style = {
    'plot_bgcolor' : colors['background'],
    'paper_bgcolor': colors['background'],
    'font_color' :colors['text'],
    'xaxis' : {'showgrid' : False}
}

graph_size = {
    'autosize' : False,
    'width' : 500,
    'height' : 500
}

################################################################################
# Data Analysis
df = pd.read_pickle('Cleaned_df')

################################################################################
# Group Products by state
def group_state_products(dataframe, count_or_cost, metric = 'sum'):
    """
    Will group dataframe by state and product, using specified metric to analyse (e.g. sum, mean etc.) 
    on either the 'Quantity Ordered' or 'Total Cost' columns
    
    """
    
    grouped_state = dataframe.groupby(['State', 'Price Category'])[count_or_cost].agg(metric)
    grouped_state.sort_index(level = 0, inplace = True)
    grouped_state = grouped_state.unstack(level = 1)
    
    grouped_state.rename(columns = {'High Value': 'High Value Item Sales', 'Low Value': 'Low Value Item Sales'}, inplace = True)
    
    return grouped_state

#################################################################################################
# Choropleth

state_data = group_state_products(df, 'Quantity Ordered')
state_data.reset_index(inplace=True)
state_data['Total Sales'] = state_data['High Value Item Sales'] + state_data['Low Value Item Sales']
state_geo = "./Raw_data/us-states.json"

map_fig = px.choropleth(state_data, locationmode='USA-states', locations='State', color='Total Sales',
                        color_continuous_scale="Viridis",
                        scope="usa")

map_fig.update_layout(**graph_style, geo_bgcolor=colors['background'], margin={"r":0,"t":0,"l":0,"b":0})

##################################################################################################
# Group Products by time

def group_products_time(dataframe, time_type):
    """
    Will group dataframe by product and by the length of time specified (time_type variable).
    Can be either month, weekday or hour.
    
    """
    
    time_options = {'Month':df['Order Date'].dt.month, 'Weekday':df['Order Date'].dt.weekday, 'hour': df['Order Date'].dt.hour}

    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 
              7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    days =   {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}

    grouped_product = dataframe.groupby(['Product', time_options[time_type]]).agg({'Total Cost':'sum'})
    grouped_product.sort_index(level = 1, inplace = True)
    grouped_product = grouped_product.unstack(level = 1)
    grouped_product.columns = grouped_product.columns.get_level_values(1)
    
    if time_type == 'Month':
        grouped_product.rename(columns = months, inplace = True)
    elif time_type == 'Weekday':
        grouped_product.rename(columns = days, inplace = True)

    return grouped_product

################################################################
# KPI Indicators

kpi_grouped = df.groupby(['Price Category', df['Order Date'].dt.month]).agg({'Total Cost':'sum'})
                
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 
          7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

kpi_grouped.sort_index(level = 1, inplace = True)
kpi_grouped = kpi_grouped.unstack(level = 0)
kpi_grouped.columns = kpi_grouped.columns.get_level_values(1)

kpi_grouped.rename(months, inplace = True)
kpi_grouped.rename(columns = {'High Value': 'High Value Item Sales', 'Low Value': 'Low Value Item Sales'}, inplace = True)
kpi_grouped['Total Sales'] = kpi_grouped['High Value Item Sales'] + kpi_grouped['Low Value Item Sales']

kpi_grouped.loc['Total'] = kpi_grouped.sum()

high_target = [2500000] * 12
high_target.append(sum(high_target))

low_target = [80000] * 12
low_target.append(sum(low_target))

kpi_grouped['High Target'] = high_target
kpi_grouped['Low Target'] = low_target

def kpi_gauge(in_value, target, title):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = in_value,
    mode = "gauge+number+delta",
    title = {'text': f"{title} Item Sales"},
    delta = {'reference': target},
    gauge = {'axis': {'range': [None,  target* 2]},
             'bar': {'color': "darkblue"},
             'steps' : [
                 {'range': [0, target], 'color': "red"},
                 {'range': [target, target * 2], 'color': "green"}],
             }))

    fig.update_layout(**graph_style, autosize=False,width=500,height=500)
    return fig

##############################################################################
# Dash Layout

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(style = main_style, children=[
    html.H1('Sales Results 2019'),
    html.Div('An Interactive Dashboard to Facilitate Strategic Decisions'),
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-KPI', children=[
        dcc.Tab(label='Key Performance Indications', value='tab-KPI', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sales vs Time', value='tab-TIME', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Product Sales', value='tab-PRODUCT', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sales Map', value='tab-MAP', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

########################################################################################
# Dash callbacks
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-KPI':
        return html.Div([
            html.H3('Key Performace Indicators 2019'), 
            html.P('Actual Figures are in blue, amount above or below target is shown underneath.'),  
            dcc.Dropdown(['January','February','March','April','May','June','July','August','September','October','November','December','Total'],
                'Total',
                id='time_unit',
                style = dropdown_style
            ),
            html.Div([
            dcc.Graph(id='graph-HIGH'),
            dcc.Graph(id='graph-LOW'),
            dcc.Graph(id='graph-TOTAL')
            ], style={'display': 'inline-flex'})
        ])
    elif tab == 'tab-TIME':
        return html.Div([
            html.H3('Sales by Time interval'),
            html.P('Click on product to include / exclude it. Double click to view only that item'),
            dcc.Dropdown(['Month', 'Weekday'],
                'Month',
                id='time_dropdown',
                style = dropdown_style
            ),
            dcc.Graph(id='graph-TIME')

        ])
    elif tab == 'tab-PRODUCT':
        return html.Div([
            html.H3('Product Sales by State'),
            html.P('Click on product to include / exclude it. Double click to view only that item'),
            dcc.Dropdown(['Unit Sales', 'Revenue'],
                'Revenue',
                id='count_cost_dropdown',
                style = dropdown_style
            ),
            dcc.Graph(id='graph_PRODUCT')
        ])
    elif tab == 'tab-MAP':
        return html.Div([
            html.H3('Amount of Sales by State'),
            html.P('Areas without colour received no sales'),
            dcc.Graph(id='graph_MAP',
                figure=map_fig)
        ])

@app.callback(Output('graph_PRODUCT', 'figure'),
              Input('count_cost_dropdown', 'value'))
def product_fig(metric):
    if metric == 'Unit Sales':
        states_grouped = group_state_products(df, 'Quantity Ordered')
    else: states_grouped = group_state_products(df, 'Total Cost')
    fig = px.bar(states_grouped)
    fig.update_layout( **graph_style, yaxis = {'showgrid' : True})
    return fig

@app.callback(Output('graph-TIME', 'figure'),
              Input('time_dropdown', 'value'))
def time_fig(time_unit):
    time_grouped = group_products_time(df, time_unit)
    fig = px.line(time_grouped.T)
    fig.update_layout( **graph_style, yaxis = {'showgrid' : False})
    return fig

@app.callback(
    Output('graph-HIGH', 'figure'),
    Output('graph-LOW', 'figure'),
    Output('graph-TOTAL', 'figure'),
    Input('time_unit', 'value'))
def kpi_graphs(month):
    high_target = kpi_grouped.loc[month]['High Target']
    low_target = kpi_grouped.loc[month]['Low Target']
    total_target = high_target + low_target

    high_value = kpi_grouped.loc[month]['High Value Item Sales']
    low_value = kpi_grouped.loc[month]['Low Value Item Sales']
    total_value = high_value + low_value

    high_fig = kpi_gauge(high_value, high_target, 'High Value')
    low_fig =  kpi_gauge(low_value, low_target, 'Low Value')
    total_fig = kpi_gauge(total_value, total_target, 'Total')

    return high_fig, low_fig, total_fig


###################################################################################
# Run App
if __name__ == '__main__':
    app.run_server(debug=True)