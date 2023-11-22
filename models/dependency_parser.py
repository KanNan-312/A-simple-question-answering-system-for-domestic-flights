class DependencyParser:
  def __init__(self):
    self.stack = list()
    self.buffer = list()

  def shift(self):
    # get the next word from buffer
    next_token = self.buffer.pop(0)
    # put that word onto the stack
    self.stack.append(next_token)

  def reduce(self):
    # reduce top element from stack
    self.stack.pop()

  def left_arc(self, relation):
    head = self.buffer[0]
    dependent = self.stack.pop()
    return (head, dependent, relation)
  
  def right_arc(self, relation):
    head = self.stack[-1]
    dependent = self.buffer.pop(0)
    self.stack.append(dependent)
    return (head, dependent, relation)
  
  def parse(self, tokens):
    relations = []
    # Initialize the parser
    for token in tokens:
      self.buffer.append(token)
    self.stack.append(("ROOT", "ROOT", "ROOT"))

    # start parsing
    while len(self.buffer) > 0:
      stack_word, stack_tag, _ = self.stack[-1]
      buffer_word, buffer_tag, _ = self.buffer[0]
      actions = self.step(stack_word, stack_tag, buffer_word, buffer_tag)
      
      for action, relation in actions:
        if action == "SHIFT":
          self.shift()
        elif action == "REDUCE":
          self.reduce()
        elif action == "LA":
          relations.append(self.left_arc(relation))
        elif action == "RA":
          relations.append(self.right_arc(relation))

    # empty the stack, buffer and return the relations
    self.stack = []
    self.buffer = []
    
    return relations

  def step(self, stack_word, stack_tag, buffer_word, buffer_tag):
    if stack_tag == "FLIGHT-N":
      if buffer_tag == "QDET":
        return [("RA", "query_flight"), ("REDUCE", None)]
      elif buffer_tag.find("-V") != -1:
        return [("LA", "nsubj")]
      elif buffer_tag == "FLIGHT-CODE":
        return [("RA", "nmod"), ("REDUCE", None)]
      elif buffer_tag == "AIRLINE-NAME":
        return [("RA", "airline"), ("REDUCE", None)]
      else:
        return [("SHIFT", None)]


    elif stack_tag == "CITY-N" and buffer_tag == "QDET":
      return [("RA", "query_city"), ("REDUCE", None), ("REDUCE", None)]

    elif stack_tag == "ROOT" and buffer_tag.find('-V') != -1:
      return [("RA", "root")]

    elif stack_tag.find('-V') != -1:
      if buffer_tag == "CITY-NAME":
        return [("RA", "to-loc"), ("REDUCE", None)] if stack_tag == "ARRIVE-V" else [("RA", "dobj"), ("REDUCE", None)]
      elif buffer_tag == "CITY-N":
        return [("RA", "dobj")]
      elif buffer_tag == "TIME":
        return [("RA", "time"), ("REDUCE", None)]
      elif buffer_tag == "WH-TIME":
        return [("RA", "query_time"), ("REDUCE", None)]
      elif buffer_tag == "AUX":
        return [("RA", "aux")]
      elif buffer_tag == "QUERY":
        return [("RA", "query")]
      else:
        return [("SHIFT", None)]

    # handle prepositions
    elif stack_tag == "P-TO" and buffer_tag in ["CITY-NAME", "CITY-N"]:
      return [("LA", "to-loc")]

    elif stack_tag == "P-FROM" and buffer_tag == "CITY-NAME":
      return [("LA", "from-loc")]

    elif stack_tag == "P-AT" and buffer_tag in ["TIME", 'WH-TIME']:
      return [("LA", "at-time")]

    elif stack_tag == "P-IN" and buffer_tag in ["TIME", 'WH-TIME']:
      return [("LA", "in-time")]

    elif stack_tag == "GIVE-SPECIFY" and buffer_tag.find('-V') != -1:
      return [("LA", "query_flight")]

    # no match, shift the buffer
    else:
      return [("SHIFT", None)]


    # if stack_tag == "FLIGHT-N" and buffer_tag == "QDET":
    #   return [("RA", "query_flight"), ("REDUCE", None)]
    # elif stack_tag == "FLIGHT-N" and buffer_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"]:
    #   return [("LA", "nsubj")]
    # elif stack_tag == "ROOT" and buffer_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"]:
    #   return [("RA", "root")]
    # elif stack_tag == "P-TO" and buffer_tag == "CITY-NAME":
    #   return [("LA", "to-loc")]
    # elif stack_tag == "P-FROM" and buffer_tag == "CITY-NAME":
    #   return [("LA", "from-loc")]
    # elif stack_tag in ["FLIGHT-V", "DEPART-V"] and buffer_tag == "CITY-NAME":
    #   return [("RA", "dobj"), ("REDUCE", None)]
    # elif stack_tag == "ARRIVE-V" and buffer_tag == "CITY-NAME":
    #   return [("RA", "to-loc"), ("REDUCE", None)]
    # elif stack_tag == "P-AT" and buffer_tag in ["TIME", 'WH-TIME']:
    #   return [("LA", "at-time")]
    # elif stack_tag == "P-IN" and buffer_tag in ["TIME", 'WH-TIME']:
    #   return [("LA", "in-time")]
    # elif stack_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"] and buffer_tag == "TIME":
    #   return [("RA", "time"), ("REDUCE", None)]
    # elif stack_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"] and buffer_tag == "WH-TIME":
    #   return [("RA", "query_time"), ("REDUCE", None)]
    # elif stack_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"] and buffer_tag == "QUERY":
    #   return [("RA", "query")]
    # elif stack_tag == "FLIGHT-N" and buffer_tag == "FLIGHT-CODE":
    #   return [("RA", "nmod"), ("REDUCE", None)]
    # elif stack_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"] and buffer_tag == "AUX":
    #   return [("RA", "aux")]
    # elif stack_tag == "GIVE-SPECIFY" and buffer_tag in ["FLIGHT-V", "ARRIVE-V", "DEPART-V"]:
    #   return [("LA", "query_flight")]
    # elif stack_tag == "FLIGHT-N" and buffer_tag == "AIRLINE-NAME":
    #   return [("RA", "airline"), ("REDUCE", None)]
    # elif stack_tag == "P-TO" and buffer_tag == "CITY-N":
    #   return [("LA", "to-loc")]
    # elif stack_tag == "FLIGHT-V" and buffer_tag == "CITY-N":
    #   return [("RA", "dobj")]
    # elif stack_tag == "CITY-N" and buffer_tag == "QDET":
    #   return [("RA", "query_city"), ("REDUCE", None), ("REDUCE", None)]
    # # no match
    # else:
    #   return [("SHIFT", None)]