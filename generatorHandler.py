# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:45:46 2020

@author: Alexander

This script creates the generator which is used for feeding input and output during the train process
"""

import pickle
import numpy as np
from settings import PATH_TOKENIZER, PATH_FEATURES, PATH_CLEAN_DESCRIPTIONS, PATH_TRAIN_IMAGES, MAX_LENGTH_DESCRIPTION, TRAIN_VOCAB_SIZE
from tokenizerHandler import getTokenizer
from dataLoadingHandler import getDescriptions, getImages
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

def generateForOneImage(tokenizer, feature, descr_list, max_length, voc_size):
    """Generates all input and output for a selected image
     
    Parameters
    ----------
    tokenizer : Tokenizer
        tokenizer for the used word set
    feature : list
        list of the feature of the image
    descr_list : list
        list of all the clean descriptions with "start" and "end" for this image
    max_length : int
        max length in words of the description
    voc_size : int
        size of the vocabulary
        
    Returns
    -------
    three np.array :
        A list with the feature of the image reapeated
        A list of the beginning of the descriptions
        A list with the next word in the desciption
    """ 

    feature_list = []
    beginning_seq = []
    next_word = list()
    for desc in descr_list:
        sequence = tokenizer.texts_to_sequences([desc])[0]
        for i in range(1, len(sequence)):
            padded_seq = pad_sequences([sequence[:i]], maxlen=max_length)[0]
            cat_word = to_categorical([sequence[i]], num_classes=voc_size)[0]
            feature_list.append(feature)
            beginning_seq.append(padded_seq)
            next_word.append(cat_word)
    return np.array(feature_list), np.array(beginning_seq), np.array(next_word)

def generator(tokenizer, featuresDict, descriptionDict, max_length, voc_size):
    """Generates infinite sequence of inputs and outputs
     
    Parameters
    ----------
    tokenizer : Tokenizer
        tokenizer for the used word set
    featureDict : dict
        dictionary with features of the image
    descriptionDict : dict
        dictionary with list of all the clean descriptions with "start" and "end" for this image
    max_length : int
        max length in words of the description
    voc_size : int
        size of the vocabulary
        
    Returns
    -------
    three np.array :
        A list with the feature of the image reapeated
        A list of the beginning of the descriptions
        A list with the next word in the desciption
    """ 
    
    while True:
        for key, descr_list in descriptionDict.items():
            feature = featuresDict[key][0]
            feature_list, beginning_seq_list, next_word_list = generateForOneImage(tokenizer, feature, descr_list, max_length, voc_size)
            yield [feature_list, beginning_seq_list], next_word_list
 
def getDefaultGenerator():
    """Returns the default generator for training
        
    Returns
    -------
    g : generator
        the default generator for the train dataset
    """ 
    
    tokenizer = getTokenizer(PATH_TOKENIZER)
    with open(PATH_FEATURES, 'rb') as f:
        featuresDict = pickle.load(f)
    listImages = getImages(PATH_TRAIN_IMAGES)
    descriptionDict = getDescriptions(PATH_CLEAN_DESCRIPTIONS, listImages)
    g = generator(tokenizer, featuresDict, descriptionDict, MAX_LENGTH_DESCRIPTION, TRAIN_VOCAB_SIZE)
    return g    
