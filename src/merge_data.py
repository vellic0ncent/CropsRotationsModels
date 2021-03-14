import pandas as pd
import os
import re
from functools import reduce

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

def merge_data(path):
    frames = []
    for file in get_files_by_path_to_dir(path)[0]:
        frame = pd.read_csv(file, sep=',')
        frames.append(frame)
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['centroid'],
                                                    how='outer'), frames)
    
    df_merged.columns = ['CODE_CULTU_2015', 'CODE_GROUP_2015','centroid',
                         'CODE_CULTU_2016', 'CODE_GROUP_2016'
                         'CODE_CULTU_2017', 'CODE_GROUP_2017'
                         'CODE_CULTU_2018', 'CODE_GROUP_2018'
                         'CODE_CULTU_2019', 'CODE_GROUP_2019']
    return df_merged
