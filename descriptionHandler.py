# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:25:27 2020

@author: Alexander

This script contains the function used to prepare the description and prepare the vocabulary
"""
import os
import string
from userInputHandler import askYesNo
from settings import PATH_DESCRIPTION

def get_raw_descriptions(filename):
    """Reads the raw descriptions
    
    Parameters
    ----------
    filename : str
        path to the raw descriptions
     
    Returns
    -------
    raw_descriptions : str
        content of the file with the raw descriptions
    """  
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                raw_descriptions=f.read()
        except IOError:
            print("Could not read file {}".format(filename))
    else:
        print("{} does not exist".format(filename))
    return raw_descriptions

def create_description_dictionary(filename):
    """Creates a dictionary with the descriptions
    
    Parameters
    ----------
    filename : str
        path to the raw descriptions
     
    Returns
    -------
    dictionary : dict
        dictionnary mapping every image to all the descriptions
    """  
    
    raw_descriptions=get_raw_descriptions(filename)
    dictionary={}
    lines = raw_descriptions.split('\n')[:-1]
    for line in lines:
        name, description = line.split('\t')
        name = name[:-2] #removing index of description (#1,#2,...)
        if name not in dictionary:
            dictionary[name]=[description]
        else:
            dictionary[name].append(description)
    return dictionary

def clean_descriptions(descriptions_dictionnary):
    """Cleans the descriptions in the description dictionary
    
    Removes all non letter characters, makes everything lowercase
    Removes all one letter words
    
    Parameters
    ----------
    descriptions_dictionnary : dict
        dictionnary mapping every image to all the descriptions
     
    Returns
    -------
    descriptions_dictionnary : dict
        dictionnary mapping every image to all the clean descriptions
    """  

    translate_table=str.maketrans("-", " ", string.punctuation)
    for image, description_list in descriptions_dictionnary.items():
        for i, description in enumerate(description_list):
            clean_description = description.split(" ")
            clean_description = [word.translate(translate_table) for word in clean_description]
            clean_description = [word.lower() for word in clean_description]
            clean_description = [word for word in clean_description if len(word)>1]
            
            clean_description = " ".join(clean_description)
            descriptions_dictionnary[image][i]=clean_description
    return descriptions_dictionnary
    
def create_vocabulary(clean_descriptions_dictionary):
    """Creates a set with all the words from all the descriptions
    
    Parameters
    ----------
    clean_descriptions_dictionnary : dict
        dictionnary mapping every image to all the clean descriptions
     
    Returns
    -------
    voc : set
        set with every word from eery description
    """  

    voc=set()
    for image, description_list in clean_descriptions_dictionary.items():
        for description in description_list:
            list_of_words = description.split(" ")
            voc.update(list_of_words)
    return voc

def create_clean_description_file(clean_descriptions_dictionary, filename):
    """Writes a file with the cleaned descriptions
    
    Parameters
    ----------
    clean_descriptions_dictionnary : dict
        dictionnary mapping every image to all the clean descriptions
    filename : str
        name of the file to write in
    """  

    description_list_to_write=[]
    for image, description_list in clean_descriptions_dictionary.items():
        for description in description_list:
            description_list_to_write.append(image+"\t"+description)
    descriptions_to_write="\n".join(description_list_to_write)
    
    if os.path.exists(filename):
        print("Warning: {} already exists.".format(filename))   
        overwrite=askYesNo("Do you want to overwrite the file?")
        if not(overwrite):
            return
    try:
        with open(filename, 'w') as f:
            f.write(descriptions_to_write)
    except IOError:
        print("Could not write file {}".format(filename))
        
def getVocabularyAndCreateFile(inputFilename, outputFilename):
    """Writes the clean description file and returns the vocabulary
    
    Parameters
    ----------
    inputFilename : str
        path to the raw description file
    outputFilename : str
        name of the file to write in
    
    Returns
    -------
    vocabulary : set
        set with all the words
    """  

    dictionary = create_description_dictionary(inputFilename)
    dictionary = clean_descriptions(dictionary)
    vocabulary = create_vocabulary(dictionary)
    create_clean_description_file(dictionary, outputFilename)
    return vocabulary
   

