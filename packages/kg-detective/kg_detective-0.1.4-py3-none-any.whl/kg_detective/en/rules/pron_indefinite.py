import os
from spacy.matcher import PhraseMatcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for indefinite pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """

  result = []
  
  pkg_path = os.path.dirname(__file__)
  INDEFINITE = open(pkg_path + '/pron_indefinite.txt', 'r').read().splitlines() 

  matcher = PhraseMatcher(nlp.vocab)

  patterns = [nlp.make_doc(text) for text in INDEFINITE]
  matcher.add("pron_indefinite", patterns)

  matches = matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    if any([e.pos_ == "PRON" for e in list(span)]):
      result.append({"text": span.text}) 

  return result
   
