#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:57:12 2022

@author: Mohammad Asim
"""

import tensorflow as tf

class Input():
    
    def __init__(self, config, window_length=1, shuffle=False, shuffle_buffer=1024, thresh=800, normalize=True):
        
        """
            Initialize input stream
        """

        self.train_dataset = config['train']['paths'] if 'train' in config.keys() and 'paths' in config['train'].keys() else None
        self.validation_dataset = config['validation']['paths'] if 'validation' in config.keys() and 'paths' in config['validation'].keys() else None
        self.train_batch_size = config['train']['batch_size'] if 'train' in config.keys() and 'batch_size' in config['train'].keys() else 32
        self.validation_batch_size = config['validation']['batch_size'] if 'validation' in config.keys() and 'batch_size' in config['validation'].keys() else 32
        self.data_type = config['data_type'] if 'data_type' in config.keys() else 'tfrecord'
        self.shuffle = shuffle
        self.window_length = window_length
        self.thresh = thresh
        self.normalize=normalize
        self.shuffle_buffer = shuffle_buffer
        self.config = config
        self.input_width = len(config['input_features']) if 'input_features' in config.keys() else 1
        self.output_width = len(config['appliances']) if 'appliances' in config.keys() else 1
        self.epochs=config['epoch'] if 'epoch' in config.keys() else 5
        self.loss=config['loss'] if 'loss' in config.keys() else 'mse'
        self.optimizer = config['optimizer'] if 'optimizer' in config.keys() else 'adam'
        self.lr = config['lr'] if 'lr' in config.keys() else None
        self.dataset()
        self._prepare_features()

    def dataset(self):

        """
            Build source data generator
        """
        
        if(type(self.train_dataset) in [list, tuple]):
        
            if(self.data_type=='tfrecord'):
                self.train_dataset = tf.data.TFRecordDataset(self.train_dataset, num_parallel_reads=tf.data.AUTOTUNE)
                
        else:
            raise TypeError("Only list, tuple are allowed")
            
        if(type(self.validation_dataset) in [list, tuple]):
            
            if(self.data_type=='tfrecord'):
                self.validation_dataset = tf.data.TFRecordDataset(self.validation_dataset, num_parallel_reads=tf.data.AUTOTUNE)
            
        elif(self.validation_dataset is not None):
            raise TypeError("Only list, tuple are allowed")
            
    def build(self):

        """
            Build input stream pipeline configurations
        """

        if(self.train_dataset is not None):
            
            if(self.data_type=='tfrecord'):
                self.train_dataset = self.train_dataset.map(self._parse_tf_record, num_parallel_calls=tf.data.AUTOTUNE)
            
            else:
                raise DatasetType('This version only supports tfrecord format')
            
            if(self.shuffle):
                self.train_dataset = self.train_dataset.shuffle(self.shuffle_buffer)
            
            self.train_dataset = self.train_dataset.batch(self.train_batch_size*self.window_length, drop_remainder=True)
            self.train_dataset = self.train_dataset.map(self._reshape_train, num_parallel_calls=tf.data.AUTOTUNE)
            self.train_dataset = self.train_dataset.cache()
            self.train_dataset = self.train_dataset.prefetch(tf.data.AUTOTUNE)

        if(self.validation_dataset is not None):
            
            if(self.data_type=='tfrecord'):
                self.validation_dataset = self.validation_dataset.map(self._parse_tf_record, num_parallel_calls=tf.data.AUTOTUNE)
            
            if(self.shuffle):
                self.validation_dataset = self.validation_dataset.shuffle(self.shuffle_buffer)
            
            self.validation_dataset = self.validation_dataset.batch(self.validation_batch_size*self.window_length, drop_remainder=True)
            self.validation_dataset = self.validation_dataset.map(self._reshape_validation, num_parallel_calls=tf.data.AUTOTUNE)
            self.validation_dataset = self.validation_dataset.cache()
            self.validation_dataset = self.validation_dataset.prefetch(tf.data.AUTOTUNE)
        
        return self
    def _prepare_features(self):
        self.features = {
            "timestamp": tf.io.FixedLenFeature([], tf.string), 
            "mains": tf.io.FixedLenFeature([], tf.float32),
            "diff": tf.io.FixedLenFeature([], tf.float32)
        }
        
        for name in self.config['input_features']:
            self.features[name] =  tf.io.FixedLenFeature([], tf.float32)

        for name in self.config['appliances']:
            self.features[name] =  tf.io.FixedLenFeature([], tf.float32)

    def _parse_tf_record(self, inp):

        """
            TFRecord parser
        """

        data = tf.io.parse_single_example(inp, self.features)
        
        if(self.normalize):
            return [data['mains']/self.thresh, data['diff']/self.thresh], [data[name]/self.thresh for name in self.config['appliances']]
        
        else:
            return [data['mains'], data['diff']], [data[name] for name in self.config['appliances']]
    
    def _reshape_train(self, mains, appliance):

        """
            Train batch reshaper
        """

        if(self.window_length is not None):
            return tf.reshape(mains, [self.train_batch_size, self.window_length, self.input_width]), tf.reshape(appliance, [self.train_batch_size, self.window_length, self.output_width])
        
        else:
            return tf.reshape(mains, [self.train_batch_size, self.input_width]), tf.reshape(appliance, [self.train_batch_size, self.output_width])

    def _reshape_validation(self, mains, appliance):

        """
            Validation batch reshaper
        """

        if(self.window_length is not None):
            return tf.reshape(mains, [self.validation_batch_size, self.window_length, self.input_width]), tf.reshape(appliance, [self.validation_batch_size, self.window_length, self.output_width])
        
        else:
            return tf.reshape(mains, [self.validation_batch_size, self.input_width]), tf.reshape(appliance, [self.validation_batch_size, self.output_width])
