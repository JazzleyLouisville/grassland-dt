import pandas as pd, geopandas as gpd
from shapely.geometry import Point

# read GBIF
occ = pd.read_csv("data/raw/gbif_pollinators.csv",
                  usecols=["species", "decimalLatitude", "decimalLongitude"])
occ = occ.dropna()
g_occ = gpd.GeoDataFrame(
            occ,
            geometry=[Point(xy) for xy in zip(occ.decimalLongitude,
                                              occ.decimalLatitude)],
            crs="EPSG:4326"
        )

# read daily env (for now use long‑term mean)
env = pd.read_csv("data/processed/daily_env.csv")
env_mean = (env.groupby(["latitude","longitude"])
                .agg({"temp":"mean","precip":"mean","nitrogen":"mean"})
                .reset_index())
g_env = gpd.GeoDataFrame(
            env_mean,
            geometry=[Point(xy) for xy in zip(env_mean.longitude,
                                              env_mean.latitude)],
            crs="EPSG:4326"
        )

# nearest‑neighbour join (each occurrence gets env values)
joined = gpd.sjoin_nearest(g_occ, g_env, how="inner", distance_col="dist_km")
joined.to_csv("data/processed/pollinators_with_env.csv", index=False)
print("Wrote data/processed/pollinators_with_env.csv  →", joined.shape)
