import json


# define prompting functions which are imported for testing
# all prompts must take one argument for now, will fix that issue later

def PROMPT_1(entry):
  """

  """

  system_prompt_content = f"""You are an expert in using what humans write and say to infer what they value and do not value.\
    Below is a journal entry from the user. Among everything the user talks about, identify what items they consider most\
    desirable and high value and give them a score from 0 - 100, where 100 is the highest value. Also identify any items they\
    consider to be least desirable and low value, and give them a score from 0 - 100, where 0 denotes the lowest value.\
    Items with high value are often virtuous, high utility, and bring meaning or fulfillment to them and others.\
    Items with low value are immoral, low utility, and bring harm to themselves or others.\
    Your task is to identify everything that the user identifies as having either a particularly high value or a particularly low value.\
    Please identify at least 10 items. Return a list that includes all these items and their scores on a scale of 0 to 100, where 0 is the\
    lowest value and 100 is the highest value. You must respond with a JSON packet with your response:\
    1. values - list:\
    1. item - <string>: the item\
    2. score - <int>: that item's score"""

  system_prompt= {
        "role": "system",
        "content": system_prompt_content
    }
  user_prompt = {
      "role": "user",
      "content": json.dumps({"journal_entry": entry})
  }

  return [system_prompt, user_prompt]



def PROMPT_2(entry):

    system_prompt_content = f"""You are an expert in using what humans write and say to infer what they value and don’t value. Given the user’s journal entry, infer their values. Values are things a person finds virtuous, high utility, and brings meaning or fulfillment to the actor and others. Return a json with each value and a score for how important it is to the user on a scale of 0 to 100, where 100 denotes the items with the highest value possible. 1. values -  list:\
    1. item - <string>: the item\
    2. score - <int>: that item's score"""

    system_prompt= {
        "role": "system",
        "content": system_prompt_content
    }
    user_prompt = {
        "role": "user",
        "content": json.dumps({"journal_entry": entry})
    }
    return [system_prompt, user_prompt]




def PROMPT_3(entry):

    system_prompt_content = f"""You are an expert in using what humans write and say to infer what they value. Return a json list named values with your answer."""
    user_content = f"""What are my values according to this entry? Return each item as a json item in a list. {entry}"""
    

    system_prompt= {
        "role": "system",
        "content": system_prompt_content
    }
    user_prompt = {
        "role": "user",
        "content": user_content
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
    You must respond with a JSON packet with your response: 1. items - list:\
    1. item - <string>: the item. 2. score - <int>: that item's score"""

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
