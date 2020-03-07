# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:12:23 2020

@author: Alexander
"""
import os
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.utils import plot_model

from settings import MAX_LENGTH_DESCRIPTION, TRAIN_VOCAB_SIZE, PATH_TRAIN_IMAGES, PATH_CLEAN_DESCRIPTIONS
from generatorHandler import getDefaultGenerator
from dataLoadingHandler import getDescriptions, getImages

# define the captioning model
def define_model(vocab_size, max_length):
    # features from the CNN model squeezed from 2048 to 256 nodes
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)
    # LSTM sequence model
    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)
    # Merging both models
    decoder1 = Add()([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)
    # tie it together [image, seq] [word]
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # summarize model
    print(model.summary())
#    plot_model(model, to_file='model.png', show_shapes=True)
    return model

def train_caption_model():
    model = define_model(TRAIN_VOCAB_SIZE, MAX_LENGTH_DESCRIPTION)
    epochs = 10
    listImages = getImages(PATH_TRAIN_IMAGES)
    descriptionDict = getDescriptions(PATH_CLEAN_DESCRIPTIONS, listImages)
    steps = len(descriptionDict)
    # making a directory models to save our models
    os.mkdir("models")
    for i in range(epochs):
        generator = getDefaultGenerator()
        model.fit_generator(generator, epochs=1, steps_per_epoch= steps, verbose=1)
        model.save("models/model_" + str(i) + ".h5")
 
def continueTraining(epochs, filename, alreadyTrained):
    model = load_model(filename)
    listImages = getImages(PATH_TRAIN_IMAGES)
    descriptionDict = getDescriptions(PATH_CLEAN_DESCRIPTIONS, listImages)
    steps = len(descriptionDict)
    # making a directory models to save our models
    for i in range(epochs):
        generator = getDefaultGenerator()
        model.fit_generator(generator, epochs=1, steps_per_epoch= steps, verbose=1)
        model.save("models/model_" + str(i+alreadyTrained) + ".h5")
    
#continueTraining(13, "models/model_1.h5", 2)
#train_caption_model()
        
if __name__ =="__main__":
    continueTraining(13, "models/model_1.h5", 2)   