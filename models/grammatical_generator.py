from .utils import *

class GrammaticalRelationGenerator:
  def __init__(self):
    pass

  def get_variable(self, var_dict, prefix):
    if prefix not in var_dict:
      var_dict[prefix] = 0

    var_dict[prefix] += 1
    return prefix + str(var_dict[prefix])

  def gen(self, dependency_relations):
    # dictionary to keep track of variables
    variables = {}

    # dictionary to keep the information from dependency relations
    dependency_dict = {}
    for head, dependent, rel in dependency_relations:
      if rel in ['to-loc', 'from-loc']:
        dependency_dict[rel] = head[2] if head[1] in ['CITY-NAME', 'CITY-N'] else dependent[2]
      elif rel in ['in-time', 'at-time']:
        dependency_dict[rel] = head[2]
      else:
        dependency_dict[rel] = dependent[2]

    # generate grammatical relations from dependency relations
    grammatical_relations = []
    # PRED
    if 'root' in dependency_dict:
      grammatical_relations.append(('PRED', dependency_dict['root']))
    
    # yes/no question
    if 'aux' in dependency_dict:
      grammatical_relations.append(('QUERY', 'CHECK'))
    # query question
    else:
      if 'query_flight' in dependency_dict:
        grammatical_relations.append(('QUERY', 'FLIGHT1'))
      if 'query_time' in dependency_dict:
        grammatical_relations.append(('QUERY', 'TIME1'))
      if 'query_city' in dependency_dict:
        grammatical_relations.append(('QUERY', 'CITY1'))

    # LSUBJ
    if 'nsubj' in dependency_dict:
      flight_sem = dependency_dict['nsubj']
      var = Variable(self.get_variable(variables, flight_sem[0].lower()))
      # query flight
      if 'query_flight' in dependency_dict:
        grammatical_relations.append(('LSUBJ', WH(var, flight_sem)))
      # flight with code
      elif 'nmod' in dependency_dict:
        flight_p = FLIGHT(var)
        name = dependency_dict['nmod']
        name_p = Name(var, name)
        grammatical_relations.append(('LSUBJ', Conjunction([flight_p, name_p])))
      # flight with airline
      elif 'airline' in dependency_dict:
        flight_p = FLIGHT(var)
        airline_name = dependency_dict['airline']
        airline_var = Variable(self.get_variable(variables, airline_name[0].lower()))
        name_p = Name(airline_var, airline_name)
        airline_p = BinaryProposition('AIRLINE', var, name_p)
        grammatical_relations.append(('LSUBJ', Conjunction([flight_p, airline_p])))

    
    # location
    if 'to-loc' in dependency_dict:
      loc_name = dependency_dict['to-loc']
      var = Variable(self.get_variable(variables, loc_name[0].lower()))
      if loc_name == 'CITY1' and 'query_city' in dependency_dict:
        grammatical_relations.append(('TO', WH(var, 'CITY1')))
      else:
        grammatical_relations.append(('TO', Name(var, loc_name)))

    if 'from-loc' in dependency_dict:
      loc_name = dependency_dict['from-loc']
      var = Variable(self.get_variable(variables, loc_name[0].lower()))
      if loc_name == 'CITY1' and 'query_city' in dependency_dict:
        grammatical_relations.append(('FROM', WH(var, 'CITY1')))
      else:
        grammatical_relations.append(('FROM', Name(var, loc_name)))

    # time
    if 'at-time' in dependency_dict:
      time = dependency_dict['at-time']
      var = Variable(self.get_variable(variables, 't'))
      if time != 'WH-TIME':
        grammatical_relations.append(('AT-TIME', Name(var, time)))
      else:
        grammatical_relations.append(('AT-TIME', WH(var, 'TIME1')))

    elif 'in-time' in dependency_dict:
      time = dependency_dict['in-time']
      var = Variable(self.get_variable(variables, 't'))
      if time != 'WH-TIME':
        grammatical_relations.append(('IN-TIME', Name(var, time)))
      else:
        grammatical_relations.append(('IN-TIME', WH(var, 'TIME1')))
    
    return grammatical_relations
