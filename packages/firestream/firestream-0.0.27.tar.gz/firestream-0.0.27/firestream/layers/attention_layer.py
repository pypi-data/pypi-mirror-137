
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 23:59:01 2022

@author: Mohammad Asim
"""

from tensorflow.keras.layers import Layer, Dense
import tensorflow as tf
import tensorflow.keras.backend as K

class AttentionLayer(Layer):

    def __init__(self, units):
        super(AttentionLayer, self).__init__()
        self.W = Dense(units, kernel_initializer='he_normal')
        self.V = Dense(1, kernel_initializer='he_normal')

    def call(self, encoder_output, **kwargs):
        score = self.V(K.tanh(self.W(encoder_output)))
        attention_weights = K.softmax(score, axis=1)
        context_vector = attention_weights * encoder_output
        context_vector = tf.reduce_sum(context_vector, axis=1)
        
        return context_vector

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'W'       : self.W,
            'V'       : self.V,
        })
        return config