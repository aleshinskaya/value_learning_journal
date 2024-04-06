
import os
import json, jsonlines
import pandas as pd
from dotenv import dotenv_values
from dotenv import load_dotenv
import requests
import numpy as np
from scipy.spatial.distance import cdist
import random
import typer




# set some global variables
load_dotenv() 
global config
config = dotenv_values(".env")

# set current path
CUR_DIR = os.path.dirname(os.path.abspath(__name__))



class Embedding():
    def __init__ (self,items,attr_list_1 = [], attr_list_2 = [], model_name = "text-embedding-ada-002"):
       self.model_name = model_name
       self.items = items
       self.attr_list_1 = attr_list_1
       self.attr_list_2 = attr_list_2
       self.attr_vector_emb = []
       self.item_attr_projections = []
       self.item_embs = []
       
    def get_embedding(self,text):
        url = 'https://api.openai.com/v1/embeddings'
        headers = {
        "Content-Type": "application/json",
        "Authorization": config['OPENAI_API_KEY']
        }
        data = { 
            "input": text,
            "model": self.model_name
        }
        response = requests.post(url, headers=headers, json=data)
        
        return response.json()


    def get_attribute_vector(self):
        emb_high = pd.DataFrame()
        emb_low = pd.DataFrame()

        list1 = self.attr_list_1
        list2 = self.attr_list_2

        #loop through each attribute set and save the embeddings in two dataframes
        for a in range(len(list1)):
            #get embedding of the high, low, and compute difference
            this_emb = self.get_embedding(list1[a])
            emb_high.insert(loc=0,column=a,value=this_emb["data"][0]["embedding"])

        for b in range(len(list2)):
            #get embedding of the high, low, and compute difference
            this_emb = self.get_embedding(list2[b])
            emb_low.insert(loc=0,column=b,value=this_emb["data"][0]["embedding"])

        #get all differences
        vector_diff = pd.DataFrame()

        for a in range(len(list1)):
            for b in range(len(list2)):
                this_col = str(a)+'_'+str(b)
                vector_diff.insert(loc=0,column = this_col, value = emb_high[a] - emb_low[b])
            
        self.attr_vector_emb = vector_diff.mean(axis=1)
        

    def get_list_embeddings(self):
       
       item_embs = [self.get_embedding(i)["data"][0]["embedding"] for i in self.items]
       self.item_embs = item_embs

       return item_embs


    def get_projections(self):
   
        item_list = self.items    #list of items 
        self.get_attribute_vector()   #obtain attribute projections for those items
        attr_emb =  self.attr_vector_emb 
    
        assert(len(attr_emb)>0)
        assert(len(item_list)>0)

        item_projections = {}

        for item in item_list:
            # get embedding of item
            item_emb = self.get_embedding(item)["data"][0]["embedding"]
            # project it onto the attribute vector
            projection_attr = np.inner(np.array(item_emb),np.array(attr_emb))
            item_projections[item] = projection_attr

        self.item_attr_projections = item_projections
    

# function to query GPT via openai API
def promptGPT(prompt_message_list, gpt_temperature=0, debug=False):
    gpt_url = "https://api.openai.com/v1/chat/completions"
    gpt_headers = {
        "Content-Type": "application/json",
        "Authorization": config['OPENAI_API_KEY']
    }
    gpt_data = {
            "model": "gpt-3.5-turbo-1106", 
            # "model": "gpt-4-turbo-preview",
            "response_format": {"type": "json_object"}, # only works on 3.5-turbo-1106, 4 and above
            "temperature": gpt_temperature,
            "messages": prompt_message_list,
    }
    response = requests.post(gpt_url, headers=gpt_headers, json=gpt_data)    
    if(debug==True):
        output = response.json()
    else:
        output = response.json()['choices'][0]['message']['content']

    return output

def get_response_dict(system_prompt_content, user_prompt_content):
    system_prompt= {
            "role": "system",
            "content": system_prompt_content
        }

    user_prompt = {
        "role": "user",
        "content": user_prompt_content,
    }
    # print([system_prompt,user_prompt])

    response_dict = json.loads(promptGPT([system_prompt,user_prompt],0,False))
    return response_dict


def main(json_filename_list,data_path,subjID):

    agg_item_list = []
    agg_score_list = []

    # loop through files and create aggregate list of items and of scores 
    for json_filename in json_filename_list:      
        try:
            with open(data_path+json_filename, 'r') as file:
                this_data = json.load(file)
        except:
            raise FileExistsError()

        # figure out keys so we just get whatever exists here 
        key_list = list(this_data.keys())
        values_data = [this_data[x] for x in key_list]

        # add to big list of items 
        for v in values_data[0]:
            agg_item_list.append((v["item"]))
            agg_score_list.append((v["score"]))

    # make all items lowercase
    agg_item_list = [x.lower() for x in agg_item_list]

    # create a new Embeddings object
    E = Embedding(agg_item_list)

    agg_emb_list = [E.get_embedding(x)['data'] for x in agg_item_list]
    agg_emb_vectors = [np.array(x[0]['embedding']) for x in agg_emb_list]
    agg_emb_array=np.array(agg_emb_vectors)
    
    #create distance matrix on pure embeddings 
    n_item = len(agg_item_list)
    agg_emb_distance = np.full((n_item,n_item),np.nan)                               


    for i in range(len(agg_emb_array)):
        for j in range(i + 1, len(agg_emb_array)):

            ag1=np.reshape(agg_emb_array[i],(1,len(agg_emb_array[i])))
            ag2=np.reshape(agg_emb_array[j],(1,len(agg_emb_array[j])))
            agg_emb_distance[i,j] = cdist(ag1, ag2,'cosine')[0][0]

    assert(agg_emb_distance.shape == (n_item,n_item))

    indices = np.where((agg_emb_distance < 0.11) & (agg_emb_distance != np.nan ))
    close_pairs = [(agg_item_list[x], agg_item_list[y]) for (x,y) in zip(indices[0],indices[1])]
         
    #now collapse the items that were synonyms (in close items)
    for pair in close_pairs:
       
       # find where the duplicates occur
       inds_list = [] 
       these_scores = []
       for ind,item in enumerate(agg_item_list):
           if(item==pair[0] or item==pair[1]):
                inds_list.append(ind)
       these_scores = [agg_score_list[i] for i in inds_list]
       score_avg = np.mean(these_scores)

        #just pick one of the two for now
       keep_ind = random.choice(inds_list)
       inds_list.remove(keep_ind)
       rm_inds = inds_list      

        # the one we are keeping, maintain the label and replace w avg score
       agg_score_list[keep_ind] = score_avg

        # replace items to remove with nans
       for ind in rm_inds:
           agg_item_list[ind] = np.nan

    # create dataframe
    item_df = pd.DataFrame({'item': agg_item_list, 'score': agg_score_list})
    # remove rows with na
    item_df_clean = item_df.dropna()
    print(item_df_clean)

    output_filename = data_path+subjID+'.csv'
    item_df_clean.to_csv(output_filename, index=False)


if __name__ == "__main__":
    typer.run(main)



