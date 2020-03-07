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
