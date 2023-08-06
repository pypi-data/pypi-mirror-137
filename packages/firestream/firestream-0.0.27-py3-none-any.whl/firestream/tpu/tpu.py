#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 21:54:20 2022

@author: admin
"""

from kaggle_secrets import UserSecretsClient
from kaggle_datasets import KaggleDatasets
import tensorflow as tf

class TPU:
    
    def __init__(self, config):
        
        self.user_secrets = UserSecretsClient()
        self.user_credential = self.user_secrets.get_gcloud_credential()
        self.user_secrets.set_tensorflow_credential(self.user_credential)
        self.gcs_path = KaggleDatasets().get_gcs_path(config['input_root_dir'])
        self.config = config
        
    def connect(self):
        
        self.resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='')
        tf.config.experimental_connect_to_cluster(self.resolver)
        tf.tpu.experimental.initialize_tpu_system(self.resolver)
        print("All devices: ", tf.config.list_logical_devices('TPU'))
        
    def strategy(self):
        
        self.strategy = tf.distribute.TPUStrategy(self.resolver)