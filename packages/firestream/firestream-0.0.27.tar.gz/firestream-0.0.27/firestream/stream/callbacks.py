#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:57:12 2022

@author: Mohammad Asim
"""

from tensorflow.keras.callbacks import Callback

class CustomCallback(Callback):

    def __init__(self, output_dir):

        self.output_dir = output_dir

    def on_train_begin(self, logs=None):

        model.save_weights(self.output_dir)

    def on_epoch_end(self, epoch, logs=None):

        model.save_weights(self.output_dir)