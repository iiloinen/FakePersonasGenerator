import pandas as pd
from ctgan import CTGAN
import pickle

def generateWithCTGAN(sampleCount):
    model_filename = 'server\ctgan_model.pkl'
    with open(model_filename, 'rb') as file:
        loaded_model = pickle.load(file)
        synthetic_data = loaded_model.sample(sampleCount, condition_column={"Wiek *": lambda x: x >= 18})

    return synthetic_data