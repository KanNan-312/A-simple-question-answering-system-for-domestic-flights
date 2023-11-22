from .utils import *
class ProceduralSemantics:
  def __init__(self, action, query_vars, literals):
    self.action = action
    self.query_vars = query_vars
    self.literals = literals
  
  def print_result(self):
    if self.action == 'CHECK':
      query_str = 'CHECK'
    else:
      query_str = 'PRINT-ALL ' + ' '.join([f'?{x.to_string()}' for x in self.query_vars])
    
    literals_str = ''
    for x in self.literals:
      lit_lst = [x]
      for v in self.literals[x]:
        if type(v) is Variable:
          lit_lst.append(f'?{v.to_string()}')
        else:
          lit_lst.append(v)
      
      lit_str = "({})".format(' '.join([v for v in lit_lst]))
    
      literals_str += lit_str
  
    return f'{query_str} {literals_str}'

class ProceduralSemanticsGenerator:
  def __init__(self):
    self.constant_map = {
      'ho chi minh': 'HCM',
      'ha noi': 'HN',
      'hue': 'HUE',
      'da nang': 'ĐN',
      'khanh hoa': 'KH',
      'hai phong': 'HP',
      'vietnam airline': 'VietnamAirline',
      'vietjet air': 'VietjetAir'
    }
    self.variable_alphabet_map = {
      'FLIGHT': ['f', 'a'],
      'DTIME': ['f', 'c', 't'],
      'ATIME': ['f', 'c' , 't'],
      'RUN-TIME': ['f', 'c', 'c', 't']
    }
  
  def get_variable(self, var_dict, prefix):
    if prefix not in var_dict:
      var_dict[prefix] = 0

    var_dict[prefix] += 1
    return prefix + str(var_dict[prefix])

  def gen(self, logical_form):
    # action to perform in the database
    action = 'CHECK' if logical_form.query_type == 'CHECK' else 'RETRIEVE'
    query_variables = []

    # init parameter list
    variables = {}
    for param in logical_form.query:
      var = logical_form.query[param]
      query_variables.append(var)
      prefix = var.to_string()[0]
      variables[prefix] = 1
    
    # initialize set of empty literals
    literals = {
      'FLIGHT': [None] * 2,
      'ATIME': [None] * 3,
      'DTIME': [None] * 3,
      'RUN-TIME': [None] * 4
    }

    # loop through each logical relations and store the necessary information
    logical_dict = {}
    for prop in logical_form.body.p_list:
      if type(prop) is FLIGHT:
        logical_dict['FLIGHT'] = prop
      elif type(prop) is Name:
        logical_dict['NAME'] = prop
      else:
        logical_dict[prop.rel] = prop
    
    ### use the information to fill in the literals' placeholder ###

    # if flight code exists, all the flight variable will be filled with the code constant
    if 'NAME' in logical_dict:
      flight_var = logical_dict['NAME'].value.upper()

    # flight code not exist, use the flight variable to fill in the placeholder(s)
    else:
      flight_var = logical_dict['FLIGHT'].variable
      literals['FLIGHT'][0] = flight_var
      # airline information
      if 'AIRLINE' in logical_dict:
        airline_name = logical_dict['AIRLINE'].p2.value
        literals['FLIGHT'][1] = self.constant_map[airline_name]

    # process flight source
    if 'SOURCE' in logical_dict:
      source_prop = logical_dict['SOURCE'].p2
      # if src is Name, fill in the database the constant, else fill in the variable
      if type(source_prop) is Name:
        source = self.constant_map[source_prop.value]
      else:
        source = source_prop
    
    # process flight destination
    if 'DEST' in logical_dict:
      dest_prop = logical_dict['DEST'].p2
      # fill the constant in case of Name and variable in case of variable
      if type(dest_prop) is Name:
        dest = self.constant_map[dest_prop.value]
      else:
        dest = dest_prop

    # if both source and dest appear, fill in the RUN-TIME literal
    if 'SOURCE' in logical_dict and 'DEST' in logical_dict:
      literals['RUN-TIME'][:3] = [flight_var, source, dest]
    
    # if either only source or dest appears, fill in the DTIME and ATIME separately
    elif 'SOURCE' in logical_dict:
      literals['DTIME'][:2] = [flight_var, source]
    
    elif 'DEST' in logical_dict:
      literals['ATIME'][:2] = [flight_var, dest]
    
    # fill in the time information
    if 'DEPART-TIME' in logical_dict:
      dtime_prop = logical_dict['DEPART-TIME'].p2
      # fill the constant if dtime_prop is Name, else fill the variable
      dtime = dtime_prop
      if type(dtime_prop) is Name:
        dtime = dtime_prop.value.upper()
      literals['DTIME'][0] = flight_var
      literals['DTIME'][2] = dtime

    if 'ARRIVE-TIME' in logical_dict:
      atime_prop = logical_dict['ARRIVE-TIME'].p2
      # fill the constant if atime_prop is Name, else fill the variable
      atime = atime_prop
      if type(atime_prop) is Name:
        atime = atime_prop.value.upper()
      literals['ATIME'][0] = flight_var
      literals['ATIME'][2] = atime
    
    # run time
    if 'RUN-TIME' in logical_dict:
      runtime_prop = logical_dict['RUN-TIME'].p2
      # fill the constant if runtime_prop is Name, else fill the variable
      runtime = runtime_prop
      if type(runtime_prop) is Name:
        runtime = runtime_prop.value.upper()
      literals['RUN-TIME'][0] = flight_var
      literals['RUN-TIME'][3] = runtime
    
    # filter out only the literals with not None values
    literals = {x:literals[x] for x in literals if any(literals[x])}
  
    # fill the unfilled placeholder with variables
    for x in literals:
      lit = literals[x]
      for idx in range(len(lit)):
        if lit[idx] is None:
          prefix = self.variable_alphabet_map[x][idx]
          lit[idx] = Variable(self.get_variable(variables, prefix))
  
    return ProceduralSemantics(action, query_variables, literals)




