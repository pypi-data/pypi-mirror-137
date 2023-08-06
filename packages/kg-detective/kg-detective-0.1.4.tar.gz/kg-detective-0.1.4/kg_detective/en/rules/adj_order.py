from spacy.matcher import Matcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for order feature of adjective  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"TAG": {"IN": ["DT", "PRP$"]}, "OP": "?"}, {"POS": "ADV", "OP": "*"}, {"DEP": "amod"}, {"DEP": "amod", "OP": "+"}, {"POS": "NOUN", "DEP": "compound", "OP": "*"}, {"POS": "NOUN"}],
  ]
  token_matcher.add("adj_order", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]
  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append(span)

  return result
   
