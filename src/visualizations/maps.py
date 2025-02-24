import plotly.express as px
import numpy as np

def create_world_map(data):
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
            title=dict(text="Log Emissions (log10)", font=dict(size=10)),
            thickness=8,  # Slimmer legend
            len=0.35,     # Shorter legend
            tickfont=dict(size=8)  # Smaller font for the legend ticks
        ),
        margin={"r": 10, "t": 50, "l": 10, "b": 10},  # Tight margins
    )
    return fig