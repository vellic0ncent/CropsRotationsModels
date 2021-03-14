import generate_features.culture_culture_code_encoding.provide_culture_and_culture_group_encodings as provide_culture_and_culture_group_encodings
from shapely.geometry import Point, Polygon
import geopandas as gpd
import shapely.wkt


def rotation_length(row):
    length = row.drop_duplicates().shape[0]
    return length

def rotation_count(row):
    count = row.value_counts().min()
    return count

def geodata_classification(df, geojson_path):
    cdf = df[['centroid']]
    cdf['wgs84'] = gpd.GeoSeries.from_wkt(cdf['centroid'], crs='epsg:2154').to_crs('epsg:4326')
    fr_phz = gpd.read_file(f'{geojson_path}/FR_PHZ.geojson')
    cdf = gpd.GeoDataFrame(cdf, geometry='wgs84', crs='EPSG:4326')
    cdf = gpd.sjoin(cdf, fr_phz, op='within')
    cdf.drop(['pm_icon', 'index_right'], axis=1, inplace=True)
    kg = gpd.read_file(f'{geojson_path}/eur_kg.geojson')
    cdf = gpd.sjoin(cdf, kg, op='within')
    cdf.drop(['index_right', 'Shape_Leng', 'Shape_Area', 'pnm'], axis=1, inplace=True)
    fr_ff = gpd.read_file(f'{geojson_path}/FR_ff.geojson')
    cdf = gpd.sjoin(cdf, fr_ff, op='within')
    cdf.drop(['index_right', 'pm_icon'], axis=1, inplace=True)
    return cdf

def attach_features(df):
    provide_culture_and_culture_group_encodings(df)
    df['RotationLength'] = df.apply(rotation_length, axis=1)
    df['RotationCount'] = df.apply(rotation_count, axis=1)
    cdf = geodata_classification(df, 'geojson')
    df = df.merge(cdf, on='centroid')
    return df

