#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes filtered user tweet files from 'preprocessed_data_path', generates
embeddings, and writes output processed_data_path.

June, 2019
@author: Joshua Rubin
"""
import time
from get_config import (get_config, create_dir_if_not_there)
from tweetvalidator.data_processing import embed_tweets_from_directories
from tweetvalidator.models import RandomForestModel
from tweetvalidator import train_models

config = get_config()
create_dir_if_not_there(config['processed_data_path'])

start = time.time()
embed_tweets_from_directories(config['preprocessed_data_path'], 
                              config['processed_data_path'])


create_dir_if_not_there(config['eval_output_path'])

dir_args = {   'input_directory'  : config['processed_data_path'],
       'negative_input_directory' : config['processed_negative_data_path'],
               'output_directory' : config['eval_output_path']}


train_models(RandomForestModel(verbose=True),
            'embedding', **dir_args,
            file_prefix = 'random_forest_model')

end = time.time()
print(end - start) 