from spacy.matcher import Matcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for indefinite article followed by noun 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  matcher = Matcher(nlp.vocab)
  patterns = [
    [{"LOWER": {"IN": ["a", "an"]}}, {"POS": "ADV", "OP": "*"}, {"POS": "ADJ", "OP": "*"}, {"POS": "NOUN", "OP": "+"}],
  ]
  matcher.add("noun_indefinite_art", patterns)

  matches = matcher(doc)
  ranges = [(start, end) for _, start, end in matches]
  refined_matches = merge(ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})
  return result
