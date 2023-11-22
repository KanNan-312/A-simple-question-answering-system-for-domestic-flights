from .utils import *
class DatabaseHandler:
  def __init__(self, data_path):
    self.database = []
    self.attribute_map = {
      'FLIGHT': ['code', 'airline'],
      'DTIME': ['code', 'source', 'depart-time'],
      'ATIME': ['code', 'destination', 'arrive-time'],
      'RUN-TIME': ['code', 'source', 'destination', 'run-time']
    }
    self.__load_data(data_path)
  
  def __load_data(self, data_path):
    tmp_dct = {}
    with open(data_path, encoding='utf-8', mode='r') as f:
      for line in f:
        line = line.strip().replace('(','').replace(')','')
        splits = line.split()
        rel = splits[0]
        values = splits[1:]
        
        # initialize the record for each flight 
        code = values[0]
        if code not in tmp_dct:
          tmp_dct[code] = {}

        # map each value with corresponding attribute in the database
        record = tmp_dct[code]
        for idx, value in enumerate(values):
          attribute = self.attribute_map[rel][idx]
          if attribute in record:
            assert value == record[attribute]
          record[attribute] = value
        
    # create database
    self.database = list(tmp_dct.values())
  
  def check(self, conditions):
    # check if at least one record in the database satisfy all the conditions
    for record in self.database:
      match = True
      for attr, value in conditions:
        if record[attr] != value:
          match = False
          break
      # at lease one record match, return True
      if match:
        return True
    return False

  def print_all(self, query_attributes, conditions):
    # return all records in the database satisfying all the conditions
    results = []
    for record in self.database:
      match = True
      for attr, value in conditions:
        if record[attr] != value:
          match = False
          break
      # at the record matches, add it to the results
      if match:
        results.append([record[attr] for attr in query_attributes])

    return results


  def query(self, procedural_semantics):
    action = procedural_semantics.action
    query_vars = procedural_semantics.query_vars
    literals = procedural_semantics.literals

    query_attributes = [0] * len(query_vars)

    conditions = []

    for x in literals:
      for idx, val in enumerate(literals[x]):
        attribute = self.attribute_map[x][idx]

        # if the variable is the query variable, find the query attribute
        if type(val) is Variable and val in query_vars:
          query_idx = query_vars.index(val)
          if query_attributes[query_idx] == 0:
            query_attributes[query_idx] = attribute

        # fill in the conditions
        elif type(val) is str:
          conditions.append([attribute, val])
    
    if action == 'CHECK':
      return self.check(conditions)
    elif action == 'RETRIEVE':
      return self.print_all(query_attributes, conditions)

# DatabaseHandler('flight_database.txt')

      
      

  
