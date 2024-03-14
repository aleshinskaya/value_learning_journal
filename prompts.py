import json
import random

# define prompting functions which are imported for testing
# all prompts must take one argument for now, will fix that issue later

def PROMPT_1(entry,sys_prompt):
  """

  """

  system_prompt_content = sys_prompt

  system_prompt= {
        "role": "system",
        "content": system_prompt_content
    }
  user_prompt = {
      "role": "user",
      "content": json.dumps({"journal_entry": entry})
  }

  return [system_prompt, user_prompt]





# @title define prompt_rate
def prompt_rate(item_list, entry):


    #randomize the order of the list of items
    random.shuffle(item_list)


    system_prompt_content = f"""You are an expert in using what humans write and say to infer what they value and do not value.\
    Below is a journal entry from the user and a list of items. For each item, provide a score from 0-100, where 100 is the highest\
    value and 0 is the lowest value. Scores of high value mean that the item is virtuous, high utility, and brings meaning or\
    fulfillment to the actor and others. Scores of low value mean the item is immoral, low utility, and bring harm to the actor or others.\
    You must respond with a JSON with an entry called values: 1. values - list:\
    1. value - <string>: the item. 2. score - <int>: that value's score"""

    system_prompt= {
        "role": "system",
        "content": system_prompt_content
    }   
    # List actions to sort
    user_prompt = {
        "role": "user",
        "content": json.dumps({"items": item_list,
                                "journal_entry": entry})
    }

    return [system_prompt, user_prompt]
