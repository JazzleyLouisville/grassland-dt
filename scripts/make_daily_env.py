# scripts/make_daily_env.py
from pathlib import Path
import xarray as xr
import pandas as pd

RAW_DIR = Path("weatherDataRaw")
OUTFILE = Path("data/processed/daily_env.csv")

# find the first (or latest) GRIB/NetCDF file
grib = sorted(RAW_DIR.glob("*.grib"))[0]      # adjust pattern if you chose netcdf

ds = xr.open_dataset(grib, engine="cfgrib")   # cfgrib handles ERA5 GRIB
# --- choose / rename variables you really need ---
ds = ds.rename({
    "t2m": "temp",                            # 2 m temperature
    "tp":  "precip"                           # total precipitation
})
# convert Kelvin to °C and scale precip from m to mm
ds["temp"] = ds["temp"] - 273.15
ds["precip"] = ds["precip"] * 1000

# average over 24 h to get daily means/sums
daily = ds.resample(time="1D").mean()         # .sum() for precip if you want totals
df = daily.to_dataframe().reset_index()

# add dummy nitrogen column (kg/ha) until you have real data
df["nitrogen"] = 50.0                         # constant placeholder
df["site_id"] = (
        "lat" + df["latitude"].round(3).astype(str) +
        "_lon" + df["longitude"].round(3).astype(str)
)
df.to_csv(OUTFILE, index=False)
print(f"Wrote {OUTFILE}")
