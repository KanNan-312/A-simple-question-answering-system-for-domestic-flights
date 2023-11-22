from models import Tokenizer
from models import DependencyParser
from models import GrammaticalRelationGenerator
from models import LogicalForm, LogicalFormGenerator
from models import ProceduralSemantics, ProceduralSemanticsGenerator
from models import DatabaseHandler
from models import Printer
import glob, os

def main():
  tokenizer = Tokenizer("input\\lexicon.json")
  dependency_parser = DependencyParser()
  grammatical_generator = GrammaticalRelationGenerator()
  logical_generator = LogicalFormGenerator()
  procedural_generator = ProceduralSemanticsGenerator()
  database_handler = DatabaseHandler(data_path='input\\flight_database.txt')
  printer = Printer()

  for query_path in glob.glob('input\\queries\\*.txt'):
    query_n = query_path.split('\\')[-1].split('.')[0]
    # read query
    with open(query_path, encoding='utf-8', mode='r') as f:
      query = f.readlines()[0]

      # tokenizer
      tokens = tokenizer.tokenize(query)

      # dependency relations
      dependency_relations = dependency_parser.parse(tokens)

      # grammatical relations
      grammatical_relations = grammatical_generator.gen(dependency_relations)

      # logical form
      logical_form = logical_generator.gen(grammatical_relations)

      # procedural semantics
      procedural_semantics = procedural_generator.gen(logical_form)

      # database query
      query_results = database_handler.query(procedural_semantics)
      
      # print results
      printer.print_result(dependency_relations, grammatical_relations, logical_form, \
        procedural_semantics, query_results, f'output\\{query_n}.txt')


if __name__ == "__main__":
  main()