# -*- coding: utf-8 -*-
"""
Load .h5 model | Captcha resolver
"""

import keras
import os
from importlib import resources
import io

import inspect, os

def get_path():
    globalPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return globalPath


def _load_model():
    try:
        modelPath = '/model/captchaSolver.h5'
        try:
            with resources.open_binary('gimpysolver', modelPath) as model:
                ml = io.BytesIO(model.read())
                captcha_model = keras.models.load_model()
        except:
            globalPath = get_path()
            fullPath = globalPath + modelPath
            
            captcha_model = keras.models.load_model(fullPath)
        return captcha_model
    except Exception as err:
        print('Error while try to read model CaptchaSolver',err)
        return err