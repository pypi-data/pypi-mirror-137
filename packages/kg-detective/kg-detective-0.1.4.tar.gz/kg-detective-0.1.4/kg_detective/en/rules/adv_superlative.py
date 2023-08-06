from spacy.matcher import Matcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for superlative adverbs 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed

  Returns:
    list: list of spacy.tokens.Span
    nlp (spacy.language.Language): context language
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"LOWER": "the", "OP": "?"}, {"POS": "ADV", "OP": "?"}, {"LOWER": "most"}, {"POS": "ADV"}],
    [{"LOWER": "the", "OP": "?"}, {"POS": "ADV", "OP": "?"}, {"TAG": "RBS"}],
  ]
  token_matcher.add("adv_superlative", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append(span)

  return result
