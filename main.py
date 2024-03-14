import os
from dotenv import dotenv_values
from dotenv import load_dotenv
import json
import requests
# import re, io, ast
# import pandas as pd
# import numpy as np
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



def test_two_step(journal_filename: str, person_name: str = 'user', prompt_list: list= []):   
  """
  journal-filename: a full path to a single text file containing a journal entry
  person-name: optional, defaults to 'user'.
  prompt_list: a list of system prompt instructions that will be varied
  """
  split_fn = journal_filename.split('.')
  
  #read in the file
  try:
    with open(journal_filename, 'r') as file:
      this_entry = file.read()
  except:
      raise FileExistsError()

  n_prompt = 0
  #pass the entry to the selected prompt
  for this_p in prompt_list: 

    # call prompts with entry and this prompt to generate prompt text
    prompt_text = prompts.PROMPT_1(this_entry,this_p)
    # use this prompt to query GPT
    prompt_response = promptGPT_json(prompt_text,0.7)  
    # save response
    response_list=json.loads(prompt_response)  
    print(response_list)
    #pass to a second stage where these items get scored 
    next_prompt = prompts.prompt_rate(response_list["values"],this_entry)
    prompt_response = promptGPT_json(next_prompt,0.7)  
    # save final output
    this_response = json.loads(prompt_response)
    # outputs_dict = this_response["items"]
    # print(this_response)
    # save to json file
    outfile_name = split_fn[0]+ '_two_step_prompt_'+str(n_prompt)+'.json'      
    #output a datastructure wth the items and ratings
    write_json(outfile_name,this_response,this_p)
    n_prompt = n_prompt+1


def test_one_step(journal_filename: str, person_name: str = 'user', prompt_list: list= []):   
  """
  journal-filename: a full path to a single text file containing a journal entry
  person-name: optional, defaults to 'user'.
  prompt_list: a list of system prompt instructions that will be varied
  """
  split_fn = journal_filename.split('.')
  outfile_name = split_fn[0]+ '_one_step'+'.json'

  #read in the file
  try:
    with open(journal_filename, 'r') as file:
      this_entry = file.read()
  except:
      raise FileExistsError()

  n_prompt = 0
  #pass the entry to the selected prompt
  for this_p in prompt_list: 

    # call prompts with entry and this prompt to generate prompt text
    prompt_text = prompts.PROMPT_1(this_entry,this_p)
    # use this prompt to query GPT
    prompt_response = promptGPT_json(prompt_text,0.7)  
    # print(prompt_response)
    # save response
    response_list=json.loads(prompt_response)  
    outfile_name = split_fn[0]+ '_one_step_prompt_'+str(n_prompt)+'.json'      
    #output a datastructure wth the items and ratings
    write_json(outfile_name,response_list,this_p)
    n_prompt = n_prompt+1

    

  

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

def write_json(fname,jlist,prompt):
    
    jsonl_file =  open(fname, 'w') 

    d = {'prompt': prompt}
    jsonl_file.write(json.dumps(d)+ '\n')

    for dictionary in jlist['values']:
      jsonl_file.write(json.dumps(dictionary) + '\n')

    jsonl_file.close()






