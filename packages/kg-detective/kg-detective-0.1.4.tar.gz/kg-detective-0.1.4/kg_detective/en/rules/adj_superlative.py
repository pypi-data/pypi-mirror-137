from spacy.matcher import Matcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for superlative adjectives 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed

  Returns:
    list: list of spacy.tokens.Span
    nlp (spacy.language.Language): context language
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"LOWER": "the"}, {"POS": "ADV", "OP": "?"}, {"LOWER": "most"}, {"POS": "ADJ"}, {"POS": "NOUN", "DEP": "compound", "OP": "?"}, {"POS": "NOUN", "OP": "?"}],
    [{"LOWER": "the"}, {"POS": "ADV", "OP": "?"}, {"TAG": "JJS"}, {"POS": "NOUN", "DEP": "compound", "OP": "?"}, {"POS": "NOUN", "OP": "?"}],
  ]
  token_matcher.add("adj_superlative", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})

  return result
