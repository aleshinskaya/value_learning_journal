import json
import random

# define prompting functions which are imported for testing
# all prompts must take one argument for now, will fix that issue later

def prompt_basic(entry,system_prompt_content):
  """

  """

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
def prompt_rate(item_list, entry, system_prompt_content):


    #randomize the order of the list of items
    random.shuffle(item_list)

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
