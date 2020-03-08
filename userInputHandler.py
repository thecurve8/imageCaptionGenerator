# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:22:22 2020

@author: Alexander

This script is used to get information from the user
"""

def askYesNo(question):
    """Asks a yes/no question to the user
     
    Parameters
    ----------
    question : str
        question to ask to the user

    Returns
    -------
    bool
        True if user said yes else False
    """ 

    answer=""
    while not(answer=="y" or answer=="n"):
        answer=input(question+" [y/n]:") 
    return True if answer=="y" else False

def askForFloat(question, minValue, maxValue):
    """Asks the user for a float
     
    Parameters
    ----------
    question : str
        question to ask to the user
    minValue : float
        minimum accepted value
    maxValue : float
        maximum accepted value

    Returns
    -------
    float
        float given by the user
    """ 

    while True:
        try:
            value=float(input(question))
        except ValueError:
            print("This is not a float")
        if(value<minValue or value>maxValue):
            print("The value has to be between {} and {}".format(minValue, maxValue))
        else:
            return value

def askForInteger(question, minValue, maxValue):
    """Asks the user for an int
     
    Parameters
    ----------
    question : str
        question to ask to the user
    minValue : int
        minimum accepted value
    maxValue : int
        maximum accepted value

    Returns
    -------
    int
        int given by the user
    """ 

    while True:
        try:
            value=int(input(question))
        except ValueError:
            print("This is not a number")
        if(value<minValue or value>maxValue):
            print("The value has to be between {} and {}".format(minValue, maxValue))
        else:
            return value  