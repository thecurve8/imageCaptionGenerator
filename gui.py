# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:01:50 2020

@author: Alexander

This script is used to get a GUI where you can try trained models
of caption generators.

This script requires that you have already trained a model.

This script requires tkinter, PIL, tensorflow, numpy and pandas
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import Button, Label, BOTTOM
from PIL import ImageTk, Image
from random import randint
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import Xception
from model import testModel
from userInputHandler import askYesNo, askForInteger
from tokenizerHandler import getTokenizer
from settings import PATH_TOKENIZER, MAX_LENGTH_DESCRIPTION
from os import listdir
import numpy as np
import os
import pandas as pd

def main():
    """Initiates and runs the GUI
    """
    
    #load the trained model
    modelToLoad="model_14.h5"
    
    useDefault=askYesNo("Do you want to use the defaul model {}?".format(modelToLoad))
    
    #list all available models and asks user to select one
    if not(useDefault):
        availableModels = [f for f in listdir('./models/')]
        print("The models are:")
        numberAvailableModels=len(availableModels)
        for i in range(numberAvailableModels):
            print("{}. {}".format(i+1, availableModels[i]))
        modelNumber = askForInteger("Select the model you want to use: ", 1, numberAvailableModels)
        modelToLoad=availableModels[modelNumber-1]
    
    tokenizer=getTokenizer(PATH_TOKENIZER)
    model = load_model("models/model_14.h5")
    xception_model= Xception(weights='imagenet',
                           include_top=False,
                           pooling='avg')
    
    #initialise GUI
    top=tk.Tk()
    top.geometry('800x600')
    top.title('Image caption generator')
    top.configure(background='#e2e8e9')
    label=Label(top,background='#e2e8e9', font=('arial',15,'bold'))
    sign_image = Label(top)
    
    def predict_caption(file_path):
        """Classifies an image into a traffic sign class and shows prediction
        
        Parameters
        ----------
        file_path : str
            The file location of the image
        """
        
        global label_packed
        image = Image.open(file_path)
        image = image.resize((30,30))
        image = np.array(image)     
        image = np.reshape(image, (-1, 30, 30, 3))
        text=testModel(file_path, MAX_LENGTH_DESCRIPTION, model, tokenizer, xception_model)
        label.configure(foreground='#011638', text="Predicted caption: "+ text) 
                        
    def show_classify_button(file_path):
        """Displays the button used to clasify the image
        
            Parameters
            ----------
            file_path : str
                The file location of the image to be classified
            """

        classify_b=Button(top,text="Classify Image",command=lambda: predict_caption(file_path),padx=10,pady=5)
        classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
        classify_b.place(relx=0.79,rely=0.46)
        
    def upload_image():
        """Uploads any image from the user computer
        """            

        try:
            file_path=filedialog.askopenfilename()
            uploaded=Image.open(file_path)
            uploaded.thumbnail(((top.winfo_width()/2),(top.winfo_height()/2)))
            im=ImageTk.PhotoImage(uploaded)
            sign_image.configure(image=im)
            sign_image.image=im
            label.configure(text='')
            show_classify_button(file_path)
        except:
            pass
    
    def upload_random_image():
        """Uploads a random image from the Test dataset
        """  
        
        max_image=1000
        try:
            value = randint(0, max_image)
            
            with open("Flickr8k_text/Flickr_8k.testImages.txt", 'r') as f:
                all_test_images =f.read()
            list_all_test_images = all_test_images.split("\n")[:-1]
            name = list_all_test_images[value]
            
            file_path=os.path.join("Flicker8k_Dataset", name)

            uploaded=Image.open(file_path)
            uploaded.thumbnail(((top.winfo_width()),(top.winfo_height())))
            uploaded = uploaded.resize((250, 250), Image.ANTIALIAS)
            im=ImageTk.PhotoImage(uploaded)
            sign_image.configure(image=im)
            sign_image.image=im
            label.configure(text='')
            show_classify_button(file_path)
        except:
            print("error while loading random image")
            pass
    
    upload=Button(top,text="Upload an image not from Test dataset",command=upload_image,padx=10,pady=5)
    upload.configure(background='#795d66', foreground='white',font=('arial',10,'bold'))
    upload.pack(side=BOTTOM,pady=5)
    
    uploadRand=Button(top,text="Upload a random image from Test dataset",command=upload_random_image,padx=10,pady=5)
    uploadRand.configure(background='#5c7c5a', foreground='white',font=('arial',10,'bold'))
    uploadRand.pack(side=BOTTOM, pady=5)
    
    
    sign_image.pack(side=BOTTOM,expand=True)
    label.pack(side=BOTTOM,expand=True)
    heading = Label(top, text="Use trained Model for caption generation",pady=20, font=('arial',20,'bold'))
    heading.configure(background='#e2e8e9',foreground='#364156')
    heading.pack()
    top.mainloop()
    return

if __name__ == "__main__":
    main()



