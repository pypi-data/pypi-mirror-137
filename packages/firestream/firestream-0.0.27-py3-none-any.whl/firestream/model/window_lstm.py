#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 23:59:01 2022

@author: Mohammad Asim
"""

from tensorflow.keras.layers import Layer, Dense, Conv1D, LSTM, Bidirectional, Reshape
from firestream.layers.attention_layer import AttentionLayer

class WindowLSTM(Layer):
    
    def __init__(self, name, window_length, input_width):

        """
            Initialize the WindowGRU model 
        """
        # Inherit from tf.keras.Layer class
        super().__init__()

        # Define layers
        self.conv1d_0 = Conv1D(16, 4, activation='relu', input_shape=(window_length, input_width), padding="same", strides=1)
        self.bidirectional_lstm_0 = Bidirectional(LSTM(128,return_sequences=True,stateful=False), merge_mode='concat')
        self.bidirectional_lstm_1 = Bidirectional(LSTM(256,return_sequences=True,stateful=False), merge_mode='concat')
        self.attention = AttentionLayer(units=128)
        self.dense_0 = Dense(128, activation='tanh')
        self.dense_1 = Dense(window_length, activation='linear')
        self.reshape = Reshape((window_length, 1))
        self.build((None, window_length, input_width))
        
    def call(self, inputs, training=False):

        """
            Define call function to be used during forward
            propagation during training and inference
        """

        # Define flow sequence for forward propagation
        x = self.conv1d_0(inputs)
        x = self.bidirectional_lstm_0(x)
        x = self.bidirectional_lstm_1(x)
        x = self.attention(x)
        x = self.dense_0(x)
        x = self.dense_1(x)
        x = self.reshape(x)
        return x