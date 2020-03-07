# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:07:40 2020

@author: Alexander
"""
import os
import pickle

def getImages(filename):
    """Get a list of images filenames
    
    Parameters
    ----------
    filename : str
        path to the image filenames
     
    Returns
    -------
    list_images : list
        list of the image names 
    """  

    raw_descriptions=""   
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                raw_descriptions=f.read()
        except IOError:
            print("Could not read file {}".format(filename))
        list_images=raw_descriptions.split("\n")[:-1]    
        return list_images
    else:
        print("{} does not exist".format(filename))


def getFeatures(filename, list_images):
    """Get the dictionary of features for the selected images
    
    Parameters
    ----------
    filename : str
        path to the pickle file with the dictionary of features
    list_images : list
        list of image names
     
    Returns
    -------
    selectedFeatures : dict
        dictionary mapping image names to their features
    """  
    print(list_images[0:10])
    with open(filename, 'rb') as f:  
        featureDict = pickle.load(f)
    selectedFeatures={image: featureDict[image] for image in list_images}
    return selectedFeatures

def getDescriptions(filename, list_images):
    """Get the dictionary of descriptions with <start> and <end>
    
    Parameters
    ----------
    filename : str
        path to the file containing the clean descriptions
    list_images : list
        list of image names
     
    Returns
    -------
    selectedDescriptions : dict
        dictionary mapping image names to their descriptions
    """  
    
    with open(filename, 'r') as f:
        clean_descriptions=f.read()
    selectedDescriptions={}
    lines = clean_descriptions.split("\n")[:-1]
    for line in lines:
        part = line.split("\t") 
        image, description = part[0], part[1]
        if image in list_images:
            if image not in selectedDescriptions:
                selectedDescriptions[image]=[]
            description="<start> "+description+" <end>"
            selectedDescriptions[image].append(description)
    return selectedDescriptions

def getImagesFeaturesDescriptions(filenameImages, filenameFeatures, filenameDescriptions):
    """Get the list of images and the dictionaries with their corresponding Features and descriptions
    
    Parameters
    ----------
    filenameImages : str
        path to the file containing the image names
    filenameFeatures : str
        path to the file containing the features
    filenameDescriptions : str
        path to the file containing the clean descriptions
     
    Returns
    -------
    list_images : list
        list of the names of the selected images
    selectedFeatures : dict
        dictionary with the feature of every image
    selectedDescriptions : dict
        dictionary with the list of descriptions for every image 
        (<start> and <end> added to every descriptions)        
    """  
    
    list_images = getImages(filenameImages)
    selectedFeatures = getFeatures(filenameFeatures, list_images)
    selectedDescriptions = getDescriptions(filenameDescriptions, list_images)
    return list_images, selectedFeatures, selectedDescriptions