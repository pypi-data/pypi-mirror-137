from spacy.matcher import Matcher, PhraseMatcher, DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"POS": "ADV", "DEP": "advmod"}, {"POS": {"IN": ["ADJ", "ADV"]}}],
    [{"POS": "VERB"}, {"POS": "ADV", "DEP": "advmod"}],
  ]
  token_matcher.add("adj_comparative", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end].text
    result.append({"text": span})


  return result
   
