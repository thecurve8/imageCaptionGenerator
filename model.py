# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:12:23 2020

@author: Alexander
"""
import os
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.xception import preprocess_input, Xception

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from settings import MAX_LENGTH_DESCRIPTION, TRAIN_VOCAB_SIZE, PATH_TRAIN_IMAGES, PATH_CLEAN_DESCRIPTIONS, PATH_TOKENIZER
from generatorHandler import getDefaultGenerator
from dataLoadingHandler import getDescriptions, getImages
from tokenizerHandler import getTokenizer

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

def train_caption_model(epochs):
    model = define_model(TRAIN_VOCAB_SIZE, MAX_LENGTH_DESCRIPTION)
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
        
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
         if index == integer:
             return word
    return None

def testModel(filename, max_length, model, tokenizer, xception_model):
    try:
        image = Image.open(filename)
    except:
        print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
    image = image.resize((299,299))
    image = np.array(image)
    # for images that has 4 channels, we convert them into 3 channels
    if image.shape[2] == 4: 
        image = image[..., :3]
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    feature = xception_model.predict(image)
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([feature,sequence])
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
        out_text = in_text.split(" ")
        if out_text[-1] == "end":
            out_text = out_text[:-1]
        if out_text[0]=="start":
            out_text=out_text[1:]
    return " ".join(out_text)

def main(filename):
    tokenizer=getTokenizer(PATH_TOKENIZER)
    model = load_model("models/model_14.h5")
    xception_model= Xception(weights='imagenet',
                           include_top=False,
                           pooling='avg')
    print("now")
    text=testModel(filename, MAX_LENGTH_DESCRIPTION, model, tokenizer, xception_model)
    print(text)
    img = Image.open(filename)
    plt.imshow(img)


#main("Flicker8k_Dataset/3044500219_778f9f2b71.jpg")
#if __name__ =="__main__":
#    continueTraining(10, "models/model_4.h5", 5)   