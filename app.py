from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np 
import os

# Dash application
app = Dash(__name__, suppress_callback_exceptions=True)


# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths relative to the script
file1 = os.path.join(script_dir, 'data', 'EDGAR_2024_GHG_booklet_2024.xlsx')
file3 = os.path.join(script_dir, 'data', 'CLASS.xlsx')


# Load the Excel files
excel1 = pd.ExcelFile(file1)
excel3 = pd.ExcelFile(file3)

# Load GHG totals by country data
ghg_totals_by_country = pd.read_excel(excel1, sheet_name="GHG_totals_by_country")
# Load the Income data
wb_income_data = pd.read_excel(excel3, sheet_name="List of economies")


# Data preparation
data = pd.merge(ghg_totals_by_country, wb_income_data, how="left", left_on="EDGAR Country Code", right_on="Code")
data = data.iloc[:-4]  # Exclude last 4 rows

# Sum emissions across all years (1970–2023) for each country
year_columns = [int(year) for year in range(1970, 2024)]
data["Total Emissions"] = data[year_columns].sum(axis=1)

# Calculate total world emissions
total_world_emissions = data["Total Emissions"].sum()

# Calculate each country's percentage contribution
data["Contribution (%)"] = (data["Total Emissions"] / total_world_emissions) * 100

# Sort countries by their contribution
data = data.sort_values(by="Contribution (%)", ascending=False)

# Group by Region (Continent) and calculate total emissions
continent_data = data.groupby("Region", as_index=False)["Total Emissions"].sum()

# Calculate each continent's percentage contribution
continent_data["Contribution (%)"] = (continent_data["Total Emissions"] / continent_data["Total Emissions"].sum()) * 100

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Greenhouse Gas Emissions Analysis",
                    style={
                        "textAlign": "center",
                        "color": "#ffffff",
                        "backgroundColor": "#013220",
                        "padding": "20px",
                        "marginBottom": "30px",
                    },
                )
            ],
            style={"backgroundColor": "#f4f4f4"},
        ),
        html.Div(
            [
                # Left side with tabs
                html.Div(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="country",
                            children=[
                                dcc.Tab(label="By Country", value="country"),
                                dcc.Tab(label="By Continent", value="continent"),
                            ],
                        ),
                        html.Div(id="tab-content"),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                    },
                ),
              
                # Right Section: World Map
                html.Div(
                    [
                        html.H3(
                            "Global Greenhouse Gas Emissions",
                            style={'textAlign': 'center', 'marginBottom': '20px'}
                        ),
                        dcc.Graph(
                            id='ghg-world-map',
                            style={
                                'height': '550px',  # Larger height for the map
                                'width': '100%'    # Full width within the container
                            }
                        )
                    ],
                    style={
                        'width': '65%',  # Increased width for the map section
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'backgroundColor': '#ffffff',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
                        'marginLeft': '2%'
                    }
                )
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        ),
            # Footer section
            html.Div(
                "Created by Ozan Tuncbilek © January 2025 for Data Science Analyst Publications and visualisation team - Statistical Applications",
                style={
                    "textAlign": "center",
                    "color": "#ffffff",
                    "backgroundColor": "#013220",
                    "padding": "10px",
                    "marginTop": "30px",
                    "fontSize": "14px",
                },
            ),
    ],
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4'}
)

# Callback to update tab content
@app.callback(Output("tab-content", "children"), [Input("tabs", "value")])
def render_tab_content(tab):
    if tab == "country":
        return html.Div(
            [
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": country, "value": country} for country in data["Country"].head(50)],
                    value=data["Country"].head(10).tolist(),
                    multi=True,
                    placeholder="Select countries (max 15)",
                    style={"marginBottom": "20px"},
                ),
                dcc.Graph(id="country-pie-chart"),
            ]
        )
    elif tab == "continent":
        return html.Div(
            [
                dcc.Dropdown(
                    id="continent-dropdown",
                    options=[{"label": region, "value": region} for region in continent_data["Region"]],
                    value=continent_data["Region"].tolist(),
                    multi=True,
                    placeholder="Select continents",
                    style={"marginBottom": "20px"},
                ),
                dcc.Graph(id="continent-pie-chart"),
            ]
        )


# Callback to update country pie chart
@app.callback(Output("country-pie-chart", "figure"), [Input("country-dropdown", "value")])
def update_country_pie_chart(selected_countries):
    if not selected_countries:
        selected_countries = data["Country"].head(10).tolist()

    filtered_data = data[data["Country"].isin(selected_countries)]
    fig = px.pie(
        filtered_data,
        names="Country",
        values="Contribution (%)",
        title="GHG Emissions by Selected Countries",
        hole=0.3,
    )
    return fig


# Callback to update continent pie chart
@app.callback(Output("continent-pie-chart", "figure"), [Input("continent-dropdown", "value")])
def update_continent_pie_chart(selected_continents):
    if not selected_continents:
        selected_continents = continent_data["Region"].tolist()

    filtered_data = continent_data[continent_data["Region"].isin(selected_continents)]
    fig = px.pie(
        filtered_data,
        names="Region",
        values="Contribution (%)",
        title="GHG Emissions by Selected Continents",
        hole=0.3,
    )
    return fig

@app.callback(
    Output('ghg-world-map', 'figure'),
    [Input('tabs', 'value')]
)
def update_world_map(tab):
    # Logarithmic Transformation to normalize large values
    data['Log Emissions'] = data['Total Emissions'].apply(lambda x: np.log10(x + 1))  # Log base 10 transformation
    
    # Create the map
    fig = px.choropleth(
        data,
        locations='EDGAR Country Code',  # ISO codes
        locationmode='ISO-3',
        color='Log Emissions',  # Using log-transformed values
        hover_name='Country',
        hover_data={
            "Total Emissions": ":,.0f",  # Show raw emissions with thousand separators
            "Contribution (%)": ":.2f"  # Show percentage contribution
        },
        color_continuous_scale=[
            (0.0, "yellow"),
            (0.5, "orange"),
            (1.0, "red"),
        ],
        title='Global Greenhouse Gas Emissions (Log-Scaled)'
    )
    
    # Adjust layout for better aesthetics
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        coloraxis_colorbar=dict(
            title="Log Emissions (log10)",
            thickness=8,  # Slimmer legend
            len=0.35,     # Shorter legend
            titlefont=dict(size=10),  # Smaller font for the legend title
            tickfont=dict(size=8)     # Smaller font for the legend ticks
        ),
        margin={"r": 10, "t": 50, "l": 10, "b": 10},  # Tight margins
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)