import sys
import os

# Projenin kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dash import Dash
from src.data_processing.load_data import load_ghg_totals_by_country, load_wb_income_data
from src.data_processing.process_data import prepare_data
from src.layout import create_layout
from src.callbacks import register_callbacks

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Load and process data
ghg_totals_by_country = load_ghg_totals_by_country()
wb_income_data = load_wb_income_data()
data, continent_data = prepare_data(ghg_totals_by_country, wb_income_data)

# Set the layout
app.layout = create_layout(data, continent_data)

# Register callbacks
register_callbacks(app, data, continent_data)

server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)