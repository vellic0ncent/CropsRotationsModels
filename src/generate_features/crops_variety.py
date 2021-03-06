import pandas as pd
import os
import re
from functools import reduce
import numpy as np
import pyproj
from geopy.geocoders import Nominatim

path = 'C:\\Users'

def get_files_by_path_to_dir(path):
    pattern_train = re.compile(r'train_\d{4}.csv')
    pattern_test = re.compile(r'test_\d{4}.csv')
    list_of_files = os.listdir(path)
    train, test, predict = [],[],[]
    for file in list_of_files:
        if pattern_train.match(file):
            train.append(file)
        elif pattern_test.match(file):
            test.append(file)
            
    return train,test

frames = []
for file in get_files_by_path_to_dir(path)[0]:
    frame = pd.read_csv(file, sep=',')
    year = re.compile('\d+').findall(file)
    frame['Year'] = year * len(frame.index)
    frames.append(frame)

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['centroid'],
                                            how='outer'), frames)

df_merged.columns = ['cult_2015', 'group_2015','centroid','year_2015',
                    'cult_2016', 'group_2016','year_2016',
                     'cult_2017', 'group_2017','year_2017',
                     'cult_2018', 'group_2018','year_2018',
                     'cult_2019', 'group_2019','year_2019',]

pattern = re.compile('cult_.*')
columnlust = [col for col in df_merged.columns if pattern.match(col)]
df_merged['rotation'] = list(zip(*[df_merged[col] for col in columnlust]))

pattern_coords = re.compile('\d+\.\d+')
df_merged['coordinates'] = df_merged['centroid'].apply(lambda x: pattern_coords.findall(x))
df_merged['coordinates_tuple'] = df_merged['coordinates'].apply(lambda x: tuple(x))

df_merged[['lamb_longitude','lamb_latitude']] = pd.DataFrame(df_merged.coordinates.tolist(),
                                                   index= df_merged.index)

input_coder = 2154
output_coder = 4326
proj = pyproj.Transformer.from_crs(input_coder,
                                       output_coder,
                                       always_xy=True)
def transform_coordinates(a):
    try:
        lamb_long,lamb_lat = a
        return list(proj.transform(lamb_long,lamb_lat))
    except:
        return 0

df_merged['ws_coordinates'] = df_merged['coordinates_tuple'].map(transform_coordinates)
df_merged['ws_coordinates_tuple'] = df_merged['ws_coordinates'].apply(lambda x: tuple(x))
df_merged[['longitude','latitude']] = pd.DataFrame(df_merged.ws_coordinates.tolist(),
                                                   index= df_merged.index)

def get_geolocator(x):
    return tuple([x[1],x[0]])
df_merged['ws_coordinates_geolocator'] = df_merged['ws_coordinates'].map(get_geolocator)

coords = ['latitude','longitude']
data['ws'] = list(zip(*[data[col] for col in coords]))

geolocator = Nominatim(user_agent="sample user", timeout=3)

def get_location_name(x):
    return geolocator.reverse(x)

metatcen_500 =[]
for el in metacenters_500:
    try:
        metatcen_500.append(get_location_name(el))
    except:
        break

def distance (p1, p2):
    return (geopy.distance.geodesic(p1,p2).km)

def get_neighbour(latlong, farmer):
    closest_distance = []
    for i in latlong:
        dist = list(map(lambda x: distance(i,x), latlong))
        min = dist.sort()
        closest_distance.append(farmer[dist.index(min[1])])
    return closest_distance
