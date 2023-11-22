from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

class Proposition:
  @abstractmethod
  def to_string(self):
    pass

@dataclass
class Variable(Proposition):
  var: str

  def to_string(self):
    return self.var
  
  def __eq__(self, v):
    return (self.var == v.var)

@dataclass
class Name(Proposition):
  variable: Variable
  value: str

  def to_string(self):
    return f"(NAME {self.variable.to_string()} '{self.value}')"

@dataclass
class WH(Proposition):
  variable: Variable
  value: str

  def to_string(self):
    return f"<WH {self.variable.to_string()} {self.value}>"


@dataclass
class BinaryProposition(Proposition):
  rel: str
  p1: Proposition
  p2: Proposition

  def to_string(self):
    return f"({self.rel} {self.p1.to_string()} {self.p2.to_string()})"

@dataclass
class FLIGHT(Proposition):
  variable: Variable

  def to_string(self):
    return f"(FLIGHT1 {self.variable.to_string()})"

@dataclass
class Conjunction(Proposition):
  p_list: List[Proposition]

  def to_string(self):
    elements = ''.join([p.to_string() for p in self.p_list])
    return f"(&{elements})"

class Printer:
  def __init__(self):
    pass

  def print_result(self, dependency_relations, grammatical_relations, logical_form, procedural_semantics,\
     query_results, out='output_0.txt'):
    with open(out, encoding='utf-8' ,mode='w') as f:
      # print dependency relations
      f.write("----Dependency relations----\n")
      for head, dependent, rel in dependency_relations:
        head_word = head[0]
        dependent_word = dependent[0]
        f.write(f"{rel}({head_word}, {dependent_word})\n")
      
      # print grammatical relations
      f.write("\n----Grammatical relations----\n")
      for rel, value in grammatical_relations:
        value_str = value if type(value) is str else value.to_string()
        f.write(f'(s1 {rel} {value_str})\n')
      
      # print logical form
      f.write("\n----Logical form----\n")
      logical_str = logical_form.print_result()
      f.write(logical_str)
      f.write('\n')

      # print procedural semantics
      f.write("\n----Procedural semantics----\n")
      semantics_str = procedural_semantics.print_result()
      f.write(semantics_str)
      f.write('\n')

      # print query result
      f.write("\n----Query results----")
      if type(query_results) is bool:
        out_str = 'Yes' if query_results else 'No'
        f.write('\n' + out_str)
      else:
        for result in query_results:
          f.write('\n' + ' '.join([x for x in result]))