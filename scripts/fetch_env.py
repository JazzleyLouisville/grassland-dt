# scripts/fetch_env.py
from copernicus import data_processing        # ⬅ correct name
from soilgrids import data_processing as sg   # ⬅ for soil data
import pandas as pd

sites = pd.read_csv("data/reference_sites.csv")

# Weather
data_processing(
    years=[2022],                       # one recent year
    months=[6, 7, 8],                  # optional: June‑August only
    coordinates_list=sites.to_dict("records"),
    final_time_resolution="daily",     # ⬅ daily means
    download_whole_area=True,          # keep default (single tile)
    target_folder="data/raw/weather"
)

# Soil
for row in sites.to_dict("records"):
    sg(row, file_name=f"data/raw/soil/{row['site_id']}_soil.txt")
