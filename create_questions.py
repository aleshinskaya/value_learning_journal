
import os
import json
from dotenv import dotenv_values
from dotenv import load_dotenv
import google-api-python-client

# set some global variables
load_dotenv() 
global config
config = dotenv_values(".env")
# returns google API key
config['GOOGLE_KEY']

CUR_DIR = os.path.dirname(os.path.abspath(__name__))


# full path to data json with values 
journal_filename = '/Users/anna/Dropbox/AOI/MoralLearning/CodeSets/value_learning_journal/data/thoughts_output_sample.json'

# read in the json
try:
    with open(journal_filename, 'r') as file:
        this_data = json.load(file)
except:
    raise FileExistsError()


assert(this_data['values'])

# open a json file for output

# for each item, define question
these_items = this_data['values']
       
for item in these_items:
    print(item['value'])
    # pipe this into the question. 

# read in contrast items/foil items
# shuffle all the items (or ensure google forms does randomization)
       
# send this entire list to google forms API - create question on its basis