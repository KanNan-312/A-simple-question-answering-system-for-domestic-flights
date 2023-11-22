from .utils import *

class LogicalForm:
  def __init__(self, query, body):
    self.query = query
    self.query_type = 'CHECK' if 'CHECK' in query else 'RETRIEVE'
    self.body = body
  
  def print_result(self):
    query_str = ''
    if self.query_type == 'CHECK':
      query_str = f"The {self.query['CHECK'].to_string()}"
    else:
      query_vars = []
      for query_param in self.query:
        query_vars.append(self.query[query_param])
      query_str = 'WH ' + ','.join([x.to_string() for x in query_vars])

    body_str = self.body.to_string()
    return f'{query_str}: {body_str}'
    

class LogicalFormGenerator:
  def __init__(self):
    self.relation_map = {
      'TO': 'DEST',
      'FROM': 'SOURCE',
      'IN-TIME': 'RUN-TIME',
      'AT-TIME': {
        'TO': 'ARRIVE-TIME',
        'FROM': 'DEPART-TIME'
      }
    }

  def gen(self, grammatical_relations):
    gm_relations_dict = {}
    for rel, value in grammatical_relations:
      # case QUERY relation
      if rel == 'QUERY':
        if rel not in gm_relations_dict:
          gm_relations_dict[rel] = [value]
        else:
          gm_relations_dict[rel].append(value)
      # other relations
      else:
        gm_relations_dict[rel] = value
    
    # PRED, LSUBJ and QUERY must be in the gm relations
    assert all([x in gm_relations_dict for x in ['QUERY', 'PRED', 'LSUBJ']])
    # one of IN-TIME, AT-TIME, FROM, TO must be in the gm relations
    assert any([x in gm_relations_dict for x in ['IN-TIME', 'AT-TIME', 'FROM', 'TO']])

    # generate logical form from grammatical relations
    logical_props = []
    flight_var = Variable('f')
    city_var = Variable('c')
    time_var = Variable('t')
    
    # lsubj relations
    lsubj = gm_relations_dict['LSUBJ']
    if type(lsubj) is WH:
      flight_var = lsubj.variable
      logical_props.append(FLIGHT(flight_var))

    elif type(lsubj) is Conjunction:
      flight_var = lsubj.p_list[0].variable
      logical_props += lsubj.p_list
    
    # to-loc, from-loc, and run-time
    for x in ['FROM', 'TO', 'IN-TIME']:
      if x in gm_relations_dict:
        rel = self.relation_map[x]
        p1 = flight_var
        p2 = gm_relations_dict[x]
        # if the value is <WH>, replace the argument with the variable name
        if type(p2) is WH:
          p2 = p2.variable
          if x == 'IN-TIME':
            time_var = p2
          else:
            city_var = p2
        
        logical_props.append(BinaryProposition(rel, p1, p2))

    # at-time
    if 'AT-TIME' in gm_relations_dict:
      rel = 'DEPART-TIME' if 'FROM' in gm_relations_dict else 'ARRIVE-TIME'
      p1 = flight_var
      p2 = gm_relations_dict['AT-TIME']
      # if the value is <WH>, replace the argument with the variable name
      if type(p2) is WH:
        p2 = p2.variable
        time_var = p2
      
      logical_props.append(BinaryProposition(rel, p1, p2))


    # logical body
    logical_body = Conjunction([p for p in logical_props])

    # logical query params
    logical_queries = {}
    # case yes no question
    if gm_relations_dict['QUERY'][0] == 'CHECK':
      logical_queries['CHECK'] = flight_var
    # case WH question
    else:
      for query_param in gm_relations_dict['QUERY']:
        if query_param == 'FLIGHT1':
          logical_queries['FLIGHT1'] = flight_var
        elif query_param == 'TIME1':
          logical_queries['TIME1'] = time_var
        elif query_param == 'CITY1':
          logical_queries['CITY1'] = city_var
    
    return LogicalForm(logical_queries, logical_body)
      

