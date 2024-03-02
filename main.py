import os
from dotenv import dotenv_values
from dotenv import load_dotenv
import json,jsonlines
import requests
import re, io, ast
import pandas as pd
import numpy as np
import random
import importlib
import prompts
import typer
importlib.reload(prompts)

# set some global variables
load_dotenv() 
global config
config = dotenv_values(".env")
CUR_DIR = os.path.dirname(os.path.abspath(__name__))

# overview:
# input is a jounral entry and person's name
# output is a set of extracted values 

# prompts are stored in .py files in this directory

# list of prompts to test
PROMPTS_TO_TEST = ['prompts.PROMPT_1','prompts.PROMPT_2','prompts.PROMPT_3']

journal_filename = '/Users/anna/Dropbox/AOI/MoralLearning/CodeSets/value_learning_journal/data/text-e1.txt'

# provide full path here 
def main(journal_filename: str, person_name: str = 'user'):   
  """
  journal-filename: a full path to a single text file containing a journal entry
  person-name: optional, defaults to 'user'.
  """


  outfile_name = journal_filename+'.json'

  #read in the file
  try:
    with open(journal_filename, 'r') as file:
      this_entry = file.read()
  except:
      raise FileExistsError()


  #pass the entry to the selected prompt
  for this_p in PROMPTS_TO_TEST:      
    # this_p = PROMPTS_TO_TEST[2]  
    this_prompt_function  = eval(this_p)
    prompt_text = this_prompt_function(this_entry)
    prompt_response = promptGPT_json(prompt_text,0.7)  
    response_list=json.loads(prompt_response)
  
    #pass to a second stage where these items get scored 
    next_prompt = prompt_rate(response_list["values"],this_entry)
    prompt_response = promptGPT_json(next_prompt,0.7)  
    response_dict = json.loads(prompt_response)
    
    #output a datastructure wth the items and ratings
    write_json(outfile_name,response_dict["items"])

  

def promptGPT_json(prompt_message_list, gpt_temperature=0,debug=False):
  
  gpt_url = "https://api.openai.com/v1/chat/completions"
  gpt_headers = {
    "Content-Type": "application/json",
    "Authorization": config['OPENAI_API_KEY']
    }
  gpt_data = {
        "model": "gpt-3.5-turbo-1106",
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

def promptGPT4(prompt_message_list, gpt_temperature=0,debug=False):
  
  gpt_url = "https://api.openai.com/v1/chat/completions"
  gpt_headers = {
    "Content-Type": "application/json",
    "Authorization": config['OPENAI_API_KEY']
    }
  gpt_data = {
        "model": "gpt-4",
        "temperature": gpt_temperature,
        "messages": prompt_message_list,
    }

  response = requests.post(gpt_url, headers=gpt_headers, json=gpt_data)


  if(debug==True):
    output = response.json()
  else:     
    output = response.json()['choices'][0]['message']['content']

  return output

def write_json(fname,jlist):
    jsonl_file =  open(fname, 'w')  
    for dictionary in jlist:
        jsonl_file.write(json.dumps(dictionary) + '\n')

    jsonl_file.close()

if __name__ == "__main__":
    typer.run(main)






