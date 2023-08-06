# -*- coding: utf-8 -*-
"""

"""

# Captcha solver

import keras
import os.path
import cv2
import PIL
import numpy as np
from . import MDL

class captcha_solver():
    """"
    Load this object with the Image path to resolve.
    The model load correctly with Images size 380,85 and can use .wrongDimension or .dimension variables
    to know it.
    The model has been trained with 4000 samples of the same captcha type.
    ACCURACY: 92% of accuracy.
    """
    
    def __init__(self,path=''):
        if os.path.exists(path):
            try:
                img = PIL.Image.open(path)
            except Exception as err:
                print(err)
            
            try:
                self.imgArray = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
            except Exception as err:
                print(err)
        
        self.path = path
        
        self.img = img
        self.dimension = self.img.size
        self.wrongDimension = False
        self.character = '4yp9nfgawm76edhv5b32r8kcxt' # letter target from model
        self.model = MDL._load_model() # load Captcha Model resolve
        
        
        # Verify Dimensions
        if self.dimension[0] !=380 or self.dimension[1]!=85:
            self.wrongDimension = True
        
    
    def resize(self):
        try:
            self.img = self.img.resize((380,85))
            self.img.save(self.path) # rewrite the file
            # Read again 
            try:
                self.img = PIL.Image.open(self.path)
            except Exception as err:
                print(err)
            
            try:
                self.imgArray = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
            except Exception as err:
                print(err)
            
            self.wrongDimension = False
            print('Resize!')
        except Exception as err:
            return print(err)
            
    
    def predict(self):
        """"
        If Image size is 380,85 so the model predict the captcha.
        """
        if self.wrongDimension is False:
            img = self.imgArray
            model = self.model
            character = self.character
            
            if img is not None: #image foud at file path
                img = img / 255.0 #Scale image
            else:
                print("Not detected");
        
            res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis])) #np.newaxis=1 
            #added this bcoz x_train 970*50*200*1
            #returns array of size 1*5*36 
            result = np.reshape(res, (5, 26)) #reshape the array
            k_ind = []
            probs = []
            for i in result:
                k_ind.append(np.argmax(i)) #adds the index of the char found in captcha
        
            capt = '' #string to store predicted captcha
            for k in k_ind:
                capt += character[k] #finds the char corresponding to the index
            return capt
        else:
            dimension = self.dimension
            print('Wrong image dimension detected, your size >>{}<< , please resize to (380,85)'.format(dimension))
            

        
    