# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Récupérer les valeurs uniques de la colonne 'Fruits'
launch_sites = spacex_df['Launch Site'].unique()

# Créer les options pour le Dropdown
# options_sites = [{'label': 'All Sites', 'value': 'ALL'}, {'label': site, 'value': site} for site in launch_sites]
options_sites = [{'label': 'All Sites', 'value': 'ALL'}]

for site in launch_sites:
    options_sites.append({'label': site, 'value': site}) 

print(options_sites)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown', 
                                                options= options_sites,
                                                value='ALL',
                                                placeholder="Search",
                                                searchable=True),
                                html.Hr(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Hr(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(
                                            id='payload_slider',
                                            min=min_payload,
                                            max=max_payload,
                                            value=[min_payload, max_payload],
                                            step=1000,
                                            marks={min_payload: '0',
                                                    max_payload: '100'},
                                            )),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    #filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Success Rate')
        return fig
    else:
        fig = px.pie(filtered_df, 
        #values='class', 
        names = 'class', 
        title='Success Rate of ' + entered_site)
        return fig        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input(component_id='site_dropdown', component_property='value'), 
    Input(component_id="payload_slider", component_property="value")
)
def update_scatter_plot(site, payload):
    # Filtrer les données en fonction de la valeur du slider
    #filtered_df = df[df['size'] >= size_threshold]
    #filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] >= size_threshold]
    
    if site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        size='Payload Mass (kg)',
        title='Correlation between Payload and success ' + site + ' From ' + str(payload[0]) + '  to ' + str(payload[1]),
        labels={'x': 'Axe X', 'y': 'Axe Y'},
        color="Booster Version Category"
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
