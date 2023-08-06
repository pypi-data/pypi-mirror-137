import json

def read_json(jsonfile):
  data = []
  with open(jsonfile) as f:
    data = json.load(f)
  return data

def write_json(content, filename):
  with open(filename, 'w') as outfile:
    json.dump(content, outfile) 

def add_bracket(ex):
  return " (" + ex + ")" if ex!=None else "" 

