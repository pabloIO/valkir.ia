import sys
import os.path
import json 
# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# sys.path.append('../')
# import models.models as database
# from sqlalchemy.exc import IntegrityError
# from config.config import env

import numpy
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

def process_text(word_file, profile_file):
    ## FEATURES AS PARAGRAPHS OF TEXT
    with open(word_file, 'r') as words:
        word_data = [x for x in words]
    ## LABELS WITH PEOPLE PROFILES
    with open(profile_file, 'r') as profiles:
        profile_data = [y for y in profiles]
    # print(word_data, profile_data)
    assert len(word_data) == len(profile_data)
    print(len(word_data) == len(profile_data))
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(word_data, profile_data, test_size=0.1, random_state=42)

    print(features_train, features_test)

process_text('../local_data/texto_perfiles.csv', '../local_data/labels.csv')