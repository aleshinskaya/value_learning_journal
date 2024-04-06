
import create_questions
import os
import importlib
importlib.reload(create_questions)


CUR_DIR = os.path.dirname(os.path.abspath(__name__))


# json_filename_list = ['s00_e6n.json','s00_e7n.json','s00_e8n.json','s00_e9n.json']
json_filename_list = ['s00_e6p.json','s00_e7p.json','s00_e8p.json','s00_e9p.json']
data_path = CUR_DIR+'/data/test_002/'
subjID='s00'

create_questions.main(json_filename_list,data_path,subjID)