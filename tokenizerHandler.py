# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:20:46 2020

@author: Alexander

This script is used to create the tokenizer
"""

from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from settings import PATH_CLEAN_DESCRIPTIONS, PATH_TOKENIZER, PATH_TRAIN_IMAGES
from dataLoadingHandler import getDescriptions, getImages

def fileToListOfAllDescriptions(filenameDescr, filenameImages):
    """Transforms the descriptions of a dictionary into a list
    
    Parameters
    ----------
    filenameDescr : str
        path to the file containing the descriptions
    filenameImages : str
        path to the file containing the image names
     
    Returns
    -------
    listOfAllDescriptions : list
        list with all descriptions
    """  
        
    list_images = getImages(filenameImages)
    descriptionDict = getDescriptions(filenameDescr, list_images)
    listOfAllDescriptions=[]
    for image, description_list in descriptionDict.items():
        for description in description_list:
            listOfAllDescriptions.append(description)
    return listOfAllDescriptions

def createTokenizer(filenameDescr, filenameImages):
    """Creates a tokenizer based on a dictionary with descriptions
    
    Parameters
    ----------
    filenameDescr : str
        path to the file containing the descriptions
    filenameImages : str
        path to the file containing the image names
     
    Returns
    -------
    tokenizer : Tokenizer
        resulting tokenizer
    """  
        
    listOfAllDescriptions = fileToListOfAllDescriptions(filenameDescr, filenameImages)
    tokenizer =Tokenizer()
    tokenizer.fit_on_texts(listOfAllDescriptions)
    return tokenizer

def saveTokenizer(filenameDescr, filenameImages, filenameTokenizer):
    """Creates and saves a tokenizer based on a dictionary with descriptions
    
    Parameters
    ----------
    filenameDescr : str
        path to the file containing the dictionary
    filenameTokenizer : str
        path to the file where the tokenizer will be created
    """  
    
    tokenizer = createTokenizer(filenameDescr, filenameImages)
    with open(filenameTokenizer, 'wb') as f:
        pickle.dump(tokenizer, f)
        
def getTokenizer(filenename):
    """Gets a saved tokeizer
    
    Parameters
    ----------
    filenameTokenizer : str
        path to the file where the tokenizer will be created
        
    Returns
    -------
    tokenizer : Tokenizer
        the saved Tokenizer
    """  
    
    with open(filenename, 'rb') as f:
        tokenizer = pickle.load(f)
    return tokenizer

#saveTokenizer(PATH_CLEAN_DESCRIPTIONS, PATH_TRAIN_IMAGES, PATH_TOKENIZER)
#t=getTokenizer(PATH_TOKENIZER)
#print(len(t.word_index)+1)