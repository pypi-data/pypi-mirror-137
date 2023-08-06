#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:59:01 2022

@author: Mohammad Asim
"""

from tensorflow.keras import Model, Input
from tensorflow.keras.layers import concatenate
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau, RemoteMonitor
from firestream.stream.callbacks import CustomCallback

import matplotlib.pyplot as plt
import os

class Disaggregator():
    
    def __init__(self, name, stream, model, optimizer, output_dir='./'):
        
        """
            Initialize disaggregator
        """

        self.name = name
        self.model = model
        self.concat = concatenate
        self.stream = stream
        self.history = []
        self.output_dir = output_dir
        self.optimizer = optimizer
        self.appliances = self.stream.config['appliances']
        self.checkpoint = ModelCheckpoint(
            os.path.join(self.output_dir, self.name+'-'+self.optimizer['name']+'-'+'checkpoint.hdf5'), 
            monitor="val_loss", 
            verbose=1,
            save_weights_only=True, 
            save_best_only=True, 
            mode="min"
        )
        self.csv_logger = CSVLogger(
            os.path.join(self.output_dir, self.name+'-'+self.optimizer['name']+'.csv'), 
            separator=",", 
            append=False
        )
        self.reduce_lr = ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.85,
            patience=5,
            verbose=1,
            mode="min",
            min_delta=0.0001,
            cooldown=0,
            min_lr=0.000001
        )
        self.remote_monitor = RemoteMonitor(
            root="https://asimjlkj.free.beeceptor.com",
            path="/publish/epoch/end",
            field="data",
            headers=None,
            send_as_json=True,
        )

    def build(self):
        
        """
            Build disaggregator model
        """
        
        input_node = Input((self.stream.window_length, self.stream.input_width))
        output = [self.model(self.name+'_'+str(i), self.stream.window_length, self.stream.input_width)(input_node) for i in range(len(self.appliances))]
        if(len(output)>1):
            output = concatenate(output)
        self.model = Model(inputs=[input_node], outputs=output)
        self.model.compile(loss=self.stream.loss, optimizer=self.optimizer['optimizer'])
    
    def train(self):

        """
            Function to starting training 
        """
        
        self.history = self.model.fit(
            self.stream.train_dataset, 
            validation_data=self.stream.validation_dataset, 
            epochs=self.stream.epochs,
            callbacks=[self.checkpoint, self.csv_logger, self.reduce_lr, self.remote_monitor]
        )

    def plotter(self, training=True):

        """
            Plotter for training and evaluation results
        """
        if(training):
            plt.plot(self.history.history['loss'])
            plt.plot(self.history.history['val_loss'])
            plt.title('Loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            plt.show()