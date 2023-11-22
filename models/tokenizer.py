import json
from unidecode import unidecode
import re

class Tokenizer:
  def __init__(self, lexicon_path=""):
    with open(lexicon_path, "r") as f:
      self.lexicon = json.load(f)
      self.blacklist =  ["cac", "co", " ma hieu", " nhung", " cua", "Thoi gian", "tp.", "TP.", "?", ",", "thoi gian", "hang hang khong"]

  def create_token(self, ngrams):
    skip = 1
    text = ngrams[0]
    tag = "NAME"
    sem = text

    # loop through the lexicon
    for entry in self.lexicon:
      p = re.compile('^' + entry['text'] + '$')
      found = False
      for idx, gram in enumerate(ngrams):
        if gram and p.match(gram):
          if entry["tag"].find("-V") != -1 and self.verb_found:
            continue
          else:
            found = True
            skip = idx + 1
            text = gram
            tag = entry["tag"]
            sem = entry["SEM"]
            if tag.find("-V") != -1:
              self.verb_found = True
            break
      # if any ngram found 
      if found:
        break
    
    # case tag is name, sem will be the same as the matched text
    if tag in ["NAME", "FLIGHT-CODE", "TIME", "AIRLINE-NAME", "CITY-NAME"]:
      sem = text

    return skip, text, tag, sem
  

  def preprocess_sentence(self, sentence):
    sentence = unidecode(sentence).strip().lower()
    # remove blacklist words/terms
    for x in self.blacklist:
      sentence = sentence.replace(x, '')
    
    # replace xx gio with HR format
    p = re.compile('([0-9]+) gio')
    match = p.search(sentence)
    if match is not None:
      t = match[1]
      replace = f'{int(t)}:00HR'
      sentence = p.sub(replace, sentence)
    
    return sentence
    

  def tokenize(self, sentence):
    self.verb_found = False
    sentence = self.preprocess_sentence(sentence)

    words = sentence.split()
    n_words = len(words)
    tokens = []

    idx = 0
    while idx < n_words:
      # pass 1,2 and 3 grams for searching
      unigram = words[idx]
      bigram = ' '.join(words[idx:idx+2]) if idx < n_words-1 else None
      trigram = ' '.join(words[idx:idx+3]) if idx < n_words-2 else None
      skip, token, pos_tag, sem = self.create_token([unigram, bigram, trigram])
      tokens.append((token, pos_tag, sem))
      idx += skip


    # remove "thanh pho" before city name
    idx = 0
    while idx < len(tokens)-1:
      if tokens[idx][1] == "CITY-N" and tokens[idx+1][1] == "CITY-NAME":
        del tokens[idx]
        break
      else:
        idx += 1
    

    # append the ? token
    tokens.append(("?", "QUERY", "QUERY"))

    self.verb_found = False
    return tokens