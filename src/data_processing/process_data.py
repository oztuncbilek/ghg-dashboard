import pandas as pd
import numpy as np

def prepare_data(ghg_totals_by_country, wb_income_data):
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

    return data, continent_data