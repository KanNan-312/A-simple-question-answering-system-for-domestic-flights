## About this project
This is the assignment from the course Natural Language Processing at HCMUT. The task is to build a simple question-answering system for domestic flights, using classic NLP techniques.

## Directory information
- **input**: including a *flight_database.txt* file for the flight database, a *lexicon.json* file for lexicon and a folder *queries* with 10 .txt query files.
- **models**: including 7 sub-modules
  - tokenizer: word tokenizer
  - dependency_parser: module that implements the dependency parser
  - grammatical_generator: module to generate grammatical relations from dependency relations
  - logical_generator: module to generate logical form from grammatical relations 
  - procedural_generator: module to generate procedural semantics from logical form
  - database_handler: module to make database queries from procedural semantics
  - utils: utility classes
- **output**: results for each query in the input folder

## Setting up
### Create and activate conda environment
``` conda create -n my_env python=3.7 ```\
``` conda activate my_env ```
### Install unidecode package
``` pip install unidecode ```

## Usage
To run the program: \
``` python main.py ```