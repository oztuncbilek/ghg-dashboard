import plotly.express as px

def create_country_pie_chart(filtered_data):
    return px.pie(
        filtered_data,
        names="Country",
        values="Contribution (%)",
        title="GHG Emissions by Selected Countries",
        hole=0.3,
    )

def create_continent_pie_chart(filtered_data):
    return px.pie(
        filtered_data,
        names="Region",
        values="Contribution (%)",
        title="GHG Emissions by Selected Continents",
        hole=0.3,
    )