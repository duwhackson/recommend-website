import numpy as np
import pandas as pd

def load_data():
    big = pd.read_csv('base.csv')
    small = pd.read_csv('base.csv')
    return big,small


