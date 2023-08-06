from spacy.matcher import Matcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for comparative adjectives  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"POS": "ADV", "OP": "*"}, {"TAG": "JJR"}, {"LOWER": "than", "OP": "?"}],
    [{"POS": "ADV", "OP": "*"}, {"LOWER": "more"}, {"TAG": "JJ"}, {"LOWER": "than", "OP": "?"}],
    [{"POS": "ADV", "OP": "*"}, {"TAG": "JJR"}, {"LOWER": "and"}, {"TAG": "JJR"}],
    [{"POS": "DET", "OP": "?"}, {"POS": "ADV", "OP": "*"}, {"TAG": "JJR"}, {"POS": "NOUN"}],
    [{"POS": "DET", "OP": "?"}, {"POS": "ADV", "OP": "*"}, {"LOWER": "more"}, {"TAG": "JJ"}, {"POS": "NOUN"}],
  ]
  token_matcher.add("adj_comparative", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end].text
    result.append({"text": span})

  return result
   
