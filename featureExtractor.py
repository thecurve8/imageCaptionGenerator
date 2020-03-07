# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:47:37 2020

@author: Alexander
"""
import os
import numpy as np
import pickle
from tqdm import tqdm
from tensorflow.keras.applications.xception import preprocess_input, Xception
from os import listdir
from os.path import isfile, join
from PIL import Image
from userInputHandler import askYesNo
from settings import PATH_IMAGES_FOLDER

def getTrainFeatures(imageDirectory):
    """Get a dictionary with the features from Xception model
     
    Parameters
    ----------
    imageDirectory : str
        path to directory with all images

    Returns
    -------
    featureDict : dict
        dictionnary mapping every image to its features
    """ 

    inputShape = (299, 299)
    
    xception_model= Xception(weights='imagenet',
                               include_top=False,
                               pooling='avg')
    
    featureDict = {}
    if os.path.isdir(imageDirectory):
        onlyfiles = [f for f in listdir(imageDirectory) if isfile(join(imageDirectory, f))]
        for imageFile in tqdm(onlyfiles):
            try:
                imagePath=os.path.join(imageDirectory, imageFile)
                with Image.open(imagePath) as image:
                    image = image.resize(inputShape)
                    image = np.array(image)
                    image = np.expand_dims(image, axis=0)
                    image = preprocess_input(image)
                    feature = xception_model.predict(image)
                    featureDict[imageFile] = feature    
            except IOError:
                print("Error while reading images")
    else:
        print("{} does not exist.".format(imageDirectory))
    return featureDict

def saveTrainFeatures(imageDirectory, outputFile):
    """Get a dictionary with the features from Xception model and save it
     
    Parameters
    ----------
    imageDirectory : str
        path to directory with all images
    outputFile : str
        name of the file to be created
    """ 

    if os.path.exists(outputFile):
        print("Warning: {} already exists.".format(outputFile))   
        overwrite=askYesNo("Do you want to overwrite the file?")
        if not(overwrite):
            return
        
    featureDict=getTrainFeatures(imageDirectory)
    if featureDict: #check if not empty, empty dict evaluates to False
        try:
            with open(outputFile, 'wb') as f: 
                pickle.dump(featureDict, f)
        except IOError:
            print("Could not write the {} file.".format(outputFile))

if __name__ == "__main__":
    saveTrainFeatures(PATH_IMAGES_FOLDER, "features")


    