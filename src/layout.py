from dash import html, dcc

def create_layout(data, continent_data):
    return html.Div(
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