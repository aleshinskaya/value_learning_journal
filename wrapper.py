
import os
import main 
import importlib
importlib.reload(main)



# full path to journal entry
journal_filename = '/Users/anna/Dropbox/AOI/MoralLearning/CodeSets/value_learning_journal/data/text-e1.txt'

# list of prompts 
p1 = f"""You are an expert in using what humans write and say to infer what they value and do not value. \
Below is a journal entry from the user. Among everything the user talks about, identify what items they consider most\
desirable and high value and give them a score from 0 - 100, where 100 is the highest value. Also identify any items they\
consider to be least desirable and low value, and give them a score from 0 - 100, where 0 denotes the lowest value.\
Items with high value are often virtuous, high utility, and bring meaning or fulfillment to them and others.\
Items with low value are immoral, low utility, and bring harm to themselves or others.\
Your task is to identify everything that the user identifies as having either a particularly high value or a particularly low value.\
Please identify at least 10 items. Return a list that includes all these items and their scores on a scale of 0 to 100, where 0 is the\
lowest value and 100 is the highest value. You must respond with a JSON packet with your response:
1. values - list:\
1. item - <string>: the item\
2. score - <int>: that item's score"""

p2 = f"""You are an expert in using what humans write and say to infer what they value and don’t value. Given the user’s journal entry, infer their values. Values are things a person finds virtuous, high utility, and brings meaning or fulfillment to the actor and others. Return a json with each value and a score for how important it is to the user on a scale of 0 to 100, where 100 denotes the items with the highest value possible.\
1. values -  list:\
1. item - <string>: the item\
2. score - <int>: that item's score"""


p3 = f"""You are an expert in using what humans write and say to infer what they value.
What are the user's values according to this journal entry? Return a json with each value. 1. values -  list:"""

p4 = f"""You are an expert in using what humans write and say to infer what they value and don’t value. \
Given the user’s journal entry, infer their values. Values are things a person finds virtuous, high utility,\
and brings meaning or fulfillment to the actor and others. Return a json with an entry called "values" with each value.\
1. values -  list:"""

p5 = f"""You are an expert in using what humans write and say to infer what they value and don’t value. Given the human's journal entries, infer their values. Values are things a person finds virtuous, high utility, and brings meaning or fulfillment to the actor and others. Return a json with an entry called "values" with each value. 1. values -  list."""
    

# there are two prompting methods - one step gets all the items and their scores in one step, two step splits them.
# prompt text should be organized accordingly

main.test_two_step(journal_filename,'user', [p3,p4,p5])
main.test_one_step(journal_filename,'user', [p1,p2])

