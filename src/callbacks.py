from dash.dependencies import Input, Output
from dash import html, dcc
from src.visualizations.charts import create_country_pie_chart, create_continent_pie_chart
from src.visualizations.maps import create_world_map



def register_callbacks(app, data, continent_data):
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

    @app.callback(Output("country-pie-chart", "figure"), [Input("country-dropdown", "value")])
    def update_country_pie_chart(selected_countries):
        if not selected_countries:
            selected_countries = data["Country"].head(10).tolist()

        filtered_data = data[data["Country"].isin(selected_countries)]
        return create_country_pie_chart(filtered_data)

    @app.callback(Output("continent-pie-chart", "figure"), [Input("continent-dropdown", "value")])
    def update_continent_pie_chart(selected_continents):
        if not selected_continents:
            selected_continents = continent_data["Region"].tolist()

        filtered_data = continent_data[continent_data["Region"].isin(selected_continents)]
        return create_continent_pie_chart(filtered_data)

    @app.callback(Output('ghg-world-map', 'figure'), [Input('tabs', 'value')])
    def update_world_map(tab):
        return create_world_map(data)