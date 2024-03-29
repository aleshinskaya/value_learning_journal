
import os
import json, jsonlines
import pandas as pd
# from dotenv import dotenv_values
# from dotenv import load_doten

# set some global variables
# load_dotenv() 
# global config
# config = dotenv_values(".env")
# # returns google API key
# config['GOOGLE_KEY']
# set current path
CUR_DIR = os.path.dirname(os.path.abspath(__name__))


# full path to data json with values 
# json_filename_list = ['s00_text-e1_one_step_prompt_0.json','s00_text-e2_one_step_prompt_0.json']
# data_path = '/Users/anna/Dropbox/AOI/MoralLearning/CodeSets/value_learning_journal/data/'
# subjID='s00'

def main(json_filename_list,data_path,subjID):


    # read in each file in list and save to a list of items for writeout

    agg_item_list = []

    for json_filename in json_filename_list:
        # read in the json
        try:
            with open(data_path+json_filename, 'r') as file:
                this_data = json.load(file)
        except:
            raise FileExistsError()

    
        # do some validation of the structure
        values_data=this_data[1]
        assert(values_data['values'])

        # expected to be a list of items 
        vlist=values_data['values']

        # add to big list of items 
        for v in vlist:
            agg_item_list.append((v["item"]))



    # go through these and write the items out to a simple csv
    # Specify the  output file path
    output_filename = data_path+subjID+'.csv'

    df = pd.DataFrame(agg_item_list,columns=['item'])
    df.to_csv(output_filename, index=False)








    # # open a json file for output

    # # for each item, define question
    # these_items = this_data['values']
        
    # for item in these_items:
    #     print(item['value'])
    # pipe this into the question. 

# read in contrast items/foil items
# shuffle all the items (or ensure google forms does randomization)
       
# send this entire list to google forms API - create question on its basis