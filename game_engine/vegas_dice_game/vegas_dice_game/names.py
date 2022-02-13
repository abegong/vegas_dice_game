import os
import random

dir_ = os.path.dirname(__file__)
filename = os.path.join(dir_, "scottish_names.txt")
with open(filename) as file_:
    names = file_.read().splitlines()

def generate_random_name():
    return random.choice(names)